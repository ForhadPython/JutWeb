from django.shortcuts import render
from django.views.generic import View
from skilldun.models import MetaData, CompanySocialMedia
from django.http import JsonResponse
from django.shortcuts import redirect

from .models import *


class EventHomeView(View):
    def get(self, request, page=1):
        page = int(page)

        event_items = EventItem.objects.filter(
                            active=True
                        ).order_by('-priority')

        if request.user.is_authenticated:
            user_events = EventBooking.objects.filter(
                            user=request.user,
                            event__id__in=[ev.id for ev in event_items],
                            verified=True,
                            event__active=True
                        ).all()
        else:
            user_events = []
        
        data = {
            'MetaData': MetaData.objects.filter(
                            active=True
                        ).first(),

            'CompanySocialMedia': CompanySocialMedia.objects.filter(
                            active=True
                        ).order_by('-priority'),

            'EventItem': event_items[((page-1)*6): (page*6)],
            'total_pagination': range(1, int(len(event_items.all())/6)+2),
            'EventBooking': user_events[((page-1)*6): (page*6)],
            'booking_total_pagination': range(1, int(len(user_events)/6)+2)
        }

        return render(request, 'events.html', data)


class SingleEventView(View):
    def get(self, request, slug):
        event = EventItem.objects.filter(
                        active=True, slug=slug
                    ).first()

        if request.user.is_authenticated:
            event_booking = EventBooking.objects.filter(
                user=request.user,
                event=event
            )
        else:
            event_booking = None

        if not event:
            return redirect('eventpage')

        data = {
            'MetaData': MetaData.objects.filter(
                            active=True
                        ).first(),

            'CompanySocialMedia': CompanySocialMedia.objects.filter(
                            active=True
                        ).order_by('-priority'),

            'EventItem': event,
            'EventBooking': event_booking
        }

        return render(request, 'events-single.html', data)


def book_event_seat(request):
    if not request.user.is_authenticated:
        return redirect('signin')

    try:
        data = dict(request.POST)

        data = {k: v[0] for k, v in data.items()}

        if data['csrfmiddlewaretoken']:
            data.pop('csrfmiddlewaretoken')

            if EventBooking.objects.filter(**data).exists():
                raise Exception("You already booked for the event.")

            event_booking = EventBooking.objects.create(**data)

            if request.is_ajax():
                data_record = event_booking.__dict__
                data_record.pop('_state')

                return JsonResponse(data_record)

        else:
            raise Exception('CSRF Token Missing')

    except Exception as e:
        if request.is_ajax():
            err = {
                'error': str(e)
            }

            response = JsonResponse(err)
            response.status_code = 403

            return response

    return redirect('homepage')

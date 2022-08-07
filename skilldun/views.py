from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

from skilldun.models import Founder
from .models import *
from event.models import EventItem
from course.models import CourseItem, Instructor


class HomePageView(View):
    def get(self, request):
        data = {
            'MetaData': MetaData.objects.filter(
                            active=True
                        ).first(),

            'HeadSlider': HeadSlider.objects.filter(
                            active=True
                        ).order_by('-priority'),

            'HeadSliderBottom': HeadSliderBottom.objects.filter(
                            active=True
                        ).order_by('-priority'),

            'ApplyNowItem': ApplyNowItem.objects.filter(
                            active=True
                        ).order_by('-priority'),

            'FacilityItem': FacilityItem.objects.filter(
                            active=True
                        ).order_by('-priority'),

            'TestimonialItem': TestimonialItem.objects.filter(
                            active=True
                        ).order_by('-priority'),

            'FooterSlider': FooterSlider.objects.filter(
                            active=True
                        ).order_by('-priority'),

            'AboutMVItem': AboutMVItem.objects.filter(
                            active=True
                        ).order_by('-priority'),
                        
            'EventItem': EventItem.objects.filter(
                            active=True
                        ).order_by('-priority')[:3],
            'CourseItem': CourseItem.objects.filter(
                            active=True
                        ).order_by('-priority')[:10],
            'Instructor': Instructor.objects.filter(
                            active=True
                        ).order_by('-priority')[:4]
        }

        return render(request, 'index.html', data)


class PaymentGuideline(View):
    def get(self, request):
        data = {
            'MetaData': MetaData.objects.filter(
                                active=True
                            ).first(),

            'CompanySocialMedia': CompanySocialMedia.objects.filter(
                                active=True
                            ).order_by('-priority'),

            'PaymentMethod': PaymentMethod.objects.filter(
                                active=True
                            ).order_by('-priority'),

            'PaymentInstruction': PaymentInstruction.objects.filter(
                                active=True
                            ).order_by('-priority'),

            'reference_number': request.user.id,

            'FooterSlider': FooterSlider.objects.filter(
                                active=True
                            ).order_by('-priority')
        }

        return render(request, 'payment-guideline.html', data)


class AboutUs(View):
    def get(self, request):
        data = {
            'MetaData': MetaData.objects.filter(
                active=True
            ).first(),

            'CompanySocialMedia': CompanySocialMedia.objects.filter(
                active=True
            ).order_by('-priority'),

            'AboutMVItem': AboutMVItem.objects.filter(
                active=True
            ).order_by('-priority'),

            'TestimonialItem': TestimonialItem.objects.filter(
                active=True
            ).order_by('-priority'),

            'Instructor': Instructor.objects.filter(
                            active=True
                        ).order_by('-priority'),

            'Founder': Founder.objects.filter(
                active=True
            ).order_by('-priority')
        }

        return render(request, 'about.html', data)


def contact_page(request):
    if request.method == "POST":
        contact = ContactMessage()
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        contact.name = name
        contact.subject = subject
        contact.email = email
        contact.phone = phone
        contact.message = message
        contact.save()
        return HttpResponse("Thanks for your contact.")

    data = {
        'MetaData': MetaData.objects.filter(
            active=True
        ).first(),

        'CompanySocialMedia': CompanySocialMedia.objects.filter(
            active=True
        ).order_by('-priority')
    }

    return render(request, "contact.html", data)

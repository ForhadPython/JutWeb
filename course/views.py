from django.shortcuts import render
from django.views.generic import View
from skilldun.models import MetaData, CompanySocialMedia
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse

from .models import *


class CourseHomeView(View):
    def get(self, request, page=1):
        page = int(page)
        course_items = CourseItem.objects.filter(
                            active=True
                        ).order_by('-priority')

        if request.user.is_authenticated:
            user_courses = CourseEnrollment.objects.filter(
                                student=request.user,
                                course__id__in=[cr.id for cr in course_items],
                                varified=True,
                                course__active=True
                            ).all()
            user_courses = [enroll.course for enroll in user_courses]
        else:
            user_courses = []

        data = {
            'MetaData': MetaData.objects.filter(
                            active=True
                        ).first(),

            'CompanySocialMedia': CompanySocialMedia.objects.filter(
                            active=True
                        ).order_by('-priority'),

            'CourseItem': course_items[((page-1)*6): (page*6)],
            'total_pagination': range(1, int(len(course_items.all())/6)+2),
            'CourseEnrollment': user_courses[((page-1)*6): (page*6)],
            'enroll_total_pagination': range(1, int(len(user_courses)/6)+2),
        }

        return render(request, 'courses.html', data)


class SingleCourseView(View):
    def get(self, request, slug):
        course = CourseItem.objects.filter(
                            active=True, slug=slug
                        ).first()

        if not course:
            return redirect('coursepage')

        if request.user.is_authenticated:
            enroll_c = CourseEnrollment.objects.filter(
                course=course
            )
        else:
            enroll_c = None

        data = {
            'MetaData': MetaData.objects.filter(
                            active=True
                        ).first(),

            'CompanySocialMedia': CompanySocialMedia.objects.filter(
                            active=True
                        ).order_by('-priority'),

            'CourseItem': course,
            'Instructor': course.instructor,
            'InstructorSocialMedia': InstructorSocialMedia.objects.filter(
                            active=True,
                            instructor=course.instructor
                        ),
            'CourseReview': CourseReview.objects.filter(
                            active=True,
                            course=course
                        ),
            'CourseCurriculum': CourseCurriculum.objects.filter(
                            active=True,
                            course=course
                        ),
            'CourseCategory': course.category,
            'CourseEnrollment': enroll_c
        }

        return render(request, 'courses-single.html', data)


class InstructorHomeView(View):
    def get(self, request, page=1):
        page = int(page)
        instructor_items = Instructor.objects.filter(
                            active=True
                        ).order_by('-priority')
        data = {
            'MetaData': MetaData.objects.filter(
                            active=True
                        ).first(),

            'CompanySocialMedia': CompanySocialMedia.objects.filter(
                            active=True
                        ).order_by('-priority'),

            'Instructor': instructor_items[((page-1)*6): (page*6)],
            'total_pagination': range(1, int(len(instructor_items.all())/6)+2)
        }

        return render(request, 'teachers.html', data)


class SingleInstructorView(View):
    def get(self, request, slug):
        instructor = Instructor.objects.filter(
                            active=True, slug=slug
                        ).first()
        social_media = InstructorSocialMedia.objects.filter(
                            instructor=instructor,
                            active=True
                        )
        courses = CourseItem.objects.filter(
                        active=True, 
                        instructor=instructor
                    ).order_by('-priority')
        reviews = InstructorReview.objects.filter(
                        active=True,
                        teacher=instructor
                    )
        data = {
            'MetaData': MetaData.objects.filter(
                            active=True
                        ).first(),

            'CompanySocialMedia': CompanySocialMedia.objects.filter(
                            active=True
                        ).order_by('-priority'),
            'Instructor': instructor,
            'InstructorSocialMedia': social_media,
            'CourseItem': courses,
            'InstructorReview': reviews
        }

        return render(request, 'teachers-single.html', data)


def add_to_favorite_list(request):
    try:
        data = dict(request.POST)

        data = {k: v[0] for k, v in data.items()}
        data['student'] = request.user

        if data['csrfmiddlewaretoken']:
            data.pop('csrfmiddlewaretoken')

            if FavoriteCourse.objects.filter(**data).exists():
                raise Exception("Already added to your favorite list.")

            favorite_course = FavoriteCourse.objects.create(**data)

            if request.is_ajax():
                data_record = favorite_course.__dict__
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


def review_course(request):
    try:
        data = dict(request.POST)

        data = {k: v[0] for k, v in data.items()}

        if data['csrfmiddlewaretoken']:
            data.pop('csrfmiddlewaretoken')

            if CourseReview.objects.filter(**data).exists():
                raise Exception("Already reviewed by you.")

            course_review = CourseReview.objects.create(**data)

            if request.is_ajax():
                data_record = course_review.__dict__
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


def review_instructor(request):
    try:
        data = dict(request.POST)

        data = {k: v[0] for k, v in data.items()}

        if data['csrfmiddlewaretoken']:
            data.pop('csrfmiddlewaretoken')

            if InstructorReview.objects.filter(**data).exists():
                raise Exception("Already reviewed by you.")

            review_instructor = InstructorReview.objects.create(**data)

            if request.is_ajax():
                data_record = review_instructor.__dict__
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


def enroll_course(request):
    try:
        data = dict(request.POST)

        data = {k: v[0] for k, v in data.items()}

        if data['csrfmiddlewaretoken']:
            data.pop('csrfmiddlewaretoken')

            if CourseEnrollment.objects.filter(**data).exists():
                raise Exception("You already enrolled to the course.")

            course_enrollment = CourseEnrollment.objects.create(**data)

            if not course_enrollment.course.free_course:
                return redirect('payment-guideline')

            if request.is_ajax():
                data_record = course_enrollment.__dict__
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

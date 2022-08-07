from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('courses/', CourseHomeView.as_view(), name='coursepage'),
    re_path('^courses/page/(?P<page>\d+)/$', CourseHomeView.as_view(), name='coursepagepagination'),
    re_path(
        '^courses/(?P<slug>[-\w]+)/$', 
        SingleCourseView.as_view(), 
        name='singlecoursepage'
    ),
    path('instructors/', InstructorHomeView.as_view(), name='instructorpage'),
    re_path('^instructors/page/(?P<page>\d+)/$', InstructorHomeView.as_view(), name='instructorpagepagination'),
    re_path('^instructors/(?P<slug>[-\w]+)/$', SingleInstructorView.as_view(), name='singleinstructorpage'),
    path('add-to-favorite/', add_to_favorite_list, name='add-to-favorite'),
    path('review-course/', review_course, name='review-course'),
    path('review-instructor/', review_instructor, name='review-instructor'),
    path('enroll-to-the-course/', enroll_course, name='enroll-to-the-course'),
]
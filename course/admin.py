from django.contrib import admin
from .models import *


admin.site.register(Instructor)
admin.site.register(InstructorSocialMedia)
admin.site.register(InstructorReview)
admin.site.register(CourseCategory)
admin.site.register(CourseItem)
admin.site.register(CourseEnrollment)
admin.site.register(CourseReview)
admin.site.register(FavoriteCourse)
admin.site.register(CourseCurriculum)
admin.site.register(CourseQuizSubmission)

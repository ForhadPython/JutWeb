from django.db import models


class Instructor(models.Model):
    user = models.ForeignKey(
                'account.User', 
                on_delete=models.CASCADE
            )
    name = models.CharField(max_length=32)
    position = models.CharField(max_length=32)
    description = models.TextField()
    about = models.TextField()
    achivement = models.TextField()
    objective = models.TextField()
    active = models.BooleanField(default=True)
    priority = models.IntegerField(default=1)
    slug = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class InstructorSocialMedia(models.Model):
    instructor = models.ForeignKey('Instructor', on_delete=models.CASCADE)
    media = models.ForeignKey(
                    'skilldun.SocialMedia', 
                    on_delete=models.CASCADE
                )
    profile_link = models.CharField(max_length=72)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "{} > {}".format(self.instructor, self.media)


class InstructorReview(models.Model):
    student = models.ForeignKey('account.User', on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    review = models.IntegerField(default=5)
    teacher = models.ForeignKey('Instructor', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "{} > {}".format(self.student, self.teacher)


class CourseCategory(models.Model):
    title = models.CharField(max_length=32)
    slug = models.CharField(max_length=24)

    def __str__(self):
        return self.title


class CourseItem(models.Model):
    instructor = models.ForeignKey(
                    'Instructor', 
                    on_delete=models.CASCADE
                )
    title = models.CharField(max_length=72)
    slug = models.CharField(max_length=56)
    category = models.ForeignKey(
                    'CourseCategory', 
                    on_delete=models.CASCADE
                )
    thumbnail = models.ImageField(upload_to='static/media/post/')
    caption = models.CharField(max_length=32)
    summery = models.TextField()
    requirements = models.TextField()
    total_duration = models.CharField(max_length=24)
    total_lectures = models.IntegerField(default=0)
    total_students = models.IntegerField(default=0)
    total_hearts = models.IntegerField(default=0)
    total_quizes = models.IntegerField(default=0)
    total_reviews = models.IntegerField(default=0)
    free_course = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    offer_price = models.DecimalField(max_digits=10, decimal_places=3)
    priority = models.IntegerField(default=1)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class CourseEnrollment(models.Model):
    student = models.ForeignKey('account.User', on_delete=models.CASCADE)
    course = models.ForeignKey(CourseItem, on_delete=models.CASCADE)
    varified = models.BooleanField(default=True)
    verify_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} > {}".format(self.student.full_name, self.course.title)


class CourseReview(models.Model):
    student = models.ForeignKey('account.User', on_delete=models.CASCADE)
    course = models.ForeignKey('CourseItem', on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    review = models.IntegerField(default=5)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "{} > {}".format(self.student, self.course)


class FavoriteCourse(models.Model):
    student = models.ForeignKey('account.User', on_delete=models.CASCADE)
    course = models.ForeignKey('CourseItem', on_delete=models.CASCADE)

    def __str__(self):
        return "{} > {}".format(self.student, self.course)


class CourseCurriculum(models.Model):
    course = models.ForeignKey('CourseItem', on_delete=models.CASCADE)
    lecture_serial = models.CharField(max_length=24)
    lecture_name = models.CharField(max_length=56)
    duration = models.CharField(max_length=24)
    description = models.TextField()
    lecture = models.FileField(
                    upload_to='static/media/coursecurriculam/', 
                    blank=True, null=True
                )
    lecture_link = models.CharField(
                        max_length=56, 
                        blank=True, null=True
                    )
    choice_1 = models.CharField(max_length=32)
    choice_2 = models.CharField(max_length=32)
    choice_3 = models.CharField(max_length=32)
    choice_4 = models.CharField(max_length=32)
    choices_answer = models.CharField(max_length=32)
    lecture_type = models.IntegerField(choices=(
                        (1, 'Video'),
                        (2, 'Text'),
                        (3, 'Quiz')
                    ), default=1)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return "{} > {}: {}".format(
            self.course, 
            self.lecture_serial, 
            self.lecture_name
        )


class CourseQuizSubmission(models.Model):
    course = models.ForeignKey('CourseItem', on_delete=models.CASCADE)
    student = models.ForeignKey('account.User', on_delete=models.CASCADE)
    course_curriculum = models.ForeignKey(
                                'CourseCurriculum',
                                on_delete=models.CASCADE
                            )
    answer = models.IntegerField()
    answer_text = models.CharField(max_length=32)

    def __str__(self):
        return "{} > {}: {}".format(
            self.student,
            self.course,
            self.course_curriculum
        )

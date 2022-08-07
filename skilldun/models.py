from django.db import models


class MetaData(models.Model):
    favicon = models.FileField(upload_to='static/media/metadata/')
    logo = models.ImageField(upload_to='static/media/metadata/')
    logo_caption = models.CharField(max_length=24)
    menu = models.CharField(max_length=24)
    site_title = models.CharField(max_length=72)
    location = models.CharField(max_length=36)
    email = models.CharField(max_length=72)
    opening_hour = models.CharField(max_length=56)
    phone = models.CharField(max_length=72)
    description = models.TextField()
    address = models.CharField(max_length=56)
    copyright = models.CharField(max_length=72)
    slider_title = models.CharField(max_length=56)
    slider_description = models.CharField(max_length=172)
    slider_button_1_label = models.CharField(max_length=14)
    slider_button_2_label = models.CharField(max_length=14)
    slider_button_1_link = models.CharField(max_length=56)
    slider_button_2_link = models.CharField(max_length=56)
    slider_2_title = models.CharField(max_length=56)
    about_title = models.CharField(max_length=24)
    about_description = models.TextField()
    about_image = models.ImageField(upload_to='static/media/metadata/')
    about_image_caption = models.CharField(max_length=32)
    about_background = models.ImageField(upload_to='static/media/metadata/')
    about_background_caption = models.CharField(max_length=32)
    facility_background = models.ImageField(upload_to='static/media/metadata/')
    facility_video_link = models.CharField(max_length=72)
    teacher_title = models.CharField(max_length=24)
    teacher_description = models.TextField()
    testimonial_background = models.ImageField(upload_to='static/media/metadata/')
    testimonial_background_caption = models.CharField(max_length=32)
    mobile = models.CharField(max_length=72)
    contact_email = models.CharField(max_length=72)
    event_page_bg = models.ImageField(upload_to='static/media/metadata/')
    event_page_bg_caption = models.CharField(max_length=32)
    course_page_bg = models.ImageField(upload_to='static/media/metadata/')
    course_page_bg_caption = models.CharField(max_length=32)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.site_title


class SocialMedia(models.Model):
    fa_icon_class = models.CharField(max_length=32)
    link = models.CharField(max_length=56)
    name = models.CharField(max_length=14)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class HeadSlider(models.Model):
    image = models.FileField(upload_to='static/media/headslider/')
    caption = models.CharField(max_length=32)
    priority = models.IntegerField(default=1)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.caption


class HeadSliderBottom(models.Model):
    image = models.FileField(upload_to='static/media/headsliderbottom/')
    caption = models.CharField(max_length=32)
    priority = models.IntegerField(default=1)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.caption


class ApplyNowItem(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField()
    button_label = models.CharField(max_length=14)
    button_link = models.CharField(max_length=56)
    priority = models.IntegerField(default=1)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class FacilityItem(models.Model):
    image = models.FileField(upload_to='static/media/facilityitem/')
    caption = models.CharField(max_length=32)
    title = models.CharField(max_length=32)
    description = models.TextField()
    priority = models.IntegerField(default=1)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class TestimonialItem(models.Model):
    image = models.FileField(upload_to='static/media/testimonialitem/')
    caption = models.CharField(max_length=32)
    description = models.TextField()
    name = models.CharField(max_length=32)
    designation = models.TextField()
    priority = models.IntegerField(default=1)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class FooterSlider(models.Model):
    image = models.FileField(upload_to='static/media/footerslider/')
    caption = models.CharField(max_length=32)
    priority = models.IntegerField(default=1)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.caption


class AboutMVItem(models.Model):
    title = models.CharField(max_length=8)
    subtitle = models.CharField(max_length=14)
    description = models.TextField()
    priority = models.IntegerField(default=1)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class CompanySocialMedia(models.Model):
    media = models.ForeignKey(SocialMedia, on_delete=models.CASCADE)
    link = models.CharField(max_length=56)
    priority = models.IntegerField(default=1)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.media)


class ContactMessage(models.Model):
    name = models.CharField(max_length=32)
    email = models.EmailField()
    subject = models.CharField(max_length=56)
    phone = models.CharField(max_length=15)
    message = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class PaymentMethod(models.Model):
    title = models.CharField(max_length=32)
    thumbnail = models.ImageField(upload_to='static/media/paymentmethod/')
    priority = models.IntegerField(default=1)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class PaymentInstruction(models.Model):
    title = models.CharField(max_length=24)
    subtitle = models.CharField(max_length=32)
    description = models.TextField()
    priority = models.IntegerField(default=1)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Founder(models.Model):
    image = models.FileField(upload_to='static/media/founder/')
    name = models.CharField(max_length=40)
    designations = models.CharField(max_length=40)
    description = models.CharField(max_length=400)
    priority = models.IntegerField(default=1)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

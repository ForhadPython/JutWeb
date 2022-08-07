from django.db import models


class EventItem(models.Model):
    title = models.CharField(max_length=172)
    slug = models.CharField(max_length=32)
    date_time_from = models.DateTimeField()
    date_time_to = models.DateTimeField()
    location = models.CharField(max_length=72)
    image = models.ImageField(upload_to='static/media/eventitem/')
    caption = models.CharField(max_length=32)
    description = models.TextField()
    address = models.CharField(max_length=72)
    priority = models.IntegerField(default=1)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class EventBooking(models.Model):
    user = models.ForeignKey('account.User', on_delete=models.CASCADE)
    event = models.ForeignKey(EventItem, on_delete=models.CASCADE)
    verified = models.BooleanField(default=True)

    def __str__(self):
        return self.event.title

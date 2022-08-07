from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('events/', EventHomeView.as_view(), name='eventpage'),
    re_path('^events/(?P<slug>[-\w]+)/$', SingleEventView.as_view(), name='singleeventpage'),
    re_path('^events/page/(?P<page>\d+)/$', EventHomeView.as_view(), name='eventpagepagination'),
    path('book-event-seat/', book_event_seat, name='book-event-seat'),
]
from django.db import models
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User


class Event(models.Model):
    event_name = models.CharField(max_length=100)
    short_description = models.CharField(max_length=200, blank=False, null=True)
    full_description = models.TextField(max_length=1000, blank=True)
    event_creator_id = models.TextField(max_length=10, default=0)
    create_date = models.DateTimeField(default=datetime.now, blank=True, null=False)
    start_date = models.DateTimeField(blank=True)
    end_date = models.DateTimeField(blank=True)
    is_closed = models.IntegerField(default=0)
    image = models.ImageField(default='default.jpg', upload_to='event_pics')

    def __str__(self):
        return self.event_name

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk': self.pk})


class EventUser(models.Model):
    event_id = models.TextField(max_length=10, default=0)
    user_id = models.TextField(max_length=10, default=0)

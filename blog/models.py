from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Weather(models.Model):
    city = models.CharField(max_length=100, primary_key=True)
    degree = models.IntegerField()
    icon_name = models.CharField(max_length=20)
    last_update = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.city

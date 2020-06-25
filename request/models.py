from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Request(models.Model):
    title = models.CharField(max_length = 50, verbose_name='Project Title')
    abstract = models.TextField(null = True)
    hardware = models.TextField(null = True)
    software = models.TextField(null=True)
    budget = models.IntegerField(default=0)
    date = models.DateTimeField(default = timezone.now)
    accepted = models.BooleanField(default=False)
    pending = models.BooleanField(default=True)
    requester = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.title
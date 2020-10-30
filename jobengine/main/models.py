from django.db import models

# Create your models here.
from django.utils import timezone


class JobEntry(models.Model):
    name = models.CharField(max_length=128, unique=True)
    mode = models.CharField(max_length=128)
    cron_string = models.CharField(max_length=128)
    optional_params = models.CharField(max_length=256)
    running = models.BooleanField(default=False)
    status = models.IntegerField(default=-1)
    date = models.DateTimeField(max_length=128, default=timezone.now)


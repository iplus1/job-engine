from django.db import models


class JobEntry(models.Model):
    """Stores a single job entry."""

    name = models.CharField(max_length=128, unique=True)
    mode = models.CharField(max_length=128)
    cron_string = models.CharField(max_length=128, default=None, null=True)
    command_ipynb = models.CharField(max_length=512, default=None, null=True)
    running = models.BooleanField(default=False)
    last_status = models.IntegerField(null=True)
    current_status = models.IntegerField(null=True)
    output = models.CharField(null=True, max_length=512, default=None)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    enabled = models.BooleanField(default=True)

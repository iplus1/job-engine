from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from main.views import create_job, get_jobs, index, control_job

urlpatterns = [
    url(r'^create_job/?$', create_job),
    url(r'^get_jobs/', get_jobs),
    url(r'^control_job/$', control_job),
    url(r'^', index, name='index'),
]

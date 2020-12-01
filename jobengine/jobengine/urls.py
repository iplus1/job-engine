from django.conf.urls import url
from django.contrib import admin

from main.views import create_job, get_jobs, get_job, index, control_job, get_log, get_backups

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^create_job/?$', create_job),
    url(r'^get_jobs/', get_jobs),
    url(r'^get_job/?$', get_job),
    url(r'^control_job/$', control_job),
    url(r'^get_log/?$', get_log),
    url(r'^get_backups/?$', get_backups),
    url(r'^', index, name='index'),
]


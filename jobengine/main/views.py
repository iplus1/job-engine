import json

from django.http import HttpResponse, JsonResponse

# Create your views here.
from django.template.response import TemplateResponse
from django.views.decorators.csrf import ensure_csrf_cookie

from main.internals.job import Job
from main.internals.db_helper import DBHelper
from main.internals.website_helper import WebsiteHelper


@ensure_csrf_cookie
def index(request):
    return TemplateResponse(request, 'index.html')


def get_jobs(request):
    all_job_entries = DBHelper.get_jobs()
    return JsonResponse(all_job_entries, safe=False)


def create_job(request):
    raw_data = request.read()
    try:
        json_data = json.loads(raw_data)
        job_name = json_data['job_name']
        mode = json_data['mode']
        cron_string = json_data['cron_string']
        optional_params = json_data['optional_params']
        job = Job(name=job_name, mode=mode, cron_string=cron_string, optional_params=optional_params)
        return HttpResponse(WebsiteHelper.perform_action(job, action='create'))
    except Exception as e:
        print(e)
        return HttpResponse('An Error occurred')


def control_job(request):
    raw_data = request.read()
    try:
        json_data = json.loads(raw_data)
        job_entry = DBHelper.get_job_by_id(json_data['id'])
        job = Job(name=job_entry.name, mode=job_entry.mode, cron_string=job_entry.cron_string, optional_params=job_entry.optional_params)
        return HttpResponse(WebsiteHelper.perform_action(job, json_data['action'], job_entry.id))
    except Exception as e:
        print(e)
        return HttpResponse('An Error Occurred')


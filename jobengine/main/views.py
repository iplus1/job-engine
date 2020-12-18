import json
import os
from os.path import join

from django.forms import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.template.response import TemplateResponse
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie

from main.internals.control_helper import ControlHelper
from main.internals.db_helper import DBHelper
from main.internals.job import Job

WORK_DIR = '/jobengine/ipynbs'


@ensure_csrf_cookie
def index(request):
    """Return the index.html template with the necessary context.

    The for loop walks through the specified WORK_DIR and collects
    files ending with '.ipynb'. The ipynb-files are then fed to
    the index.html template in an object named 'context'.

    **Context**

    ``nbs``
        A list of ipynb-files.

    **Template:**

    :template:`index.html`

    :param request: Request Object
    :return: index.html
    """

    ipynb_files = []
    for root, directories, filenames in os.walk(WORK_DIR):
        for filename in filenames:
            if filename.endswith(".ipynb"):
                if '/.ipynb_checkpoints' not in root:
                    ipynb_files.append(join(root, filename))

    context = {
        'nbs': ipynb_files
    }
    return TemplateResponse(request, 'index.html', context)


def get_jobs(request):
    """Return JSON-Response containing all entries of the job DB.

    :param request: No attributes expected.
    :return: JSON containing all jobs.
    """

    try:
        all_job_entries = DBHelper.get_jobs()
        return JsonResponse(all_job_entries, safe=False)
    except Exception as e:
        print(f'[{timezone.now()}] Server Error: {e}')
        return HttpResponse(f'[{timezone.now()}] Server Error: {e}')


def get_job(request):
    """Return JSON-Response containing the entry of the specified job.

    :param request: Expected GET-attributes:
        'job_name': string;

    :return: JSON containing the specified job.
    """

    try:
        job_name = request.GET['job_name']
        job_entry = DBHelper.get_job_by_name(job_name)
        return JsonResponse(model_to_dict(job_entry), safe=False)
    except Exception as e:
        print(f'[{timezone.now()}] Server Error: {e}')
        return HttpResponse(f'[{timezone.now()}] Server Error: {e}')


def get_backups(request):
    """Return JSON-Response containing all entries that resemble backup-job entries.

    :param request: Expect no attributes:
    :return: JSON containing the backup job.
    """

    try:
        job_entries = DBHelper.get_backups()
        return JsonResponse(job_entries, safe=False)
    except Exception as e:
        print(f'[{timezone.now()}] Server Error: {e}')
        return HttpResponse(f'[{timezone.now()}] Server Error: {e}')


def get_log(request):
    """Return a specific log as HttpResponse.

    Fetches the entry of a specific job from the database by ID.
    Creates a job-Object from the data of the fetched entry and
    gets a specific log file from the specified job.

    :param request: Expected GET-Parameter:
        'id': int;
        'log_file': string;
    :return: Requested Log file.
    :exception Exception if try fails. Printed to the terminal and returned as HttpResponse.:
    """

    try:
        job_id = request.GET["id"]
        log_file = request.GET["log_file"]
        job_entry = DBHelper.get_job_by_id(job_id)
        job = Job(name=job_entry.name, mode=job_entry.mode, cron_string=job_entry.cron_string,
                  command_ipynb=job_entry.command_ipynb)
        return HttpResponse(job.get_log(log_file))
    except Exception as e:
        print(f'[{timezone.now()}] Server Error: {e}')
        return HttpResponse(f'[{timezone.now()}] Server Error: {e}')


def create_job(request):
    """Return HttpResponse with the status of the performed create-action.

    Creates a job object from the JSON-attributes attached in the request and
    performs a 'create' action to make an entry in the 'main_jobentry' table
    and create the necessary directories and files for the job.

    :param request: Expected JSON-attributes:
        'job_name': string;
        'mode': string;
        'cron_string': string;
        'command': string;
        'ipynb_file': string

    :return: Status of the perform_action() function.
    :exception Exception if try fails. Printed to the terminal and returned as HttpResponse.:
    """

    try:
        raw_data = request.read()
        json_data = json.loads(raw_data)
        job_name = json_data['job_name']
        mode = json_data['mode']
        cron_string = json_data['cron_string']
        command = json_data['command']
        ipynb_file = json_data['ipynb_file']
        if 'ipynb' in mode:
            command_ipynb = ipynb_file
        else:
            command_ipynb = command
        job = Job(name=job_name, mode=mode, cron_string=cron_string, command_ipynb=command_ipynb)
        return HttpResponse(ControlHelper(job, 'create').perform_action())
    except Exception as e:
        print(f'[{timezone.now()}] Server Error: {e}')
        return HttpResponse(f'[{timezone.now()}] Server Error: {e}')


def control_job(request):
    """Return Http- or TemplateResponse depending on the 'action' parameter.

    Fetches the entry of a specific job from the database by ID.
    Creates a job-Object from the data of the fetched entry and
    performs an action defined by the 'action' parameter.

    If the 'action' parameter matches `logs` the response will change from
    HttpResponse to TemplateResponse.

    TemplateResponse
    ----------------

    **Context**

        ``list``
            contains log_file names

    **Template:**

    :template:`logs_selection.html`

    :param request: Expected JSON-attributes:
        'id': int;
        'action': string;
    :return: Either the status of the perform_action() function or the logs_selection.html
    :exception Exception if try fails. Printed to the terminal and returned as HttpResponse.:
    """

    try:
        raw_data = request.read()
        json_data = json.loads(raw_data)
        job_entry = DBHelper.get_job_by_id(json_data['id'])
        job = Job(name=job_entry.name, mode=job_entry.mode, cron_string=job_entry.cron_string,
                  command_ipynb=job_entry.command_ipynb)
        if json_data['action'] != 'logs':
            return HttpResponse(ControlHelper(job, json_data['action'], job_entry.id).perform_action())
        else:
            context = ControlHelper(job, json_data['action'], job_entry.id).perform_action()
            return TemplateResponse(request, 'logs_selection.html', context)
    except Exception as e:
        print(f'[{timezone.now()}] Server Error: {e}')
        return HttpResponse(f'[{timezone.now()}] Server Error: {e}')



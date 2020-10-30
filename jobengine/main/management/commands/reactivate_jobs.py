from django.core.management.base import BaseCommand

from main.internals.job import Job
from main.internals.db_helper import DBHelper


class Command(BaseCommand):
    help = 'Reactivates all running jobs from the Database.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        all_jobs = DBHelper.get_all_jobs()
        try:
            for job_entry in all_jobs:
                job = Job(name=job_entry['name'], mode=job_entry['mode'], cron_string=job_entry['cron_string'],
                          optional_params=job_entry['optional_params'])
                job.create_job()
            return 'All jobs should be restarted.'
        except Exception as e:
            print(e)
            return f'An Error occurred while restarting the jobs.'


import os
import shutil

from django.core.management.base import BaseCommand
from django.utils import timezone

from main.internals.db_helper import DBHelper
from main.internals.job import Job


class Command(BaseCommand):
    help = 'Reactivate all Cron-Jobs from the Database.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        """Fetch the Cron-Jobs from the database and create them.

        :return: Status of the restart.
        """

        all_crons = DBHelper.get_all_crons()
        for job_entry in all_crons:
            try:
                job = Job(name=job_entry['name'], mode=job_entry['mode'], cron_string=job_entry['cron_string'],
                          command=job_entry['command'], ipynb_file=job_entry['ipynb_file'])
                if 'ipynb' in job.mode:
                    print(f'[{timezone.now()}]{job.create_ipynb_cron()}')
                else:
                    print(f'[{timezone.now()}]{job.create_cron()}')
            except Exception as e:
                print(f'[{timezone.now()}] Server Error: {e}')
        print(f'[{timezone.now()}] All jobs should be restarted.')

        dir_list = os.listdir('/jobengine/jobs')
        all_jobs = DBHelper.get_jobs()
        for directory in dir_list:
            if os.path.isdir(f'/jobengine/jobs/{directory}'):
                if not any(entry['name'] == directory for entry in all_jobs):
                    shutil.rmtree(f'/jobengine/jobs/{directory}')
                    print(f'[{timezone.now()}] {directory} is not associated with a job and will be destroyed.')
        print(f'[{timezone.now()}] job dir should be clean now.')


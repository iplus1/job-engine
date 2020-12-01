import os

from django.core.management.base import BaseCommand
from django.utils import timezone

from main.internals.db_helper import DBHelper
from main.internals.job import Job


class Command(BaseCommand):
    help = 'Check if a job is running.'

    def add_arguments(self, parser):
        """Create a parser to handle arguments."""

    def handle(self, *args, **options):
        """Check if a job is running.

        :param options: Expects `job_name`.
        :return: Status of the check.
        """

        all_entries = DBHelper.get_jobs()
        for job_entry in all_entries:
            try:
                job = Job(name=job_entry['name'], mode=job_entry['mode'], cron_string=job_entry['cron_string'],
                          command=job_entry['command'], ipynb_file=job_entry['ipynb_file'])
                output = ''
                if os.path.isfile(f'{job.job_dir}/last_output'):
                    with open(f'{job.job_dir}/last_output', 'r') as file:
                        output = file.read()
                DBHelper.update_running_and_std(job_entry['id'], job.check_if_running(), output)
            except Exception as e:
                print(f'[{timezone.now()}] Server Error: {e}')
        return f'[{timezone.now()}] All jobs should be updated.'


import os

from django.core.management.base import BaseCommand
from django.utils import timezone

from main.internals.db_helper import DBHelper


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
                if os.path.isdir(f'/jobengine/jobs/{job_entry["name"]}'):
                    os.rename(f'/jobengine/jobs/{job_entry["name"]}', f'/jobengine/jobs/{job_entry["id"]}')
            except Exception as e:
                print(f'[{timezone.now()}] Server Error: {e}')
        return f'[{timezone.now()}] All jobs should be migrated.'



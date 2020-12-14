from django.core.management.base import BaseCommand
from django.utils import timezone

from main.internals.db_helper import DBHelper

BASE_DIR = '/jobengine'


class Command(BaseCommand):
    help = 'Update a job with a new status.'

    def add_arguments(self, parser):
        """Create a parser to handle arguments."""

        parser.add_argument('job_name', type=str)
        parser.add_argument('return_code', type=int)
        parser.add_argument('job_state', type=str)

    def handle(self, *args, **options):
        """Update a job with a new status.

        Reads in the `last_output` file of the job to fetch
        the latest STDOUT and STDERR of the process.

        :param options: Expects `job_name` and `return_code`
        :return: Status of the update.
        """

        try:
            # Clear the last_output file for a new start
            if options['job_state'] == 'start':
                open(f'{BASE_DIR}/jobs/{options["job_name"]}/last_output', 'w').close()
            DBHelper.update_state_name(options['job_name'], options['return_code'], options['job_state'])
        except Exception as e:
            print(f'[{timezone.now()}] Server Error: {e}')
            return f'An Error occurred while making the database entry for job: {options["job_name"]}'


import re

from django.utils import timezone

from main.internals.db_helper import DBHelper
from main.internals.job import Job


class ControlHelper:

    def __init__(self, job_data, action, job_new_data=None):
        """Constructor for the ControlHelper.

        :param job_data: dict: contains the data necessary for a job.
        :param action: string: specifies an action.
        :param job_new_data: dic: contains the data necessary to change a jobs information.
        """

        self.action = action
        self.job_new_data = job_new_data
        
        """To avoid lifecycle problems the database entry has to exist before creating the job-object."""
        if self.action == 'create':
            job_entry = DBHelper.create_entry(job_data)
            self.job = Job(name=job_entry.name, mode=job_entry.mode, cron_string=job_entry.cron_string,
                           command_ipynb=job_entry.command_ipynb, job_id=job_entry.id)

        else:
            job_entry = DBHelper.get_job_by_id(job_data['id'])
            self.job = Job(name=job_entry.name, mode=job_entry.mode, cron_string=job_entry.cron_string,
                           command_ipynb=job_entry.command_ipynb, job_id=job_entry.id)

    def perform_action(self):
        """Execute a specific function depending on the 'action' parameter.

        :return: Value of the invoked function.
        :rtype: str
        :exception Exception if try fails. Printed to the terminal and returned string.:
        """

        try:
            if self.action == 'delete':
                return self.delete()

            elif self.action == 'start':
                return self.start()

            elif self.action == 'stop':
                return self.stop()

            elif self.action == 'cleanup':
                return self.cleanup()

            elif self.action == 'update':
                return self.update()

            elif self.action == 'logs':
                return self.logs()

            elif self.action == 'edit':
                return self.edit()

            elif self.action == 'enable' and 'cron' in self.job.mode:
                return self.enable()

            elif self.action == 'disable' and 'cron' in self.job.mode:
                return self.disable()

        except Exception as e:
            print(f'[{timezone.now()}] Server Error: {e}')
            return f'[{timezone.now()}] Server Error: {e} with {self.job.name}'

    def create(self):
        """Execute a create_ function depending on the 'mode' attribute of the specified job.

        :return: Status of the performed create_ function.
        :rtype: str
        """

        if self.job.mode == 'cron':
            return self.job.create_cron()
        elif self.job.mode == 'cron ipynb':
            self.job.copy_ipynb_file()
            return self.job.create_cron()
        elif self.job.mode == 'cmd':
            return self.job.create_cmd()
        elif self.job.mode == 'ipynb':
            self.job.copy_ipynb_file()
            return self.job.create_cmd()

    def delete(self):
        """Delete the database entry of a job and execute necessary delete_ functions.

        Invoke kill_process() to properly kill the process.
        Invoke delete_job_dir() to properly delete the directory of the job.
        If the job is a Cron-Job -> invoke delete_cron() to clear the Crontab entry.

        :return: Message of completed delete action.
        """

        DBHelper.delete_entry(self.job.id)
        self.job.kill_process()
        self.job.delete_job_dir()
        if 'cron' in self.job.mode:
            self.job.delete_cron()
        return f'<b>{self.job.name}:</b> is now deleted.'

    def start(self):
        """Start an execution of a job by invoking the create() function.

        If the specified job is a Cron-Job dont invoke the create() function.

        :return: Message of the create() function || String: Cron specific handling.
        """

        if 'cron' in self.job.mode:
            return f'<b>{self.job.name}:</b> is a Cron-Job and will be started by the Crontab.'
        else:
            return self.create()

    def stop(self):
        """Stop the execution of a job by killing the process.

        If the process was killed, update the status of the job with the exit code 137.

        :return: Status of the Job.
        """

        if self.job.kill_process():
            DBHelper.stop_process(self.job.id)
            return f'<b>{self.job.name}:</b> is now stopped.'
        else:
            return f'<b>{self.job.name}:</b> is not running.'

    def cleanup(self):
        """Clean the directory of the job by deleting all log files.

        :return: Status of the cleanup_job_dir() function.
        :rtype: str
        """

        return self.job.cleanup_job_dir()

    def update(self):
        """Update the ipynb file that the job uses for its execution.

        This is necessary because the job uses a copy of the initial ipynb file
        to ensure that the user can work on the initial file without interfering
        with the execution of the job.

        :return: Status of the copy_ipynb_file() function.
        :rtype: str
        """

        return self.job.copy_ipynb_file()

    def logs(self):
        """Return all log files of a job as a list.

        :return: All log files of the job.
        :rtype: list
        """

        return self.job.get_logs()

    def edit(self):
        """Edit the job with new parameters.

        :return: Status of the edit() function
        :rtype: str
        """

        if 'cron' in self.job.mode:
            self.job.delete_cron()
        else:
            self.job_new_data['cron_string'] = ''

        DBHelper.edit_job(self.job.id, self.job_new_data['name'], self.job_new_data['cron_string'],
                          self.job_new_data['command_ipynb'])

        """Start the new job depending on its mode"""
        self.job = Job(name=self.job_new_data['name'], mode=self.job.mode, cron_string=self.job_new_data['cron_string'],
                       command_ipynb=self.job_new_data['command_ipynb'], job_id=self.job.id)
        if 'cron' in self.job.mode:
            self.job.create_cron()
        if 'ipynb' in self.job.mode:
            self.job.copy_ipynb_file()

        return f'<b>{self.job.name}:</b> The job info has been modified.'

    def enable(self):
        """Enables a cron-job."""

        DBHelper.update_enabled(self.job.id, True)
        self.create()
        return f'<b>{self.job.name}:</b> The job has been enabled.'

    def disable(self):
        """Disables a cron-job."""

        DBHelper.update_enabled(self.job.id, False)
        self.job.delete_cron()
        return f'<b>{self.job.name}:</b> The job has been disabled.'

    @staticmethod
    def check_special_characters(string):
        """Check a string for forbidden characters.

        :param string: Expects a valid string.
        :return: boolean
        """
        search = re.compile(r'[^a-zA-Z0-9_\-\s+]').search
        return bool(search(string))


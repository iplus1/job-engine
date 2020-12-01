from django.utils import timezone

from main.internals.db_helper import DBHelper


class ControlHelper:

    def __init__(self, job, action, job_id=None):
        """Constructor for the ControlHelper.

        :param job: Job-Object: main.internals.job.
        :param action: string: specifies an action.
        :param job_id: int: indicates the ID of a job.
        """

        self.job = job
        self.job_id = job_id
        self.action = action

    def perform_action(self):
        """Execute a specific function depending on the 'action' parameter.

        In the special case of the 'create' action a database entry is created
        before the function create() is being executed.

        :return: Value of the invoked function.
        :rtype: str
        :exception Exception if try fails. Printed to the terminal and returned string.:
        """

        try:
            if self.action == 'create':
                DBHelper.create_entry(self.job)
                return self.create()

            elif self.action == 'delete':
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
            return self.job.create_ipynb_cron()
        elif self.job.mode == 'cmd':
            return self.job.create_cmd()
        elif self.job.mode == 'cmd ipynb':
            return self.job.create_ipynb_cmd()

    def delete(self):
        """Delete the database entry of a job and execute necessary delete_ functions.

        Invoke kill_process() to properly kill the process.
        Invoke delete_job_dir() to properly delete the directory of the job.
        If the job is a Cron-Job -> invoke delete_cron() to clear the Crontab entry.

        :return: Message of completed delete action.
        """

        DBHelper.delete_entry(self.job_id)
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
            DBHelper.update_current_status_name(self.job.name, 137)
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


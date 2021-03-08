import os

from django.utils import timezone

from main.internals.job import Job
from main.models import JobEntry


class DBHelper:
    """Helper class to handle all the database operations."""

    @staticmethod
    def get_jobs():
        """Get all job entries and return as list."""

        return list(JobEntry.objects.values())

    @staticmethod
    def get_job_by_id(job_id):
        """Get one specific job by its ID."""

        return JobEntry.objects.get(id=job_id)

    @staticmethod
    def get_job_by_name(job_name):
        """Get one specific job by its name."""

        return JobEntry.objects.get(name=job_name)

    @staticmethod
    def get_all_crons():
        """Get all jobs with the mode including 'cron'."""

        return list(JobEntry.objects.filter(mode__contains='cron').values())

    @staticmethod
    def get_backups():
        """Get all backup-job entries and return as a list."""

        return list(JobEntry.objects.filter(name__contains='backup').values())

    @staticmethod
    def delete_entry(job_id):
        """Delete a specific job entry by its ID."""

        try:
            JobEntry.objects.filter(id=job_id).delete()
        except Exception as e:
            print(f'[{timezone.now()}] Server Error: {e}')
            return f'[{timezone.now()}] Server Error: {e}'
        return 'Entry deleted.'

    @staticmethod
    def update_running_and_std(job_id, running, output):
        """Update the running state of a job by its ID."""

        JobEntry.objects.filter(id=job_id).update(running=running, output=output)
        return f'Job running updated.'

    @staticmethod
    def update_running(job_id, job_running):
        """Update the running state of a job by its ID."""

        JobEntry.objects.filter(name=job_id).update(running=job_running)
        return f'Job running updated.'

    @staticmethod
    def update_enabled(job_id, enabled):
        """Update the enabled state of a job by its ID."""

        JobEntry.objects.filter(id=job_id).update(enabled=enabled)
        return f'Job enabled update.'

    @staticmethod
    def update_current_status(job_id, job_status):
        """Update the status of a job by its ID."""

        JobEntry.objects.filter(id=job_id).update(current_status=job_status)
        return f'Job status updated.'

    @staticmethod
    def update_current_status_name(job_name, job_status):
        """Update the status of a job by its name."""

        JobEntry.objects.filter(name=job_name).update(current_status=job_status)
        return f'Job status updated.'

    @staticmethod
    def update_state_id(job_id, job_status, state):
        """Update the overall state of the job.

        Depending on the state variable update multiple columns of the job.

        start: Make sure that status, output and end_date are cleared for a new execution of the job.
        end: Make sure that the status of the job and the end_date is set.
        """
        job_entry = DBHelper.get_job_by_id(job_id)
        if state == 'start':
            JobEntry.objects.filter(id=job_id).update(running=True, last_status=job_entry.current_status,
                                                      current_status=None, output=None, start_date=timezone.now(),
                                                      end_date=None)
        elif state == 'end':
            if job_entry.last_status is not None:
                JobEntry.objects.filter(id=job_id).update(running=False, current_status=job_status,
                                                          end_date=timezone.now())
            else:
                JobEntry.objects.filter(id=job_id).update(running=False, last_status=job_status,
                                                          current_status=job_status,
                                                          end_date=timezone.now())
        return f'Job status updated.'

    @staticmethod
    def update_std_all():
        """Update the STD of all running jobs."""

        all_job_entries = DBHelper.get_jobs()
        for job_entry in all_job_entries:
            try:
                job = Job(name=job_entry['name'], mode=job_entry['mode'], cron_string=job_entry['cron_string'],
                          command_ipynb=job_entry['command_ipynb'], job_id=job_entry['id'])
                if os.path.isfile(f'{job.job_dir}/last_output'):
                    with open(f'{job.job_dir}/last_output', 'r') as file:
                        output = file.read()
                    JobEntry.objects.filter(id=job.id).update(output=output)
            except Exception as e:
                print(f'[{timezone.now()}] Server Error: {e}')
                return f'[{timezone.now()}] Server Error: {e}'
        return f'All STDs updated.'

    @staticmethod
    def stop_process(job_id):
        """Mirror the stop of a process by changing the status to 137 and the end date to current"""

        JobEntry.objects.filter(id=job_id).update(current_status=137, end_date=timezone.now())
        return

    @staticmethod
    def edit_job(job_id, job_name, job_cron, job_command):
        """Edit the Name, Crontab and Command of a job.

        Sets the current_status, start_date and end_date to its default state.
        """

        JobEntry.objects.filter(id=job_id).update(name=job_name, cron_string=job_cron, command_ipynb=job_command)
        return f'Job info updated.'

    @staticmethod
    def create_entry(job_data):
        """Create an entry in the job database depending on the."""

        job_entry = JobEntry.objects.create(name=job_data['job_name'], mode=job_data['mode'],
                                            cron_string=job_data['cron_string'],
                                            command_ipynb=job_data['command_ipynb'])
        return job_entry


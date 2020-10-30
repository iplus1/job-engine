from main.models import JobEntry


class DBHelper:

    @staticmethod
    def get_jobs():
        return list(JobEntry.objects.values())

    @staticmethod
    def get_job_by_id(job_id):
        return JobEntry.objects.get(id=job_id)

    @staticmethod
    def get_all_jobs():
        return list(JobEntry.objects.filter(mode='cron').values())

    @staticmethod
    def delete_entry(job_id):
        try:
            JobEntry.objects.filter(id=job_id).delete()
        except Exception as e:
            print(e)
            return 'There has been an Error.'
        return 'Entry deleted.'

    @staticmethod
    def change_entry_status(job_id, job_status):
        JobEntry.objects.filter(id=job_id).update(status=job_status)
        return

    @staticmethod
    def create_entry(job):
        job_entry = JobEntry.objects.create(name=job.name, mode=job.mode, cron_string=job.cron_string, optional_params=job.optional_params)
        return job_entry


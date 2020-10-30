from main.internals.db_helper import DBHelper


class WebsiteHelper:

    @staticmethod
    def perform_action(job, action, job_id='New Job'):
        try:
            if action == 'create':
                DBHelper.create_entry(job)
                if job.mode == 'cron':
                    job.create_job()
                else:
                    job.create_cmd()

            elif action == 'delete':
                DBHelper.delete_entry(job_id)
                if job.mode == 'cron':
                    job.delete_job()

            return f'Performed action {action} on {job.name}'
        except Exception as e:
            print(e)
            return f'An Error occurred with {action} on {job.name}'


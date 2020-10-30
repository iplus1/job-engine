from django.utils import timezone
from crontab import CronTab


class Job:

    def __init__(self, name, mode, cron_string, optional_params, running=False, status=-1, date=timezone.now):
        self.name = name
        self.mode = mode
        self.optional_params = optional_params
        self.running = running
        self.status = status
        self.date = date

        if mode == 'cron':
            self.cron_string = cron_string
            self.cron = CronTab(user='root')
        else:
            self.cron_string = ''

    def create_job(self):
        job = self.cron.new(command=f'echo "hello world {self.name}" >> /usr/local/output.txt', comment=f'Identifier: {self.name}')
        job.setall(self.cron_string)
        self.cron.write()

    def create_cmd(self):
        cmd = f'echo "Hello world {self.name}" >> /usr/local/output.txt'

    def delete_job(self):
        job = self.cron.find_comment(f'Identifier: {self.name}')
        self.cron.remove(job)
        self.cron.write()


import glob
import ntpath
import os
import shutil
import signal
import subprocess
import psutil

from crontab import CronTab
from django.utils import timezone

BASE_DIR = '/jobengine'


class Job:

    def __init__(self, name, mode, cron_string, command, ipynb_file=''):
        """The Job class is responsible for all operations necessary to create, delete, start and stop a Job.

        Create the necessary Job directory if it doesnt exist.
        Create an instance of CronTab if the Job is a Cron-Job.

        Additional attributes:

        *self.job_dir*: specifies the directory of the Job.

        *self.job_file*: stores the name of the Job specific file.

        *self.cron*: stores the Job specific CronTab instance.

        *self.pid*: stores the PID.

        :param name: string: name of the Job.
        :param mode: string: specifies the mode of the Job (Expected: 'cmd', 'cron', 'cmd ipynb', 'cron ipynb')
        :param cron_string: string: specifies the interval for the Crontab. (Only relevant if 'mode' includes 'cron')
        :param command: string: command that the job should execute. (Only relevant if the 'mode' includes 'cmd')
        :param ipynb_file: string: ipynb file path. (optional)
        """

        self.name = name
        self.mode = mode
        self.command = command
        self.job_dir = f'{BASE_DIR}/jobs/{self.name}'
        self.pid = self.get_pid_name()
        self.ipynb_file = ipynb_file
        if not os.path.exists(self.job_dir):
            os.makedirs(self.job_dir)

        if 'cron' in mode:
            self.cron_string = cron_string
            self.cron = CronTab(user='root')
        else:
            self.cron_string = None
        if 'ipynb' in mode:
            self.job_file = ntpath.basename(self.ipynb_file)
            self.command = None
        else:
            self.ipynb_file = None

    def copy_ipynb_file(self):
        """Copy the source ipynb into the Job directory.

        To ensure that the user can still work on the source file while the Job is running,
        the function copies it into the Job directory.

        :return: Status of the copied file.
        :exception FileNotFoundError if source file doesnt exist.:
        """

        if os.path.isfile(self.ipynb_file):
            shutil.copy2(self.ipynb_file, f'{self.job_dir}/')
            return f'<b>{self.name}:</b> Job File is now in place.'
        else:
            raise FileNotFoundError(f'<b>{self.name}:</b> File was not found.')

    def create_cron(self):
        """Create an entry in the Crontab with the command of the Job.

        The CronTab places a unique Identifier with the Job name
        at the end of the Cronline as a comment.

        :return: Status of the started Cron-Job.
        """

        job = self.cron.new(command=self.build_command(), comment=f'Identifier: {self.name}')
        job.setall(self.cron_string)
        self.cron.write()
        return f'<b>{self.name}</b> has been started as a {self.mode}-job.'

    def create_ipynb_cron(self):
        """Create an entry in the Crontab with a command of the Job specific for ipynb.

        Copies the needed source file for the Job to the Job directory with `copy_ipynb_file()`.
        The CronTab places a unique Identifier with the Job name
        at the end of the Cronline as a comment.

        :return: Status of the started ipynb-Cron-Job
        """

        self.copy_ipynb_file()
        job = self.cron.new(command=self.build_command(),
                            comment=f'Identifier: {self.name}')
        job.setall(self.cron_string)
        self.cron.write()
        return f'<b>{self.name}</b> has been started as a {self.mode}-job.'

    def create_cmd(self):
        """Create a command for the Job and execute it.

        Checks if a process with the same PID is already running.

        :return: Status of the started cmd-Job.
        """

        if not self.check_if_running():
            command = self.build_command()
            subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            return f'<b>{self.name}:</b> has been started as a {self.mode}-job.'
        else:
            return f'<b>{self.name}:</b> is still running.'

    def create_ipynb_cmd(self):
        """Create a command for the Job specific for ipynb and execute it.

        Checks if a process with the same PID is already running.

        :return: Status of the started ipynb-cmd-Job.
        """

        if not self.check_if_running():
            self.copy_ipynb_file()
            subprocess.Popen(self.build_command(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
            return f'<b>{self.name}:</b> has been started as a {self.mode}-job.'
        else:
            return f'<b>{self.name}:</b> is still running.'

    def delete_cron(self):
        """Delete the Job specific Crontab entry.

        :return: Stratus of the Crontab entry deletion.
        """

        job = self.cron.find_comment(f'Identifier: {self.name}')
        self.cron.remove(job)
        self.cron.write()
        return f'<b>{self.name}:</b> The cron entry has been deleted.'

    def delete_job_dir(self):
        """Delete the Job directory.

        :return: Status of the directory deletion.
        :rtype: str
        """

        if os.path.exists(self.job_dir):
            shutil.rmtree(self.job_dir)
            return f'The Job Dir and Files for <b>{self.name}</b> have been deleted.'
        return f'<b>{self.name}:</b> No Job Dir found.'

    def cleanup_job_dir(self):
        """Clean the Job directory of all log files by deleting them.

        :return: Status of the directory cleaning.
        """

        if os.path.exists(self.job_dir):
            file_list = glob.glob(f'{self.job_dir}/{self.job_file}.*.html')
            for file in file_list:
                os.remove(file)
            return f'<b>{self.name}:</b> Job dir is now cleaned up.'
        else:
            return f'<b>{self.name}:</b> No Job Dir found.'

    def get_logs(self):
        """Get all log file names and append them to a list.

        :return: list containing all log file names or status of the fetching.
        """

        if os.path.exists(self.job_dir):
            path_list = glob.glob(f'{self.job_dir}/{self.job_file}.*.html')
            data = {'logs': []}
            for path in path_list:
                data['logs'].append(ntpath.basename(path))
            data['logs'].sort()
            return data
        else:
            return f'<b>{self.name}:</b> Job dir doesnt exist'

    def get_log(self, file):
        """Get a specific log file.

        Takes in the file name to search for and read in.

        :param file: string: name of the log file.
        :return: log file content.
        """

        file = f'{self.job_dir}/{file}'
        if os.path.exists(file):
            if file.endswith('.html'):
                try:
                    with open(file, 'r') as log:
                        out = log.read()
                    return out
                except Exception as e:
                    print(f'[{timezone.now()}] Server Error: {e}')
                    return f'[{timezone.now()}] Server Error: {e} with {self.name}'
        else:
            raise FileNotFoundError(f"File: {file} was not found.")

    def check_if_running(self):
        """Sends a signal 0 to the process at the Jobs PID.

        :return: True or False depending if the process exists.
        """

        if self.pid is not None:
            try:
                os.kill(self.pid, 0)
            except OSError:
                return False
            else:
                return True
        else:
            return False

    def get_pid_name(self):
        """Get the PID of a Job by its name.

        Use the psutil.process_iter() to get a list of all processes like ps auxw would.
        Join the command line arguments and search for the wrapper.sh string plus the Jobs name.

        :return: PID of the Job.
        """

        for p in psutil.process_iter():
            joined = " ".join(p.cmdline())
            if f'/jobengine/wrapper.sh "{self.name}"' in joined:
                return p.pid
        return None

    def kill_process(self):
        """Kill the parent process of the job and its children.

        A SIGTERM signal will be send to the children of the parent process and finally the parent process.

        :return: True of False depending if the process exists or not.
        """

        if self.pid is not None:
            assert self.pid != os.getpid()
            parent = psutil.Process(self.pid)
            process_list = parent.children(recursive=True)
            process_list.append(parent)
            for process in process_list:
                try:
                    print(f'Killing Process: {process.name()}')
                    process.send_signal(signal.SIGTERM)
                except psutil.NoSuchProcess:
                    print(f'[{timezone.now()}] Server Error: {psutil.NoSuchProcess}')
            gone, alive = psutil.wait_procs(process_list, timeout=3,
                                            callback=None)
            print(gone, alive)
            print(f'<b>{self.name}:</b> Job process should be killed.')
            return f'<b>{self.name}:</b> Job process should be killed.'
        else:
            return False

    def build_command(self):
        """Build a command specific to the mode of the Job.

        Every command has the following parts build into:

        *stats_code*: Stores the return code of the base command in a variable.

        *update_status*: Executes a custom Django command to update the database entry of the Job.

        At the start of every command comes the execution of the wrapper.sh script
        that handles the commands execution. As arguments it takes in the command and the Jobs name.

        Ipynb specifics:

        *nb_convert*: Uses the nbconvert tool of jupyter to convert the ipynb to html and execute it.

        *log_creation*: Uses the converted ipynb html format to create 'log files' with the output
        of the Notebook stored into it.

        *garbage_collector*: Makes sure the Job directory doesnt get too cluttered and deletes
        log files with a certain ruleset.

        Non Ipynb specifics:

        To ensure that the command gets properly executed by the Shell, we have to escape "'".

        :return: Finished build command.
        """

        status_code = fr'code=\$?'
        update_status = fr'/var/www/jobengine/venv/bin/python /var/www/jobengine/manage.py update_status \"{self.name}\" \$code \"end\"'
        if 'ipynb' in self.mode:
            if 'cmd' in self.mode:
                log_creation = f'cp {self.job_dir}/{self.job_file}.html {self.job_dir}/{self.job_file}.$(date +\%Y-\%m-\%d-\%H\%M\%S).html'
            else:
                log_creation = f'cp {self.job_dir}/{self.job_file}.html {self.job_dir}/{self.job_file}.$(date +\\\%Y-\\\%m-\\\%d-\\\%H\\\%M\\\%S).html'
            nb_convert = f'/opt/conda/bin/jupyter nbconvert --ExecutePreprocessor.timeout=None --to html --output {self.job_dir}/{self.job_file}.html --execute {self.job_dir}/{self.job_file}'
            base_command = f'{nb_convert} && {log_creation}'
            garbage_collector = f'find {self.job_dir}/{self.job_file}.*.html -mmin +30 -exec rm {{}} \\;'
            ipynb_command = f'{base_command} && {garbage_collector}'
            full_command = f'/jobengine/wrapper.sh "{self.name}" "{ipynb_command} ; {status_code} ; {update_status}"'
            return full_command
        else:
            escaped_command = self.command.replace('"', r'\"').replace('$', r'\$')
            full_command = f'/jobengine/wrapper.sh "{self.name}" "{escaped_command} ; {status_code} ; {update_status}"'
            return full_command


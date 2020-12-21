#### Description

Jobengine is a container application that helps the user to create and manage jobs that can perform tasks on the container or a cluster.

The container uses Django as a web-framework to present the user a simplistic and easy to use frontend that displays all relevant information for the jobs in a table. 

The user is able to create jobs through a form in the frontend that includes various options for different modes the jobs can run in.

To give the user the ability to execute tasks for the container on startup, the jobengine checks if a script named ``pre_conditions.sh`` exists and executes it.
This script is optional and will only run once when the container is started.

#### Modes

The Jobengine can execute commands or ipynbs like you would do it in Shell or in an interval through Crontab. We therefore differentiate between four modes: 

    cmd        : Run a command once like a normal shell command.
    cron       : Run a command in a defined interval through Cron.
    ipynb      : Run a converted ipynb once through the shell.
    cron ipynb : Run a converted ipynb in a defined interval through Cron.

#### Install

1. Mounting volumes to persist data:
    1. Database for the jobs:     ``/your/db/directory:/jobengine/db``
    2. Source ipynbs: ``/your/jupyter/directory:/jobengine/ipynbs``
    3. Job ipynbs:    ``/your/job/directory:/jobengine/jobs``
    
3. **(Optional)** Pre conditions script:
    1. Add a script named ``pre_conditions.sh`` in the ``/`` of the container.

#### Example Dockerfile

````shell script
$ docker run --name some-jobengine -v /your/db/directory:/jobengine/db -v /your/jupyter/directory:/jobengine/ipynbs -v /your/job/directory:/jobengine/jobs iplus1/job-engine:0.0.1
````



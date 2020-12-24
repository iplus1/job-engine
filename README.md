## Description

Jobengine is an open-source docker container that helps you to easily create, manage and schedule jobs.

#### Features:
- Provides a web-based User-Interface.
- Can execute shell-commands and custom scripts.
- Uses Cron to schedule jobs on the container. 
- Displays the status, output and logs of a job.
- Contains all necessary libs and packages to convert and run ipynbs.

## Quickstart

````shell script
$ docker run --name=my-jobengine -p 8010:8010 iplus1/job-engine:0.0.3
````

Additional arguments:

  |Argument|Desciption|
  |---|---|
  |``-v /your/db/directory:/jobengine/db`` | Mount a database volume to persist the database containing the jobs. <br/> Helps to preserve saved jobs.|
  |``-v /your/jupyter/directory:/jobengine/ipynbs``| Mount a volume that includes ipynbs that can be used to create jobs. <br/> The jobengine will use this directory to look for suitable ipynbs to execute.|
  |``-v /your/job/directory:/jobengine/jobs``| The Jobengine makes a job directory for every job created through the engine. <br/> Log files, the last output and the possible executed ipynb that are stored in it <br/> can be persisted by mounting a volume.|
  |``-v /path/to/pre_conditions.sh:/pre_conditions.sh``| On startup the Jobengine container checks if the pre_conditions.sh script exists <br/> and if so executes it. This gives the user the ability to perform certain tasks <br/> that have to run before the jobengine is finished starting. |
  |``-v /path/to/custom/script.sh:/usr/local/bin/script.sh``| It is also possible to mount your own scripts into the PATH of the Jobengine <br/> container, which allows for an ease of use by just calling it as a command. |

After successfully starting the container you can access the user-interface by opening it in your browser. http://localhost:8010/ 

## UI

#### Job table:

![example job table](png/example_filled_table.png)

#### Create-job menu:

![example job creation](png/example_job_creat.png)

#### Example job output:

![example job output](png/example_output.png)

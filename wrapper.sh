#!/bin/bash
#set -eo pipefail

source /common

export PATH="/opt/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/jobengine/scripts"

PID=$1
CMD=$2
CMD_SEP=$3

number_occur=$(ps auxww | grep -v "grep" | grep -o "/jobengine/wrapper.sh \"${PID}\" " | wc -l)

if [ ${number_occur} -ge 2 ]; then
    error "Skipping execution. Already running (found '${number_occur}' for '${PID}') ..."
else
    bash -c "/var/www/jobengine/venv/bin/python /var/www/jobengine/manage.py update_status '${PID}' -1 'start'"
    echo "Job Command: ${CMD_SEP}" > /jobengine/jobs/"${PID}"/last_output
    eval ${CMD} >> /jobengine/jobs/"${PID}"/last_output 2>&1
fi



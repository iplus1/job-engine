#!/bin/bash
#set -eo pipefail

source /common

CMD=$2
PNAME=$1
ALLELSE=$@

number_occur=$(ps auxww | grep -v "grep" | grep -o "/jobengine/wrapper.sh \"${PNAME}\" " | wc -l)

if [ ${number_occur} -ge 2 ]; then
    error "Skipping execution. Already running (found '${number_occur}' for '${PNAME}') ..." >> /jobengine/out
else
    bash -c "/var/www/jobengine/venv/bin/python /var/www/jobengine/manage.py update_status '${PNAME}' -1 'start'"
    eval ${CMD} > /jobengine/jobs/"${PNAME}"/last_output 2>&1
fi


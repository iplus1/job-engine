#!/bin/bash
#set -eo pipefail

source /common

CMD=$2
PNAME=$1
ALLELSE=$@
echo "Pre Grep: PNAME=${PNAME} CMD=${CMD}" >> /jobengine/out

echo "All Arguments for ${PNAME}: ${ALLELSE}" >> /jobengine/out

number_occur=$(ps auxww | grep -v "grep" | grep -o "/jobengine/wrapper.sh '${PNAME}' " | wc -l)

echo "Post Grep: PNAME=${PNAME} , number=${number_occur}" >> /jobengine/out

if [ ${number_occur} -ge 2 ]; then
    error "Skipping execution. Already running (found '${number_occur}' for '${PNAME}') ..." >> /jobengine/out
else
    bash -c "/var/www/jobengine/venv/bin/python /var/www/jobengine/manage.py update_status '${PNAME}' -1 'start'"
    eval ${CMD} > /jobengine/jobs/${PNAME}/last_output 2>&1
fi


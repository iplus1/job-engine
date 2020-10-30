#!/bin/bash
set -e
set -o pipefail

info() {
    local L_MSG=$1
    TIMESTAMP=$(date +"[%Y-%m-%d %H:%M:%S]")
    if [ "${L_MSG:0:1}" != '[' ]; then
        L_MSG=" ${L_MSG}"
    fi
    echo "${TIMESTAMP}[INFO][$(basename "$0")]${L_MSG}"
}

DBDIR=/glusterfs/test-max/jobengine
DBFILE=${DBDIR}/jobengine.sqlite3

info "Check if Pre Conditions exist."
if [ -f /pre_conditions.sh  ]; then
    info "Pre Conditions exist."
    . /pre_conditions.sh
fi

mkdir -p ${DBDIR}

# Give Django a fresh secret if it lacks one.
SECRET="$(pwgen 70 1 | tr -d '\n')"
sed -i "s/^#SECRET_KEY = .*$/SECRET_KEY = '$SECRET'/" /var/www/jobengine/jobengine/settings.py

sed -i "s#___DBFILE___#$DBFILE#" /var/www/jobengine/jobengine/settings.py

cd /var/www/jobengine/
source activate ./venv 

info "Make migrations"
bash -c "python manage.py makemigrations && python manage.py migrate --run-syncdb --no-input"

info "Collecting static files."
bash -c "python manage.py collectstatic --no-input"

info "Starting Cron"
service cron restart

info "Restarting jobs from database."
bash -c "python manage.py reactivate_jobs"

/var/www/jobengine/venv/bin/uwsgi --chdir=/var/www/jobengine/ \
    --module=jobengine.wsgi:application \
    --env DJANGO_SETTINGS_MODULE=jobengine.settings \
    --master --pidfile=/tmp/project-master.pid \
    --touch-reload /var/www/jobengine/jobengine/settings.py \
    --http :8010 \
    --processes=5 \
    --harakiri=60 \
    --max-requests=32768 \
    --home=/var/www/jobengine/venv \
    --buffer-size=65535 \
    --static-map /static=/var/www/jobengine/static \

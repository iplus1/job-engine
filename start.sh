#!/bin/bash
set -e
set -o pipefail

source /common

printenv > /etc/environment

DBDIR=/jobengine/db
DBFILE=${DBDIR}/jobengine.sqlite3

info "Check if Pre Conditions exist."
if [ -f /pre_conditions.sh  ]; then
    info "Pre Conditions exist."
    /pre_conditions.sh
fi

mkdir -p ${DBDIR}

# Give Django a fresh secret if it lacks one.
SECRET="$(pwgen 70 1 | tr -d '\n')"
sed -i "s/^#SECRET_KEY = .*$/SECRET_KEY = '$SECRET'/" /var/www/jobengine/jobengine/settings.py

sed -i "s#___DBFILE___#$DBFILE#" /var/www/jobengine/jobengine/settings.py

info "Check if scripts directory is mounted..."
if [ -d /jobengine/scripts/ ]; then
    chmod +x /jobengine/scripts/*.sh
else
    info "No scripts directory mounted."
fi

cd /var/www/jobengine/

info "Make migrations"
venv/bin/python manage.py makemigrations && venv/bin/python manage.py migrate --no-input

info "Collecting static files."
venv/bin/python manage.py collectstatic --no-input

info "Starting Cron"
service cron restart

info "Looking for jobs to migrate..."
venv/bin/python manage.py migrate_data

info "Looking for jobs to restart..."
venv/bin/python manage.py reactivate_jobs

info "Starting the update process..."
/jobengine/update_job_states.sh > /dev/null &

venv/bin/uwsgi --chdir=/var/www/jobengine/ \
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
    --static-map /jobengine/static=/var/www/jobengine/static \

#!/bin/bash
set -e
set -o pipefail

source /common

printenv > /etc/environment

make_scripts_executable(){
    info "Check if $1 directory is mounted..."
    if [ -d /jobengine/$1/ ]; then
        shopt -s nullglob dotglob
        files=(/jobengine/$1/*.sh)
        if [ ${#files[@]} -gt 0 ]; then
            chmod +x /jobengine/$1/*.sh
            info "$1 in directory should now be executable."
            if [ $1 == "startup-scripts" ]; then
		for script in $STARTUP_SCRIPTS/*.sh; do
                    info "Executing script: $script"
                    $script
                done
            fi
        else
            info "No scripts in the directory."
        fi
    else
        info "No scripts directory mounted."
    fi
}

DBDIR=/jobengine/db
DBFILE=${DBDIR}/jobengine.sqlite3
STARTUP_SCRIPTS=/jobengine/startup-scripts

info "Check if Pre Conditions exist."
if [ -f /pre_conditions.sh  ]; then
    info "Pre Conditions exist."
    /pre_conditions.sh
fi

make_scripts_executable "runtime-scripts"
make_scripts_executable "startup-scripts"

mkdir -p ${DBDIR}

# Give Django a fresh secret if it lacks one.
SECRET="$(pwgen 70 1 | tr -d '\n')"
sed -i "s/^#SECRET_KEY = .*$/SECRET_KEY = '$SECRET'/" /var/www/jobengine/jobengine/settings.py

sed -i "s#___DBFILE___#$DBFILE#" /var/www/jobengine/jobengine/settings.py

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

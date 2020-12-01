#!/bin/bash

source /common

cd /var/www/jobengine

while true; do
    venv/bin/python manage.py update_processes
    sleep 2
done


#!/usr/bin/bash

set -eu

# collect static files to backend_static
./manage.py collectstatic --no-input

if [ "$BACKEND_DEBUG" = "True" ]; then
    python manage.py runserver 0.0.0.0:8000
else
    gunicorn org.conf.wsgi:application --bind 0.0.0.0:8000 --access-logfile=- --error-logfile=- --capture-output --log-level=info
fi

#!/usr/bin/env bash

set -e

RUN_MANAGE_PY='python3 -m tracksales.manage'

echo 'Collecting static files...'
$RUN_MANAGE_PY collectstatic --no-input

echo 'Running migrations...'
$RUN_MANAGE_PY migrate --no-input

exec gunicorn -c gunicorn.py.ini tracksales.config.wsgi

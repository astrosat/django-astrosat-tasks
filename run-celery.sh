#!/bin/bash
set -euo pipefail

cd $APP_HOME/example

exec /sbin/setuser app \
    pipenv run celery \
    --app=astrosat_tasks.celery:app worker \
    --loglevel=INFO \
    -n worker.%%h

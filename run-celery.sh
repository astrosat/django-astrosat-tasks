#!/bin/bash
set -euo pipefail

cd $APP_HOME/example

# TODO: run beat separately for deployments

exec /sbin/setuser app \
    pipenv run celery \
    --app=astrosat_tasks.celery:app worker \
    --beat --scheduler django_celery_beat.schedulers.DatabaseScheduler \
    --loglevel=INFO \
    -n worker.%%h

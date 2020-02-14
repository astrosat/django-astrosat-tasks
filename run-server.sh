#!/bin/bash
set -euo pipefail

until echo > /dev/tcp/db/5432; do sleep 1; done

cd $APP_HOME

setuser app pipenv run ./example/manage.py migrate
# setuser app pipenv run ./example/manage.py collectstatic --no-input --link

exec /sbin/setuser app pipenv run ./example/manage.py runserver 0.0.0.0:8000

#!/usr/bin/env bash

set -e;

APP_GUNICORN_USE=${APP_GUNICORN_USE:-"sibdev_test.wsgi:application"}
APP_GUNICORN_MAX_REQUESTS=${APP_GUNICORN_MAX_REQUESTS:-"1000"}

APP_GUNICORN_WORKERS_DEFAULT=$(nproc)
APP_GUNICORN_WORKERS=${APP_GUNICORN_WORKERS:-$APP_GUNICORN_WORKERS_DEFAULT}

APP_HOST=${APP_HOST:-"0.0.0.0"}
APP_PORT=${APP_PORT:-"8000"}

if ! [ -z "$APP_MIGRATE" ]; then
  django-admin migrate --noinput
  django-admin createcachetable
fi

if ! [ -z "$APP_COLLECTSTATIC" ]; then
  django-admin collectstatic --noinput
fi

if ! [ -z "$APP_COMMAND" ]; then
  django-admin $APP_COMMAND
  exit
fi

if ! [ -z "$APP_CELERY" ]; then
  rm -f /tmp/celeryd.pid || true
  celery $APP_CELERY
  exit
fi

if ! [ -z "$APP_CREATE_SUPERUSER" ]; then
  echo "from django.contrib.auth import get_user_model; User = get_user_model(); bool(User.objects.filter(email='admin@mail.ru').count()) or User.objects.create_superuser('admin@mail.ru', 'admin')" | django-admin shell
fi

if ! [ -z "$APP_FIXTURES" ]; then
  django-admin loaddata $APP_FIXTURES
fi


if ! [ -z "$APP_DEBUG" ]; then
  django-admin runserver ${APP_HOST}:${APP_PORT}
else
  gunicorn -b ${APP_HOST}:${APP_PORT} --capture-output --max-requests $APP_GUNICORN_MAX_REQUESTS -w $APP_GUNICORN_WORKERS -k gevent $APP_GUNICORN_USE
fi
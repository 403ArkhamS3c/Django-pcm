#!/bin/sh
set -eu

if [ -z "${SECRET_KEY:-}" ] && [ "${GENERATE_SECRET_KEY:-False}" = "True" ]; then
    SECRET_KEY="$(uv run --no-sync python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
    export SECRET_KEY
fi

uv run --no-sync python manage.py migrate
exec uv run --no-sync gunicorn config.wsgi:application --bind "0.0.0.0:${PORT:-8000}" --workers 3

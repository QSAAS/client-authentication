#!/bin/sh

set -e
#
#. /venv/bin/activate

exec "$@"
#exec gunicorn --bind 0.0.0.0:5000 --forwarded-allow-ips='*' wsgi:app

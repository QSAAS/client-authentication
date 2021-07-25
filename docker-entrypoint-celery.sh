#!/bin/bash

cd /app

/app/.venv/bin/celery -A config worker --concurrency=10 -l warning --beat

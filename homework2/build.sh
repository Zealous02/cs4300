#!/usr/bin/env bash
# Render build script: install deps, collect static files, migrate, seed sample data.
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py seed_data

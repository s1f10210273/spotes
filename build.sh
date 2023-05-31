#!/usr/bin/env bash
# exit on error
set -o errexit
python manage.py makemigrations
python manage.py migrate

pip install -r requirements.txt
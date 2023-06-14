#!/usr/bin/env bash
python manage.py makemigrations
python manage.py migrate
python manage.py seed_db
python manage.py collectstatic --noinput

python manage.py runserver 0.0.0.0:8000
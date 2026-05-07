#!/usr/bin/env bash

set -o errexit  # error হলে script stop করবে

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Installed packages:"
pip list   # debug: gunicorn install হয়েছে কিনা দেখাবে

echo "Running collectstatic..."
python manage.py collectstatic --noinput

echo "Applying migrations..."
python manage.py migrate
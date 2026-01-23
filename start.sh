#!/bin/bash
set -e

# Fallback to 8000 if PORT is not set
APP_PORT="${PORT:-8000}"

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn on port $APP_PORT..."
# Using the variable directly ensures the shell replaces it with the number
exec gunicorn config.wsgi:application --bind 0.0.0.0:"$APP_PORT" --workers 2 --timeout 120
#!/bin/bash
set -e

# Use a local variable to ensure expansion happens correctly
APP_PORT=${PORT:-8000}

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn on port $APP_PORT..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:$APP_PORT --workers 2 --timeout 120
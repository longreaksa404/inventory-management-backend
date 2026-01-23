FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy project files
COPY . .

# Expose the port (optional, but good practice)
EXPOSE 8000

# Use shell form to allow $PORT substitution
CMD python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
# Use official slim Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies including gunicorn
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy project files
COPY . .

# Temporary environment variables for build-time (won't affect Railway runtime)
ENV SECRET_KEY=temporarydummykey1234567890
ENV DATABASE_URL=postgres://user:password@localhost:5432/dbname
ENV REDIS_URL=redis://localhost:6379/0

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port (optional, Railway maps automatically)
EXPOSE 8000

# Run the Django app with Gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]

# Use slim Python 3.12 image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies for PostgreSQL & building packages
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Temporary environment variables for build-time only
# These are needed so Django collectstatic runs successfully
ENV SECRET_KEY=temporarydummykey1234567890
ENV DATABASE_URL=postgres://user:password@localhost:5432/dbname

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port (optional, Railway will map automatically)
EXPOSE 8000

# Run the app using Gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]

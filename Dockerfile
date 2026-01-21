FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Temporary build-time env vars
ENV SECRET_KEY=temporarydummykey1234567890
ENV DATABASE_URL=postgres://user:password@localhost:5432/dbname
ENV REDIS_URL=redis://localhost:6379/0

# Collect static files
RUN python manage.py collectstatic --noinput

# Run server
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]

# Backend Dockerfile for Django Ninja
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /app/

# Make entrypoint script executable
RUN chmod +x /app/docker-entrypoint.sh

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Use entrypoint script
ENTRYPOINT ["/app/docker-entrypoint.sh"]

#!/bin/bash

# Script to run Django Backend

echo "🦞 Starting Seafood Backend..."

# Activate virtual environment if exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Run migrations
echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

# Start server
echo "Starting Django server at http://localhost:8000"
echo "API Docs: http://localhost:8000/api/docs"
python manage.py runserver

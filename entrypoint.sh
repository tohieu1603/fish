#!/bin/sh

echo "🦞 Starting Seafood Backend Setup..."

# Wait for PostgreSQL
echo "Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "✅ PostgreSQL started"

# Run migrations
echo "📦 Running migrations..."
python manage.py makemigrations
python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput || true

# Create superuser if not exists (optional)
echo "👤 Creating superuser (if needed)..."
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123');
    print('Superuser created: admin/admin123');
else:
    print('Superuser already exists');
" || true

echo "🚀 Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000

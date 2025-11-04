#!/bin/sh

echo "🦞 Starting Seafood Backend..."

# Wait for PostgreSQL
echo "⏳ Waiting for PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "✅ PostgreSQL is ready!"

# Run migrations
echo "📦 Creating migrations..."
python manage.py makemigrations --noinput

echo "📦 Running migrations..."
python manage.py migrate --noinput

# Create superuser if not exists
echo "👤 Creating superuser..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('✅ Superuser created: admin/admin123')
else:
    print('✅ Superuser already exists')
END

echo "🚀 Starting Django server..."
exec python manage.py runserver 0.0.0.0:8000

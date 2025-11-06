#!/bin/bash
# Script to reset and recreate all migrations as a single initial migration

echo "🗑️  Step 1: Removing all migration files..."
find apps/*/migrations -name "*.py" ! -name "__init__.py" -type f -delete
echo "✅ Migration files deleted"

echo ""
echo "🔄 Step 2: Creating fresh initial migrations..."
python manage.py makemigrations
echo "✅ Fresh migrations created"

echo ""
echo "📊 Step 3: Showing migration status..."
python manage.py showmigrations

echo ""
echo "✅ Done! You can now run: python manage.py migrate"

"""URL configuration for Seafood Order Management System."""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from api.main import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]

# Serve media files (both development and production)
# Note: For better performance in production, use nginx/apache to serve static/media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

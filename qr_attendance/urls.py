from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from attendance.views import home  # Import 'home' for root URL

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin site
    path('attendance/', include('attendance.urls', namespace='attendance')),  # Include the attendance app URLs here
    path('', home, name='home'),  # Home page for employees at the root path
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

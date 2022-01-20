from django.contrib import admin
from django.urls import path, include

from app.urls import url_patterns as app_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(app_urls))
]

from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

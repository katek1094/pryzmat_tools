from django.contrib import admin
from django.urls import path, include

from app.urls import url_patterns as app_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(app_urls))
]

from django.contrib import admin
from django.urls import path, include

from testapp.urls import url_patterns as testapp_urls
from app.urls import url_patterns as app_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', include(testapp_urls)),
    path('', include(app_urls))
]

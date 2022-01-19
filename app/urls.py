from django.urls import path

from .views import home

url_patterns = [
    path('', home, name='home')
]

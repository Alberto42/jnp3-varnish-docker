"""www_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from a.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',string_hash_searcher, name="start"),
    path('compute_hash', brute_force_hash_sync, name="brute_force_hash_sync"),
    path('request_hash', brute_force_hash_async, name="brute_force_hash_async"),
    path('hash_query', hash_query, name="hash_query"),
]

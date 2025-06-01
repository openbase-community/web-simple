"""
URL configuration for web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

import json
import os

from django.contrib import admin
from django.urls import include, path

from config.app_packages import get_package_apps

urlpatterns = [
    path("admin/", admin.site.urls),
]

url_prefixes = json.loads(os.environ.get("URL_PREFIXES", "{}"))

for app in get_package_apps():
    try:
        prefix = url_prefixes[app].rstrip("/") + "/" if app in url_prefixes else "api/"
        urlpatterns.append(path(prefix, include(f"{app}.urls")))
    except (ImportError, ModuleNotFoundError) as e:
        print(f"Error importing {app}.urls: {e}")
        raise e

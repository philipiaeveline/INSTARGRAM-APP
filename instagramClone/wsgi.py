"""
WSGI config for instagramClone project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.conf.urls import url,include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^instagram/',include('instagram.urls'))
]

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'instagramClone.settings')

application = get_wsgi_application()

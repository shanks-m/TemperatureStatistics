"""
WSGI config for TemperatureStatistics project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TemperatureStatistics.settings')
sys.path.append('/var/www/html/django/TemperatureStatistics')
application = get_wsgi_application()


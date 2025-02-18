"""
WSGI config for reclaim project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise  # WhiteNoiseを利用して静的ファイルを効率的に配信

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reclaim.settings')

application = get_wsgi_application()
# WhiteNoiseでWSGIアプリケーションをラップし、静的ファイルの配信を行えるようにする
application = WhiteNoise(application, root=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static'))

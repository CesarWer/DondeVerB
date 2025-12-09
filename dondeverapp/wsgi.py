import os
from pathlib import Path
from django.core.wsgi import get_wsgi_application

# If DJANGO_SETTINGS_MODULE isn't set, infer from this package's folder name
if 'DJANGO_SETTINGS_MODULE' not in os.environ:
	pkg_name = Path(__file__).resolve().parent.name
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{pkg_name}.settings')

application = get_wsgi_application()


import os
import sys

import django

# Initialize Django
print('Initializing Django...')
my_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(my_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'history.settings')
django.setup()


# from history import settings
# from django.db import transaction
# from django.contrib.auth.models import Permission, Group
# from django.contrib.contenttypes.models import ContentType
from sources.models import Citation, Source

for s in Source.objects.all():
    if getattr(s, 'edition_number', None):
        s.edition_number = None
        s.save()


Citation.objects.all().delete()

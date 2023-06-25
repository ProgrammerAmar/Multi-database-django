from django.conf import settings
from django.db import connections


def set_dynamic_database(database_name):
    # Create a new dictionary based on the existing DATABASES setting
    connections.close_all()
    connections.databases['default'] = connections.databases[database_name]


# Handle Django 3.0/3.1 compatiblity
try:
    from django.db.models import JSONField  # noqa: F401
except ImportError:
    from django.contrib.postgres.fields import JSONField  # noqa: F401

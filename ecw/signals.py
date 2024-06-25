# signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.apps import apps
from .models import *

@receiver(post_save)
def log_create_update(sender, instance, created, **kwargs):
    if sender == AuditLog:
        return  # Prevent logging for AuditLog model itself

    user = None
    # Assuming you have request user in the context, this can be improved by using a middleware to set the user.
    # Here we use a simple method to get the user from the instance if possible
    if hasattr(instance, 'user'):
        user = instance.user

    action = 'CREATE' if created else 'UPDATE'
    AuditLog.objects.create(
        user=user,
        action=action,
        model_name=sender.__name__,
        object_id=instance.pk,
        changes=str(instance.__dict__),  # Optionally store changes
    )

@receiver(post_delete)
def log_delete(sender, instance, **kwargs):
    if sender == AuditLog:
        return  # Prevent logging for AuditLog model itself

    user = None
    if hasattr(instance, 'user'):
        user = instance.user

    AuditLog.objects.create(
        user=user,
        action='DELETE',
        model_name=sender.__name__,
        object_id=instance.pk,
    )

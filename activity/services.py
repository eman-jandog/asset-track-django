from django.db.models.signals import post_save
from django.dispatch import receiver

from activity.services import log_activity
from .models import Asset


@receiver(post_save, sender=Asset)
def asset_created(sender, instance, created, **kwargs):
    if not created:
        return

    log_activity(
        type="asset",
        action="created",
        message=f"New asset added: {instance.name}",
        obj=instance
    )

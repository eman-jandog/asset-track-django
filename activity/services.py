from .models import Activity

def log_activity(
    *,
    type: str,
    msg: str,
    action: str,
    message: str,
    user=None,
    obj=None
):
    Activity.objects.create(
        type=type,
        action=action,
        message=msg,
        user=user,
        related_object_id=getattr(obj, "id", None),
        related_object_type=obj.__class__.__name__ if obj else None
    )
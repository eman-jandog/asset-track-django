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
        relate_obj_name = getattr(obj, "name", None),
        related_object_serial= getattr(obj, "sn", None)
        # related_object_id=getattr(obj, "id", None),
        # related_object_nam=obj.__class__.__name__ if obj else None
    )
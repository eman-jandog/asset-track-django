from django.db.models import F, ExpressionWrapper, DurationField
from django.db.models.functions import Now
from django.shortcuts import get_object_or_404
from datetime import timedelta
from .models import Activity

def get_recent_activities(limit=5, user=None):
    print(user)
    activity_qs = get_object_or_404(Activity, user=user)
    activities_qs = Activity.objects.filter(user=user)[:limit]
    activities_qs = activities_qs.annotate(
        last_activity=ExpressionWrapper(
                Now() - F("created_at"), 
                output_field=DurationField()
            )
        )
    activities = activities_qs.values("action", "message", "user", "related_obj_name", "related_obj_sn")

    return activities
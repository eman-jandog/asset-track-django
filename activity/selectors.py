from django.db.models import F, ExpressionWrapper, DurationField
from django.db.models.functions import Now
from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from datetime import timedelta
from .models import Activity

def get_recent_activities(limit=5, user=None):

    activities = Activity.objects.all()[:limit]

    if activities is None:
        return

    for activity in activities:
        activity.time_since = now() - activity.created_at

    return activities
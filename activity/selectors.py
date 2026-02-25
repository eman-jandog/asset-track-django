from django.db.models import F, ExpressionWrapper, DurationField
from django.db.models.functions import Now
from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from .models import Activity
import humanize, datetime

def get_recent_activities(limit=5, user=None):

    activities = Activity.objects.all()[:limit]

    if activities is None:
        return

    for activity in activities:
        time_difference = now() - activity.created_at
        if time_difference < datetime.timedelta(days=1):
            convert_time = humanize.naturaltime(time_difference)
            actual_time = str(convert_time).replace('from now', '')
        else:
            convert_time = humanize.naturalday(time_difference)
            actual_time = convert_time.split(",")[0]

        activity.time_since = actual_time

    return activities
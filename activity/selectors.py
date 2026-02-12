from .models import Activity

def get_recent_activities(limit=5):
    return Activity.objects.all()[:limit]
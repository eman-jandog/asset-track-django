from datetime import datetime
from .models import Activity
from dashboard.models import Asset

def get_recent_activities(limit=5):
    activities_qs = Asset.objects.all()[:limit]
    ''' 
        action = activity.action
        message = activity.message
        item = activiy.obj.name
        obj.sn = activity.obj.sn
        date = datenow - activity.create_at
    ''' 

    return Asset.objects.all()[:limit]
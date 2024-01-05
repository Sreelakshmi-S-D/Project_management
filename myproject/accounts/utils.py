
from accounts.models import UserActivityLog



def log_user_action(user, action):
    from datetime import datetime
    date=datetime.now().strftime("%Y-%m-%d %H:%M")
    UserActivityLog.objects.create(user=user, action=action,timestamp=date)
    
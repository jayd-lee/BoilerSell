from .models import User

def top_users(request):
    users = User.objects.all()[:10]
    return { 'users': users }
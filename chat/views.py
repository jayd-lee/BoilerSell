from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from blog.models import Post
# Create your views here.
from .models import Thread

@csrf_exempt
@login_required
def messages_page(request):

    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('-timestamp')
    context = {
        'Threads': threads
    }

    if request.method == 'POST':
        # Get the author id from the form data
        author_id = request.POST.get('author_id')
        
        # Query the database to see if a thread exists between the logged-in user and the author
        thread = Thread.objects.by_user(user=request.user, other_person_id=author_id).first()
        
        # If no thread exists, create a new thread
        if thread is None:
            author = User.objects.get(id=author_id)
            thread = Thread.objects.create(first_person=request.user, second_person=author)
        
        # Add the thread to the context
        context['Thread'] = thread

    return render(request, 'chat/messages.html', context)
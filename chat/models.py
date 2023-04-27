from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q
from blog.views import Post
User = get_user_model()

# Create your models here.

class ThreadManager(models.Manager):
    def by_user(self, user, other_person_id=None):
        lookup = Q(first_person=user) | Q(second_person=user)
        if other_person_id:
            lookup &= Q(first_person=other_person_id) | Q(second_person=other_person_id)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs


class Thread(models.Model):
    first_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_first_person')
    second_person = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='thread_second_person')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    objects = ThreadManager()
    class Meta:
        unique_together = ['first_person', 'second_person']


class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.CASCADE, related_name='chatmessage_thread')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
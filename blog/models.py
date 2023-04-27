from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Category(models.Model): 
    name = models.CharField(max_length=255) 

    class Meta: 
        ordering = ('name',) 
        verbose_name_plural ='Categories' 

    def __str__(self): 
        return self.name

class Post(models.Model):
    
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    title = models.CharField(max_length = 90)
    image = models.FileField(blank=True)
    content = models.TextField()
    price = models.IntegerField()
    is_sold = models.BooleanField(default = False)
    date_posted = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete = models.CASCADE)


    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('post-detail', kwargs= {'pk': self.pk})



class PostImage(models.Model):
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
    image = models.FileField(upload_to='item_images', default='default.png', blank=True, null = True)

    def __str__(self):
        return self.post.title
    
from django.contrib import admin
from .models import Post, Category
# Register your models here.
from django.contrib import admin

from .models import Post, PostImage, Category

admin.site.register(Category)

class PostImageAdmin(admin.StackedInline):
    model = PostImage

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageAdmin]

    class Meta:
       model = Post

@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    pass
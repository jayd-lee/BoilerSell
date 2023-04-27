from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse_lazy

from django.views.generic import (
                            ListView, 
                            DetailView, 
                            CreateView,
                            UpdateView,
                            DeleteView
                            )
from .models import Post, Category, PostImage

def search(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    posts = Post.objects.filter(is_sold=False)

    if category_id:
        posts = posts.filter(category_id=category_id)

    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))

    return render(request, 'blog/sidebar/search.html', {
        'posts': posts,
        'query': query,
        'categories': categories,
        'category_id': int(category_id)
    })

class PostListView(ListView):
    model = Post
    template_name ='blog/shop.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = context['posts']

        for post in posts:
            cover_image = PostImage.objects.filter(post=post).first()
            post.cover_image = cover_image

        return context
    

    
    

class MarketListView(ListView):
    model = Post
    template_name ='blog/sidebar/market.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.filter(name__in=['Textbook', 'category2', 'category3'])
        context['categories'] = categories
        return context

class TicketListView(ListView):
    model = Post
    template_name ='blog/sidebar/ticket.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 9

class RideListView(ListView):
    model = Post
    template_name ='blog/sidebar/rideshare.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 9

class SubListView(ListView):
    model = Post
    template_name ='blog/sidebar/sublease.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 9

class FavListView(ListView):
    model = Post
    template_name ='blog/sidebar/fav.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 9

class SettingsListView(ListView):
    model = Post
    template_name ='blog/sidebar/settings.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 9






class UserPostListView(ListView):
    model = Post
    template_name ='blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')



def about(request):
    return render(request, 'blog/about.html')


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        photos = PostImage.objects.filter(post=post)
        related = Post.objects.filter(category=post.category, is_sold=False).exclude(pk=post.pk)
        context['photos'] = photos
        context['related'] = related
        return context



class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url ='/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False




def create_post_view(request):
    if request.method == 'POST':
        length = request.POST.get('length')
        title = request.POST.get('title')
        content = request.POST.get('content')
        price = request.POST.get('price')
        category = request.POST.get('category')

        post = Post.objects.create(
            title=title,
            content=content,
            price=price,
            category=Category.objects.get(id=category),
            author=request.user 
        )

        for image in request.FILES.getlist('images[]'):
            PostImage.objects.create(
                post=post,
                image=image
            )

        return redirect('/')

    categories = Category.objects.all()
    return render(request, 'blog/post_form.html', {'categories': categories})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'price', 'category']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
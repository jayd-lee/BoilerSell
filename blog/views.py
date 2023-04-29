from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
    ordering = ['is_sold', '-date_posted']
    paginate_by = 12

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
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(category__name='items')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = context['posts']

        for post in posts:
            cover_image = PostImage.objects.filter(post=post).first()
            post.cover_image = cover_image

        return context


class TicketListView(ListView):
    model = Post
    template_name ='blog/sidebar/ticket.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(category__name='Tickets')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = context['posts']

        for post in posts:
            cover_image = PostImage.objects.filter(post=post).first()
            post.cover_image = cover_image

        return context

class RideListView(ListView):
    model = Post
    template_name ='blog/sidebar/rideshare.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(category__name='RideShare')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = context['posts']

        for post in posts:
            cover_image = PostImage.objects.filter(post=post).first()
            post.cover_image = cover_image

        return context

class SubListView(ListView):
    model = Post
    template_name ='blog/sidebar/sublease.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(category__name='Sublease')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = context['posts']

        for post in posts:
            cover_image = PostImage.objects.filter(post=post).first()
            post.cover_image = cover_image

        return context

class FavListView(ListView):
    model = Post
    template_name ='blog/sidebar/fav.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        # filter queryset to only include posts created by the current user
        queryset = queryset.filter(author=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = context['posts']

        for post in posts:
            cover_image = PostImage.objects.filter(post=post).first()
            post.cover_image = cover_image

        return context




class SettingsListView(ListView):
    model = Post
    template_name ='blog/sidebar/settings.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 12






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
    template_name ='blog/post_confirm_delete.html'


    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



@login_required
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


def update_view(request, pk, status):
    post = get_object_or_404(Post, pk=pk)

    # Check if the current user is the author of the post
    if request.user == post.author:
        if status == 'sold':
            post.is_sold = True
            messages.success(request, f'Post marked as sold!')
        elif status == 'unsold':
            post.is_sold = False
            messages.success(request, f'Post marked as not sold!')
        post.save()
    else:
        messages.error(request, f'You do not have permission to update this post.')

    return redirect(reverse('post-detail', kwargs= {'pk': pk}))

from django.contrib import admin
from django.urls import path, include
from .views import (about, 
                    PostListView, PostDetailView,
                    
                    PostDeleteView, UserPostListView,
                    MarketListView, TicketListView,
                    RideListView, SubListView,
                    FavListView, SettingsListView, search, create_post_view, update_view)

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('market/', MarketListView.as_view(), name='market-home'),
    path('tickets/', TicketListView.as_view(), name='tickets-home'),
    path('rideshare/', RideListView.as_view(), name='rideshare-home'),
    path('sublease/', SubListView.as_view(), name='sublease-home'),
    path('favorites/', FavListView.as_view(), name='favorites-home'),
    path('settings/', SettingsListView.as_view(), name='settings-home'),
    
    path('search/', search, name='search'),


    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('about/', about, name ='blog-about'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', create_post_view, name='post-create'),
    path('post/<int:pk>/update/<str:status>/', update_view, name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),

    path('chat/', include('chat.urls')),

    


]
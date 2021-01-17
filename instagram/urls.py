from . import views
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from .views import (PostListView, PostDetailView, follow_unfollow, 
    PostCreateView, PostUpdateView, PostDeleteView, UserListView, ProfileDetailView)

urlpatterns = [
    path('', PostListView.as_view(), name='gram-landing'),
    path('search/', views.searchprofile, name='search'),
    path('following/',views.posts_following, name='posts-follow-view'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('user/users/', UserListView.as_view(), name='user-posts'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('register/',views.register, name='registration'),
    path('profile/',views.profile, name='profile'),
    path('about/',views.about, name='about'),
    path('comment/<id>/', views.comment, name='comment'),
    path('like/<int:pk>/', views.like_image, name='like_post'),
    path('<pk>/', ProfileDetailView.as_view(), name='profile-details'),
    path('follow/<pk>/',follow_unfollow, name='follow-unfollow'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
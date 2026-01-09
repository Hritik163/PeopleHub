from django.contrib import admin
from django.urls import path
from socialmedia import settings
from userauth import views
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('loginn/', views.loginn, name='loginn'),
    path('logoutt/', views.logoutt, name='logout'),
    path('upload', views.upload, name='upload'),
    path('like-post/<str:id>', views.likes, name='likes'),
    path('explore', views.explore, name='explore'),
    path('profile/<str:id_user>', views.profile, name='profile'),
    path('delete/<str:id>', views.delete, name='delete'),
    path('search/', views.search_results, name='search_results'),
    path('follow', views.follow, name='follow'),
]

    
    
    
    
    


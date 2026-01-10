from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('signup/', views.signup, name='signup'),
    path('loginn/', views.loginn, name='loginn'),
    path('logoutt/', views.logoutt, name='logout'),

    path('upload/', views.upload, name='upload'),
    path('like-post/<int:id>/', views.likes, name='likes'),
    path('delete/<int:id>/', views.delete, name='delete'),

    path('explore/', views.explore, name='explore'),
    path('profile/<str:id_user>/', views.profile, name='profile'),

    path('search/', views.search_results, name='search_results'),
    path('follow/', views.follow, name='follow'),

    # Optional but valid
    path('post/<int:id>/', views.home_post, name='home_post'),
]

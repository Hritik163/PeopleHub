from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("signup/", views.signup, name="signup"),
    path("loginn/", views.loginn, name="loginn"),
    path("logoutt/", views.logoutt, name="logout"),

    path("upload/", views.upload, name="upload"),
    path("like-post/<uuid:id>/", views.likes, name="likes"),
    path("delete/<uuid:id>/", views.delete, name="delete"),

    path("profile/<int:user_id>/", views.profile, name="profile"),
    path("search/", views.search_results, name="search_results"),
    path("follow/", views.follow, name="follow"),
]

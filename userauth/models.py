from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
from cloudinary.models import CloudinaryField   # ✅ ADD THIS

User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField(primary_key=True, default=0)
    bio = models.TextField(blank=True, default='')
    profileimg = CloudinaryField(                # ✅ CHANGE
        'profile_image',
        blank=True,
        null=True
    )
    location = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return self.user.username


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.CharField(max_length=100)
    image = CloudinaryField(                     # ✅ CHANGE
        'post_image',
        blank=True,
        null=True
    )
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user


class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Followers(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user

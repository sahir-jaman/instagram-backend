from django.db import models
from django.contrib.auth.models import AbstractUser
from app.manager import UserManager

# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=50, unique= True)
    first_name = models.CharField(max_length=100, null= True, blank= True)
    last_name =models.CharField(max_length=100, null= True, blank= True)
    bio = models.CharField(max_length=200, null=True)


    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)

    USERNAME_FEILD = "email"
    REQUIRED_FIELDS =[]
    objects = UserManager()         

class Post(models.Model):
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=164)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

class PostLike(models.Model):
    post = models.ForeignKey(Post, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("post", "user"), )

class PostComment(models.Model):
    comment_text = models.CharField(max_length=264)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=False, on_delete=models.CASCADE)

class UserFollow(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name="src_follow")
    follows = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name="dest_follow")

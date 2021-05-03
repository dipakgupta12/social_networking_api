from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Post(models.Model):
    title = models.CharField(max_length=40, blank=False)
    description = models.TextField()
    created_by = models.ForeignKey(
        to=User, on_delete=models.SET_NULL, null=True, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserPostActivity(models.Model):
    ACTION_CHOICES = (
        ("L", "like"),
        ("UN", "unlike"),
        ("NA", "no_action")
    )
    user = models.ForeignKey(
        to=User, on_delete=models.SET_NULL, null=True, related_name="activities")
    post = models.ForeignKey(
        to=Post, on_delete=models.SET_NULL, null=True, related_name="activities")
    action = models.CharField(choices=ACTION_CHOICES,
                              max_length=10, default="NA")
    created_at = models.DateTimeField(auto_now_add=True)


class UserLocationDetail(models.Model):
    user = models.OneToOneField(
        to=User, on_delete=models.SET_NULL, null=True, related_name="location")
    ip = models.CharField(max_length=40, blank=False, null=True)
    country = models.CharField(max_length=40, blank=False, null=True)
    geo = models.CharField(max_length=40, blank=False, null=True)
    is_holiday = models.BooleanField(default=False)

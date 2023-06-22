from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.

class User(AbstractUser):
    pass

class Photo(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos', null=False)
    uploadTime = models.DateTimeField(auto_now_add=True, null=False)

    def user_directory_path(instance, filename):
        return "{0}/photos/{1}".format(instance.created_by, filename)
    content = models.ImageField(upload_to=user_directory_path, null=False)

    class Meta:
        verbose_name = 'Photo'

class Profile(models.Model):
    user = models.OneToOneField(User, related_name = 'profile', primary_key=True, null = False, on_delete = models.CASCADE)
    bio = models.CharField(max_length=500, null = False)
    profilePic = models.ForeignKey(Photo, related_name = '+', on_delete=models.SET_NULL, null = True)

class Post(models.Model):
    created_by = models.ForeignKey(Profile, related_name = 'posts', null = False, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, null = False, on_delete = models.CASCADE)
    caption = models.CharField(max_length=1000, null = False)
    upload_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-upload_time']

class Message(models.Model):
    by = models.ForeignKey(Profile, related_name = 'messages_sent_by_user', null = False, on_delete=models.CASCADE)
    to = models.ForeignKey(Profile, null = False, related_name='messages_sent_to_user', on_delete=models.CASCADE)
    upload_time = models.DateTimeField(auto_now_add=True)
    body = models.CharField(max_length=600)

class Follow(models.Model):
    profile = models.OneToOneField(Profile, related_name = 'follow_table', primary_key = True, null = False, on_delete = models.CASCADE)
    following = models.ManyToManyField(Profile, related_name = 'followers')

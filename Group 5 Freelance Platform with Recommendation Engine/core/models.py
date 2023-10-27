from django.contrib.auth.models import AbstractUser
from django.db import models

class Tag(models.Model):
    tag = models.CharField(max_length=255)
    category = models.CharField(max_length=255)

class UserProfile(AbstractUser):
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True)
    profile_image = models.ImageField(upload_to='images/', default='assets/user-profile.svg')
    username = models.CharField(max_length=255, unique=True)
    online_status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.username

class UserInterests(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    score = models.FloatField(default = 0)

class Freelancer(models.Model):
    user_id = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    freelancer_id = models.AutoField(primary_key=True)
    custom_url = models.CharField(max_length=255, unique=True, null=True)
    paypal_id = models.CharField(max_length=255, null=True)

class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='images/')
    link = models.SlugField(unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class Post_tag(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    score = models.IntegerField(default = 0)

class Interaction(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

class Logs(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

class Recommendations(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    score = models.TextField()
    visited = models.BooleanField(default=False)

class TopCharts(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    type = models.TextField()

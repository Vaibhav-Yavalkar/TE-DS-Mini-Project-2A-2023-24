from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class post(models.Model):
    tittle=models.CharField(max_length=100)
    content=models.TextField()
    date_posted=models.DateTimeField(default=timezone.now)
    author=models.ForeignKey(User,on_delete=models.CASCADE)
# Create your models here.

from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    director = models.CharField(max_length=255)
    year = models.IntegerField()
    description = models.TextField()
    # Add more fields as needed

    def __str__(self):
        return self.title

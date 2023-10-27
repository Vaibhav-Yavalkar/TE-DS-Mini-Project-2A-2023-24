from django.db import models
from core.models import UserProfile
from core.models import Post

class Order(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    service = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

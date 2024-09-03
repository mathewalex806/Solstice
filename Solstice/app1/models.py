from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="portfolios")
    portfolio_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}'s {self.portfolio_name}"
    
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=True, null= True)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=52, blank=True, null= True)

    def __str__(self):
        return f"{self.user}'s {self.name}"
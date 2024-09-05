from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="portfolios")
    portfolio_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}'s {self.portfolio_name}"
    
class Watchlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=True, null= True)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=52, blank=True, null= True)

    def __str__(self):
        return f"{self.user}'s {self.name}"
    

class Company(models.Model):
    name = models.CharField(max_length=51,blank=False, null=False)
    sector = models.CharField(max_length=51,blank=False, null=False)
    ticker = models.CharField(max_length=5,blank=False, null=False)
    industry = models.CharField(max_length=51,blank=True, null=True)

    def __str__(self):
        return self.name


class Watchlist_company(models.Model):
    watchlist = models.ForeignKey(Watchlist, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.watchlist.user} => {self.company.name}"
    

class Investment(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    purchase_price = models.DecimalField(decimal_places=3, max_digits=10,default=0.00)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company.name}'s {self.quantity} shares"


class Transactions(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    transction_type = models.CharField(max_length=5)            ## USE 'BUY' or 'SELL'
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    date = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f"{self.transction_type} {self.quantity} shares of {self.company.name} at {self.price}"


class Portfolio_performance(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=3,default=0.00)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.portfolio.user}'s portfolio value is {self.value}"

class StockPrice (models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    price = models. DecimalField(max_digits=10, decimal_places=3)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company.name} price is {self.price}"
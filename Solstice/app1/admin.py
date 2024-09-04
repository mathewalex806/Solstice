from django.contrib import admin
from .models import Portfolio, Watchlist, Company, Watchlist_company, Investment, Transactions, Portfolio_performance
from django.contrib.auth.models import User
# Register your models here.


admin.site.register(Portfolio)
admin.site.register(Watchlist)
admin.site.register(Company)
admin.site.register(Watchlist_company)
admin.site.register(Investment)
admin.site.register(Transactions)
admin.site.register(Portfolio_performance)
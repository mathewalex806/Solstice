from django.contrib import admin
from .models import Portfolio, Watchlist
from django.contrib.auth.models import User
# Register your models here.


admin.site.register(Portfolio)
admin.site.register(Watchlist)
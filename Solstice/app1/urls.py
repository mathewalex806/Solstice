from django.urls import path
from . import views

urlpatterns = [
    path("",views.index, name="index"),
    path("signup/",views.signup, name="signup"),
    path("login/",views.login, name="login"),
    path('create-portfolio/',views.create_portfolio, name="create_portflio"),
    path('create-watchlist/',views.create_watchlist,name="create_watchlist"),
    path('watchlist/',views.watchlist,name="watchlist"),
    path('investment/', views.add_investment, name="investment"),
]
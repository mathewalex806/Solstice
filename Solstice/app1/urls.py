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
    path('transactions/', views.transaction, name="transactions"),
    path('populate-company/', views.populate_company_table, name="populate_company"),
    path('portfolio-performance/', views.portfolio_performance, name="portfolio_performance"),      ##Used by the cron job
    path('user-portfolioPerformace/', views.portfolio_performance_user, name="user_portfolio_performance"),
]
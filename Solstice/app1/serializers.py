from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password"]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
    

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["name", "sector", "ticker", "industry"]

class WatchlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = ["user", "name", "description", "created_at"]

class WatchlistCompanyserializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model  = Watchlist_company
        fields = ["company", "added_on"]

class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ["user", "portfolio_name"]


class ShortendCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["name", "ticker"]

class InvestmentSerializer(serializers.ModelSerializer):
    company = ShortendCompanySerializer(read_only=True)
    portfolio = PortfolioSerializer(read_only=True)

    class Meta:
        model = Investment
        fields = ["portfolio", "company", "quantity", "purchase_price", "date"]


class TransactionSerializer(serializers.ModelSerializer):
    company = ShortendCompanySerializer(read_only=True)
    portfolio = PortfolioSerializer(read_only=True)

    class Meta:
        model = Transactions
        fields = ["portfolio", "company", "transction_type", "quantity", "price", "date"]
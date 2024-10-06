from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, WatchlistCompanyserializer, InvestmentSerializer, TransactionSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from .models import Portfolio, Watchlist, Watchlist_company, Investment, Transactions, Portfolio_performance, Company
from django.contrib.auth.models import User
import finnhub
import dotenv 
import os
from dotenv import load_dotenv

load_dotenv()
finnhub_client = finnhub.Client(os.getenv("API_KEY"))

@csrf_exempt
@api_view(["POST","GET"])
@permission_classes([AllowAny])
def index(request):
    return Response({"message":"Index url for Solstice "},status=status.HTTP_200_OK)

@api_view(['POST',"GET"])
def signup(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message":"Get url for the signup url"},status=status.HTTP_200_OK)

## Adding the login fuction

@api_view(["GET","POST"])
@permission_classes([AllowAny])
def login(request):
    if request.method == "POST":
        username = request.data["username"]
        password = request.data["password"]

        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, "message":"Login successfull"}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message":"Get url for the login page"},status=status.HTTP_200_OK)


## Creating Portfolio

@api_view(["POST","GET"])
@permission_classes([IsAuthenticated])
def create_portfolio(request):
    if request.method == "POST":
        username  = request.user.username
        portfolio_name = request.data["portfolio_name"]
        try:
            user  = User.objects.get(username = username)
            portfolio = Portfolio.objects.create(user = user, portfolio_name = portfolio_name)
            return Response({"message":f"Created portfolio : {portfolio_name}"}, status=status.HTTP_201_CREATED)
        except:
            return Response({"error":"Failed to create portfolio"},status=status.HTTP_400_BAD_REQUEST)
    return Response({"message":"GET url for the create portfolio route"})

## Creating Watchlist

@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def create_watchlist(request):
    if request.method == "POST":
        username  = request.user.username
        name = request.data["name"]
        desc = request.data["description"]
        try:
            user  = User.objects.get(username = username)
            watchlist = Watchlist.objects.create(user = user, name = name, description = desc)
            return Response({"message":f"Created watchlist : {name}"}, status=status.HTTP_201_CREATED)
        except:
            return Response({"error":"Failed to create watchlist"},status=status.HTTP_400_BAD_REQUEST)
    return Response({"message":"GET url for the create watchlist route"})


# POST request to add company to watchlist
# GET request to get all companies in watchlist

@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def watchlist(request):
    if request.method == "POST":
        user = request.user.username
        comp_ticker = request.data.get("ticker")  
        print(comp_ticker)
        try:
            watchlist = Watchlist.objects.get(user__username=user)
            print(watchlist)
            company = Company.objects.get(ticker=comp_ticker)   
            print(company)
            comp_watchlist = Watchlist_company.objects.get_or_create(watchlist=watchlist, company=company)
            print(comp_watchlist)

            return Response({"message": f"Added {comp_ticker} to watchlist"}, status=status.HTTP_201_CREATED)
        
        except Watchlist.DoesNotExist:
            return Response({"error": "Watchlist not found for user"}, status=status.HTTP_404_NOT_FOUND)
        
        except Company.DoesNotExist:
            return Response({"error": f"Company {comp_ticker} not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            print(e)  
            return Response({"error": "Failed to add to watchlist"}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        user = request.user.username
        try:
            watchlist = Watchlist.objects.get(user__username=user)
            watchlist_comp = Watchlist_company.objects.filter(watchlist=watchlist)

            serializer = WatchlistCompanyserializer(watchlist_comp, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Watchlist.DoesNotExist:
            return Response({"error": "Watchlist not found for user"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)  
            return Response({"error": "Failed to get watchlist"}, status=status.HTTP_400_BAD_REQUEST)


##Adding investment to portfolio

# Post request to add investment to portfolio
# GET request to get all investments in portfolio

@api_view(["POST","GET"])
@permission_classes([IsAuthenticated])
def add_investment(request):
    if request.method == "POST":
        username = request.user.username
        ticker = request.data["ticker"]
        quantity = request.data["quantity"]
        #purchase_price = request.data["purchase_price"]
        try:
            user = User.objects.get(username = username)
            company = Company.objects.get(ticker = ticker)
            portfolio = Portfolio.objects.get(user = user)
            purchase_price = finnhub_client.quote(ticker)["c"] * float(quantity)
            investment = Investment.objects.create(portfolio = portfolio, company = company, quantity = quantity, purchase_price = purchase_price)
            return Response({"message":f"Added investment to portfolio"}, status=status.HTTP_201_CREATED)
        except Company.DoesNotExist:
            return Response({"error":"Company not found"},status=status.HTTP_404_NOT_FOUND)
        except Portfolio.DoesNotExist:
            return Response({"error":"Portfolio not found"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"error":"Failed to add investment"},status=status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":
        username = request.user.username
        try:
            user = User.objects.get(username= username)
            portfolio = Portfolio.objects.get(user = user)
            investments = Investment.objects.filter(portfolio = portfolio)
            serializer = InvestmentSerializer(investments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Portfolio.DoesNotExist:
            return Response({"error":"Portfolio not found"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"error":"Failed to get investments"},status=status.HTTP_400_BAD_REQUEST)
        

#Creating a transaction

# Post request to add transaction to portfolio
# GET request to get all transactions in portfolio

@api_view(["POST", "GET"])
@permission_classes([IsAuthenticated])
def transaction(request):
    if request.method == "POST":
        username = request.user.username
        ticker = request.data["ticker"]
        quantity = request.data["quantity"]
        transaction_type = request.data["transaction_type"]
        try:
            user = User.objects.get(username = username)
            company = Company.objects.get(ticker = ticker)
            portfolio = Portfolio.objects.get(user = user)
            if transaction_type == "BUY":
                price = finnhub_client.quote(ticker)["c"] * float(quantity)
                transaction = Transactions.objects.create(portfolio = portfolio, company = company, transction_type = transaction_type, quantity = quantity, price = price)
                return Response({"message":f"Added transaction to portfolio"}, status=status.HTTP_201_CREATED)
            elif transaction_type == "SELL":
                price = finnhub_client.quote(ticker)["c"] * float(quantity)
                transaction = Transactions.objects.create(portfolio = portfolio, company = company, transction_type = transaction_type, quantity = quantity, price = price)
                return Response({"message":f"Added transaction to portfolio"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"error":"Invalid transaction type"},status=status.HTTP_400_BAD_REQUEST)
        except Company.DoesNotExist:
            return Response({"error":"Company not found"},status=status.HTTP_404_NOT_FOUND)
        except Portfolio.DoesNotExist:
            return Response({"error":"Portfolio not found"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"error":"Failed to add transaction"},status=status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":
        username = request.user.username
        try:
            user = User.objects.get(username= username)
            portfolio = Portfolio.objects.get(user = user)
            transactions = Transactions.objects.filter(portfolio = portfolio)
            serializer = TransactionSerializer(transactions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Portfolio.DoesNotExist:
            return Response({"error":"Portfolio not found"},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"error":"Failed to get transactions"},status=status.HTTP_400_BAD_REQUEST)
        
#Populating Company table
# GET request to populate company table
# POST request to add company to company table

@api_view(["GET","POST"])
@permission_classes([AllowAny])
def populate_company_table(request):
    if request.method == "GET":
        companies = finnhub_client.stock_symbols('US')
        for company in companies:
            # Use get_or_create to avoid duplicates
            Company.objects.get_or_create(
                ticker=company["displaySymbol"],
                defaults={
                    'name': company["description"],
                    'sector': "sector",    
                    'industry': "industry"  
                }
            )
        return Response({"message": "Populated company table"}, status=status.HTTP_200_OK)
    
    if request.method == "POST":
        name = request.data["name"]
        ticker = request.data["ticker"]
        sector = request.data["sector"]
        industry = request.data["industry"]
        try:
            company = Company.objects.get_or_create(name = name, ticker = ticker, sector = sector, industry = industry)
            return Response({"message":f"Added company to company table"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"error":"Failed to add company"},status=status.HTTP_400_BAD_REQUEST)
        

## Tracking portfolio performance

@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def portfolio_performance(request):
    if request.method == "GET":
        try:
            users = User.objects.all()
            for user in users:
                try:
                    portfolio = Portfolio.objects.get(user=user)
                    investments = Investment.objects.filter(portfolio=portfolio)
                    if len(investments) != 0:
                        total_investment = 0
                        total_value = 0

                        # Purchase price stored in the database is the purchase price of all the stocks and not individual ones.
                        for investment in investments:
                            total_investment += investment.purchase_price
                            # Fetching current value
                            current_price = finnhub_client.quote(investment.company.ticker)['c']
                            if current_price is not None:  
                                total_value += current_price * investment.quantity

                        portfolio_perform = Portfolio_performance(portfolio=portfolio, value=total_value)
                        portfolio_perform.save()
                except Portfolio.DoesNotExist:
                    print(f"Portfolio does not exist for user: {user.username}")
                except Exception as e:
                    print(f"Error processing portfolio for user {user.username}: {e}")

            return Response({"message": "Portfolio performance records added for users"}, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({"error": "Failed to add portfolio performance records"}, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response({"message": "POST request for the portfolio performance route is not implemented"}, status=status.HTTP_200_OK)


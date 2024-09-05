from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, WatchlistCompanyserializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from .models import Portfolio, Watchlist, Watchlist_company, Investment, Transactions, Portfolio_performance, Company
from django.contrib.auth.models import User

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
        comp_name = request.data.get("name")  
        print(comp_name)
        try:
            watchlist = Watchlist.objects.get(user__username=user)
            print(watchlist)
            company = Company.objects.get(name=comp_name)
            print(company)
            comp_watchlist = Watchlist_company.objects.create(watchlist=watchlist, company=company)
            print(comp_watchlist)

            return Response({"message": f"Added {comp_name} to watchlist"}, status=status.HTTP_201_CREATED)
        
        except Watchlist.DoesNotExist:
            return Response({"error": "Watchlist not found for user"}, status=status.HTTP_404_NOT_FOUND)
        
        except Company.DoesNotExist:
            return Response({"error": f"Company {comp_name} not found"}, status=status.HTTP_404_NOT_FOUND)
        
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

## Tracking portfolio performance
import os
import sys
import django
import finnhub
from dotenv import load_dotenv
from Solstice.app1.models import Portfolio, Investment, Portfolio_performance
from django.contrib.auth.models import User

# Adjust the system path
sys.path.append('/app')

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Solstice.settings')

# Initialize Django
django.setup()

# Load environment variables
load_dotenv()
finnhub_client = finnhub.Client(os.getenv("API_KEY"))

# Debug print for settings
print("DJANGO_SETTINGS_MODULE:", os.environ.get('DJANGO_SETTINGS_MODULE'))

try:
    users = User.objects.all()
    for user in users:
        portfolio = Portfolio.objects.get(user=user)
        investments = Investment.objects.filter(portfolio=portfolio)
        total_investment = 0
        total_value = 0

        # Purchase price stored in the database is the purchase price of all the stocks and not individual ones.
        for investment in investments:
            total_investment += investment.purchase_price
            # Fetching current value
            current_price = finnhub_client.quote(investment.company.ticker)['c']
            if current_price is not None:  # Check if current_price is valid
                total_value += current_price * investment.quantity

        # Create and save the portfolio performance record
        portfolio_perform = Portfolio_performance(portfolio=portfolio, value=total_value)
        portfolio_perform.save()
        print("Portfolio performance record added for user:", user.username)

except Exception as e:
    print("An error occurred:", e)

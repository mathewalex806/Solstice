import requests

url = 'http://localhost:8000/portfolio-performance/'

def update_portfolio_performance():
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Portfolio performance updated successfully.")
            print(response.json())  # Print the response JSON for confirmation
        else:
            print(f"Failed to update portfolio performance. Status Code: {response.status_code}")
            print(response.json())  # Print any error message returned by the API
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    update_portfolio_performance()

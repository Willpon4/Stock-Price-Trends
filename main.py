import requests

###################
# Constants
###################
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo'

user_input = input("Pick a stock: ")

data = {
    "function": "TIME_SERIES_DAILY",
    "symbol": user_input,
    "ouputsize": "compact",
    "apikey": "ON68K3T82IU38UJI"
}

response = requests.get(url, data)

print(response.status_code)
print(response.json())




import urllib.request, urllib.error
import ssl
import certifi
import os

# Set the location of the CA certificates file
os.environ['REQUESTS_CA_BUNDLE'] = "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages/certifi/cacert.pem"

finviz_url = "https://finviz.com/quote.ashx?t="
tickers = ['AMZN', 'AAPL', 'IBM', 'COST', 'NFLX']
headers = {'User-Agent': 'Mozilla/5.0'}



for ticker in tickers:
    url = finviz_url + ticker

    try:
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)
        print("result code: " + str(response.getcode()))
    except urllib.error.URLError as e:
        print(f"Failed to catch data for {ticker}. Error: {e}")
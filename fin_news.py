
import urllib.request, urllib.error
from bs4 import BeautifulSoup
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

# Set the location of the CA certificates file
os.environ['REQUESTS_CA_BUNDLE'] = "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages/certifi/cacert.pem"

finviz_url = "https://finviz.com/quote.ashx?t="
tickers = ['AMZN', 'AAPL', 'IBM', 'COST', 'NFLX']
headers = {'User-Agent': 'Mozilla/5.0'}

news_tables = {}

for ticker in tickers:
    url = finviz_url + ticker

    try:
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)
        
        print("result code: " + str(response.getcode()))
    except urllib.error.URLError as e:
        print(f"Failed to catch data for {ticker}. Error: {e}")

    html = BeautifulSoup(response, 'html.parser',)
    news_table = html.find(id='news-table')
    news_tables[ticker] = news_table
    #print(news_tables)
    break

amzn_data = news_tables["AMZN"]
amzn_rows = amzn_data.findAll('tr')

#for index, row in enumerate(amzn_rows):
    #Some of the rows dont have <a> tags, so this check still allows all the rows to be printed.
    #Without this check, the rows stop printing when an <a> tag is missing.
    #if row.a:
        #The strip() takes the extra whitespace off, otherwise it looks very messy in the terminal.
       # title = row.a.text.strip()
        #timestamp = row.td.text.strip()
        #print(f"{timestamp}   {title}")
   # else:
        #print("No <a> tag found in this row.")

#data structure to hold lists of the ticker news and timestamps
parsed_data = []

for ticker, news_table in news_tables.items():
    for row in news_table.findAll('tr'):

        title = row.a.text
        date_data = row.td.text.split(' ')

        if len(date_data) == 1:
            time = date_data[1]
        else:
            date = date_data[0]
            time = date_data[1]

        parsed_data.append([ticker, date, time, title])

print(parsed_data)


 
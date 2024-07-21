
import urllib.request, urllib.error
from bs4 import BeautifulSoup
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

# Set the location of the CA certificates file
os.environ['REQUESTS_CA_BUNDLE'] = "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages/certifi/cacert.pem"

finviz_url = "https://finviz.com/quote.ashx?t="
# Tickers I are using (May add more in future)
ticker = str(input("Insert Ticker: "))
headers = {'User-Agent': 'Mozilla/5.0'}

news_tables = {}

url = finviz_url + ticker

# Was having trouble and getting errors with gathering the html
# so this try/except block fixes that
try:
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    
    print("result code: " + str(response.getcode()))
except urllib.error.URLError as e:
    print(f"Failed to catch data for {ticker}. Error: {e}")

# This gets the html
html = BeautifulSoup(response, 'html.parser')
# This gets the news articles from the html
news_table = html.find(id='news-table')
# This creates a dictonary with the key as the ticker and value as all of the news headers
news_tables[ticker] = news_table
#print(news_tables)

#######################
# This was for only using AMZN (May delete this later)
#######################


#amzn_data = news_tables["AMZN"]
#amzn_rows = amzn_data.findAll('tr')

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

######################################################

#data structure to hold lists of the ticker news and timestamps
parsed_data = []

for ticker, news_table in news_tables.items():
    for row in news_table.findAll('tr'):

        title = row.a.text
        date_data = row.td.text.split(' ')

        #splits depending on if there is a time and date or just a time
        if len(date_data) == 1:
            time = date_data[1]
        else:
            date = date_data[0]
            time = date_data[1]

        parsed_data.append([ticker, date, time, title])

# This creates a table of data using Pandas with the headers being in columns[]
# it uses the data from parsed data to create this
df = pd.DataFrame(parsed_data, columns=['ticker', 'date', 'time', 'title'])

# This is allowing vader to call this function
vader = SentimentIntensityAnalyzer()

#This creates the polarity scores (sentiment analysis) for the data in parsed_data
f = lambda title: vader.polarity_scores(title)['compound']
#Applys the data
df["compound"] = df['title'].apply(f)

total_compound_score = 0
compound_num = 0
for score in df["compound"]:
    compound_num += 1
    total_compound_score += score

average_compound_score = total_compound_score/compound_num

print(df.head())
print(f"Average Sentiment Score: {average_compound_score}")

 
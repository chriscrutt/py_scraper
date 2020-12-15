#########################################################
# gives author aditional privacy when commiting- delete #
# Allowing for type hints cause why not                 #
from apis import api_key, api_secret  #
#########################################################

# for type hints
from typing import List

# importing binance client
from binance.client import Client

# importing date for a readable server time
from datetime import datetime

# to format the date we get from the server
from date_format import convert_date

# import other funcs to make everything more readable
from misc_funcs import my_median

# setting up api keys
pub = api_key
priv = api_secret

# setting up client functions will access
client = Client(pub, priv)

#########################################################

# pulling (average) price of a ticker
avg_price = client.get_avg_price(symbol="WBTCBTC")

# prints that average
print("average price WBTC/BTC:", avg_price["price"])

#########################################################

# getting daily candles from past 21 days
tickers = client.get_klines(symbol="WBTCBTC", interval="1d", limit="21")

# creating an array for all highs and lows of candles, as well as volume
high: List[float] = []
low: List[float] = []

# appends highs and lows of candles to respective arrays, as well as volume
for candle in tickers:
    high.append(float(candle[2]))
    low.append(float(candle[3]))

#########################################################

highMedian = round(my_median(high) * 100000) / 100000
lowMedian = round(my_median(low) * 100000) / 100000

# prints the 21 day median of the highs and lows
print("21 day median high:", highMedian, "| 21 day median low:", lowMedian)

#########################################################
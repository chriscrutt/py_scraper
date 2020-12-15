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

# importing sleep
from time import sleep

# import other funcs to make everything more readable
from misc_funcs import my_median, price_round, quant_round, percent_change

# setting up api keys
pub = api_key
priv = api_secret

# setting up client functions will access
client = Client(pub, priv)

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

my_orders = client.get_open_orders(symbol='WBTCBTC')

order_status = client.get_order(symbol='WBTCBTC',
                                orderId=my_orders[0]["orderId"])

if order_status["status"] == "FILLED":
    print("order ID", order_status["orderId"], "if filled")
else:
    print("order ID", order_status["orderId"], "if not filled")

#########################################################

tickers = client.get_ticker(symbol="WBTCBTC")

last_price = tickers["lastPrice"]
print("last price:", last_price)
ask = tickers["askPrice"]
print("current ask price:", ask)
bid = tickers["bidPrice"]
print("current bid price:", bid)
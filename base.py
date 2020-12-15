# for time
import datetime

# importing sleep
from time import sleep

# import other funcs to make everything more readable
from misc_funcs import my_median, price_round, quant_round, percent_change

#########################################################

# import stuff for apis
from apis import api_key, api_secret

# importing binance client
from binance.client import Client

# setting up api keys
pub = api_key
priv = api_secret

# setting up client functions will access
client = Client(pub, priv)

#########################################################

server_time = client.get_server_time()

readable_time = datetime.datetime.fromtimestamp(
    round(server_time["serverTime"]) / 1000).strftime('%Y-%m-%d %H:%M:%S')

print(readable_time)

tickers = client.get_ticker(symbol="WBTCBTC")

ask = tickers["askPrice"]
print("current ask price:", ask)
bid = tickers["bidPrice"]
print("current bid price:", bid)

last_price = tickers["lastPrice"]
print("last price:", last_price)
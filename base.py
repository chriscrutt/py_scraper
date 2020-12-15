# for time
import datetime

# importing sleep
from time import sleep

# import other funcs to make everything more readable
from misc_funcs import median, price_round, quant_round, percent_change

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


def header() -> None:

    server_time = client.get_server_time()

    readable_time = datetime.datetime.fromtimestamp(
        round(server_time["serverTime"]) / 1000).strftime('%Y-%m-%d %H:%M:%S')

    pair_data = client.get_ticker(symbol="WBTCBTC")
    last_price = pair_data["lastPrice"]

    candle_data = client.get_klines(symbol="WBTCBTC",
                                    interval="1d",
                                    limit="21")

    high_median, low_median = median(candle_data)

    print(readable_time, "| Open Orders =", None, "| High Median ≈",
          high_median, "| Low Median ≈", low_median, "| Last price =",
          price_round(last_price))


header()
# importing date for a readable server time
from datetime import datetime

# to format the date we get from the server
from date_format import convert_date

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


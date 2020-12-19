from math import log
from apis import apis

from binance.client import Client

from time import time

from binance.client import Client


# gets wbtc and btc balances (free & locked into order)
def get_balances(client):
    btc = client.get_asset_balance(asset='BTC')
    btc_f = float(btc["free"])
    btc_l = float(btc["locked"])

    wbtc = client.get_asset_balance(asset='WBTC')
    wbtc_f = float(wbtc["free"])
    wbtc_l = float(wbtc["locked"])

    return [btc_f, btc_l, wbtc_f, wbtc_l]


start = 1606037036000


def num_orders(client):

    t = client.get_my_trades(symbol='WBTCBTC', startTime=start, limit=1000)

    counter = len(t)

    while len(t) == 1000:

        t = client.get_my_trades(symbol='WBTCBTC',
                                 startTime=t[len(t) - 1]["time"],
                                 limit=1000)

        counter += len(t)

    return counter


def init(apis):
    for api in apis:
        print(api)

        client = Client(apis[api]["pub"], apis[api]["priv"])

        shucks = get_balances(client)
        btc = shucks[0]
        btcc = shucks[1]
        wbtc = shucks[2]
        wbtcc = shucks[3]

        # Total P+I (A):
        # Principal (P):
        # Compound (n):	Compounding (x/Yr)
        # Time (t in years)

        # r = n[(A / P) ^ (1 / nt) - 1]

        A = 0.51  # Total P+I (A)
        P = 0.5  # Principal (P)
        t = (round(time()) - start / 1000) / 31557600  # time passed
        n = num_orders(client) / t  # Compound (n): (orders filled/time passed)

        apy = n * ((A / P)**(1 / (n * t)) - 1)

        print(apy)

        print("%-20s %4.8f   |   %-21s %4.8f" %
              ("start btc balance:", btc + btcc, "start wbtc balance:",
               wbtc + wbtcc))

        print("%-20s %4.8f   | %23s %4.8f" %
              ("current btc balance:", btc + btcc, "current wbtc balance:",
               wbtc + wbtcc))

        print(
            "----------------------------------------------------------------------"
        )


init(apis)
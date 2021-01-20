from apis import apis

from binance.client import Client

from time import time

from datetime import datetime

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


start = 1609055490357
s_bnb = 60


def num_orders(client):

    t = client.get_my_trades(symbol='WBTCBTC', startTime=start, limit=1000)

    avg_price = float(client.get_avg_price(symbol='BNBBTC')["price"])
    bnb = client.get_asset_balance("BNB")
    c_bnb = float(bnb["free"]) + float(bnb["locked"])

    counter = len(t)

    while len(t) == 1000:

        t = client.get_my_trades(symbol='WBTCBTC',
                                 startTime=t[len(t) - 1]["time"],
                                 limit=1000)

        counter += len(t)

    return counter, avg_price, c_bnb


def init(apis):
    a = "<br>" + datetime.utcfromtimestamp(start / 1000).strftime(
        '%Y-%m-%d %H:%M:%S') + "</br><br>" + datetime.utcfromtimestamp(
            time()).strftime('%Y-%m-%d %H:%M:%S') + "</br>"

    for api in apis:
        a += f"<br>{api}</br>"

        client = Client(apis[api]["pub"], apis[api]["priv"])

        s_btc, s_wbtc = apis[api]["start_balance"]

        shucks = get_balances(client)
        btc, btcc, wbtc, wbtcc = shucks

        # Total P+I (A):
        # Principal (P):
        # Compound (n):	Compounding (x/Yr)
        # Time (t in years)

        # r = n[(A / P) ^ (1 / nt) - 1]

        avg_price = float(client.get_avg_price(symbol='WBTCBTC')["price"])

        orders_filled, bnb_price, bnb = num_orders(client)
        bnb_lost = s_bnb - bnb

        A = btc + btcc + (wbtc + wbtcc) / avg_price  # Total P+I (A)
        P = s_btc + (s_wbtc) / avg_price  # Principal (P)
        t = (round(time()) - start / 1000) / 31557600  # time passed in years
        n = orders_filled / t  # Compound (n): (orders filled/time passed)

        apy = n * ((A / P)**(1 / (n * t)) - 1)
        b_apy = n * (((A - bnb_lost * bnb_price) / P)**(1 / (n * t)) - 1)

        a += f"<br>orders filled: {orders_filled}</br>"
        a += f"<br>apy: {round(apy * 100, 3)}%   with bnb fees: {round(b_apy * 100, 3)}%</br>"

        a += "<br>%-20s %4.8f   |   %-20s %4.8f   |   %-21s %4.8f   |   total in btc: " % (
            "start bnb:", s_bnb, "start btc:", s_btc,
            "start wbtc:", s_wbtc) + str(round(P, 8)) + "</br>"

        a += "<br>%-20s %4.8f   |   %-20s %4.8f   | %21s %4.8f   |   total in btc: " % (
            "current bnb:", bnb, "current btc:", btc + btcc,
            "current wbtc:", wbtc + wbtcc
        ) + f"{round(A, 8)}  |  with fees: {round(A - bnb_lost * bnb_price, 8)}</br>"

        a += "<br>----------------------------------------------------------------------</br><br></br>"

    b = f"<div style = \"font-family:roboto mono;\">{a}</div>"
    return b


def eh():
    return ''.join(map(str, init(apis)))


print(eh())
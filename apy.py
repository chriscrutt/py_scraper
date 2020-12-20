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


start = 1608435897000


def num_orders(client):

    t = client.get_my_trades(symbol='WBTCBTC', startTime=start, limit=1000)

    avg_price = float(client.get_avg_price(symbol='BNBBTC')["price"])

    bnb = 0

    counter = len(t)

    while len(t) == 1000:

        t = client.get_my_trades(symbol='WBTCBTC',
                                 startTime=t[len(t) - 1]["time"],
                                 limit=1000)

        for i in range(len(t)):
            bnb += float(t[i]["commission"])

        counter += len(t)

    return counter, bnb * avg_price


def init(apis):
    print(round(time() * 1000), "\n")
    for api in apis:
        print(api)

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

        orders_filled, bnb = num_orders(client)

        A = btc + btcc + (wbtc + wbtcc) / avg_price  # Total P+I (A)
        P = s_btc + (s_wbtc) / avg_price  # Principal (P)
        t = (round(time()) - start / 1000) / 31557600  # time passed in years
        n = orders_filled / t  # Compound (n): (orders filled/time passed)

        apy = n * ((A / P)**(1 / (n * t)) - 1)
        b_apy = n * (((A - bnb) / P)**(1 / (n * t)) - 1)

        print("orders filled:", orders_filled)
        print("annual percentage yeild:",
              str(round(apy * 100, 3)) + "%   with bnb fees:",
              str(round(b_apy * 100, 3)) + "%")

        print(
            "%-20s %4.8f   |   %-21s %4.8f   |   total balance in btc:" %
            ("start btc balance:", s_btc, "start wbtc balance:", s_wbtc),
            round(P, 8))

        print(
            "%-20s %4.8f   | %23s %4.8f   |   total balance in btc:" %
            ("current btc balance:", btc + btcc, "current wbtc balance:",
             wbtc + wbtcc), round(A, 8), "-", bnb, "=", round(A - bnb, 8))

        print(
            "----------------------------------------------------------------------"
        )


init(apis)
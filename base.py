from typing import List

from math import ceil, floor
# for time
import datetime

# importing sleep
from time import sleep

# import other funcs to make everything more readable
from misc_funcs import median, quant_round, percent_change

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

    orders = client.get_open_orders(symbol='WBTCBTC')

    num_orders = len(orders)

    print(readable_time, "| Open Orders =", num_orders, "| High Median ≈",
          high_median, "| Low Median ≈", low_median, "| Last price =",
          round(last_price * 100000) / 100000)

    return low_median, pair_data["bidPrice"], high_median, pair_data[
        "askPrice"], last_price, pair_data["weightedAvgPrice"]


# header()
#  * 100000) / 100000


def set_buy_price(prices, ask=0, order=None) -> None:

    if order:
        sold_price = order["price"]
        prices.append(sold_price - sold_price * 0.00076)
        price = floor(min(prices) * 100000) / 100000
    else:
        price = floor(min(prices) * 100000) / 100000
        base_price = ask - ask * 0.00076
        if price > base_price:
            print("lowest bid price is:", price,
                  "which is over our max price of:", base_price)
            return None

    return price


def buy(prices, balances, ask, order) -> None:

    price = set_buy_price(prices, ask, order)
    
    if price is None:
        return None

    balance = balances[1]["free"] + balances[1]["locked"] + (
        balances[0]["free"] + balances[0]["locked"]) / price

    quantity = quant_round(balance / 190)

    if quantity * price < balance[0]["free"]:
        buy_order = client.order_limit_buy(symbol='WBTCBTC',
                                           quantity=quantity,
                                           price=price)

        return buy_order

    else:
        print("insufficient balance. Have", balance[0]["free"], "BTC but need",
              quantity)
        return None


def set_sell_price(prices, bid, order) -> None:

    if order:
        bought_price = order["price"]
        prices.append(bought_price + bought_price * 0.00076)
        price = ceil(max(prices) * 100000) / 100000
    else:
        price = ceil(max(prices) * 100000) / 100000
        base_price = bid - bid * 0.00076
        if price < base_price:
            print("lowest bid price is:", price,
                  "which is over our max price of:", base_price)
            return None

    return price


def sell(prices, balances, bid, order) -> None:

    price = set_sell_price(prices, bid, order)
    
    if price is None:
        return None

    balance = balances[1]["free"] + balances[1]["locked"] + (
        balances[0]["free"] + balances[0]["locked"]) / price

    quantity = quant_round(balance / 190)

    if quantity < balance[1]["free"]:
        sell_order = client.order_limit_sell(symbol='WBTCBTC',
                                             quantity=quantity,
                                             price=price)

        return sell_order

    else:
        print("insufficient balance. Have", balance[1]["free"],
              "WBTC but need", quantity)
        return None


def check_orders(orders: List[dict]) -> None:

    low, bid, high, ask, last, avg = header()

    balances = [
        client.get_asset_balance(asset='BTC'),
        client.get_asset_balance(asset='WBTC')
    ]

    for i in range(len(orders)):
        order_status = client.get_order(symbol='WBTCBTC',
                                        orderId=orders[i]["orderId"])

        if order_status["status"] == "FILLED":
            if order_status["side"] == "SELL":
                new_order = buy([low, bid, last, avg], balances, None, order_status)
            elif order_status["side"] == "BUY":
                new_order = sell([high, ask, last, avg], balances, None, order_status)
            else:
                raise Exception("order_status doesn't have a side:",
                                order_status)
            
            if new_order:
                del orders[i]
                orders.append(new_order)


# my_orders = client.get_open_orders(symbol='WBTCBTC')
# check_orders(my_orders)
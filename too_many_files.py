"""here's a module docstring"""

from typing import List

import datetime

from math import ceil, floor

from time import sleep

from binance.client import Client

from apis import api

client = Client(api["neo 0.076 8h 21"]["pub"], api["neo 0.076 8h 21"]["priv"])

################################################################################


def main(last_trade: List[dict]) -> None:
    """controller function that gathers kline and last trade data"""

    # was this a buy or sell order
    og_side = last_trade[0]["side"]
    # what was the price of this order
    og_price = last_trade[0]["price"]

    # get current candle data
    candle_data = client.get_klines(symbol="WBTCBTC", interval="1d", limit="1")

    # set opening price of candle
    _open = candle_data[0][1]
    # set current price
    current_price = candle_data[0][4]

    # gets server time in UNIX
    server_time = client.get_server_time()

    # makes server time readable to normal people
    readable_time = datetime.datetime.fromtimestamp(
        round(server_time["serverTime"]) / 1000).strftime('%Y-%m-%d %H:%M:%S')

    # prints initial data
    print("\n", server_time["serverTime"], "-", readable_time,
          "| Last Trade Buy", last_trade[0]["origQty"], "WBTC at",
          last_trade[0]["price"], "| Open Price =", _open, "| Current Price =",
          current_price)

    # checking if trade was filled
    if last_trade[0]["status"] == "FILLED":
        # initiate a trade using the above info
        initiate_trade(og_price, og_side, _open)

    # if it's only partially filled
    elif last_trade[0]["status"] == "PARTIALLY_FILLED":
        # show how much of it has been filled
        print("Partially filled -", last_trade[0]["executedQty"],
              "already executed")

    # if order hasn't been filled or partially filled
    else:
        # if it is a sell order
        if og_side == "SELL":
            # and the new open base price is better
            if _open * 1.001 > og_price:
                # cancel current order
                client.cancel_order(symbol="WBTCBTC",
                                    orderId=last_trade[0]["orderId"])

                print("replacing order with a better price")

                # make a new order (remember putting 'buy' will create a sell order)
                complete_trade("BUY", _open * 1.001)

        # if it is a buy order
        elif og_side == "BUY":
            # and the new open base price is better
            if _open * 0.999 < og_price:
                # cancel current order
                client.cancel_order(symbol="WBTCBTC",
                                    orderId=last_trade[0]["orderId"])

                print("replacing order with a better price")

                # make a new order (remember putting 'sell' will create a buy order)
                complete_trade("SELL", _open * 0.999)


def initiate_trade(og_price: float, og_side: str, _open: float) -> None:
    """finalizes price points for buy and sell orders"""

    # if last order was a sell
    if og_side == "SELL":

        # setting first base price based on open
        new_open = _open * 0.999
        # setting second base price based on original order
        new_price = og_price * 0.999

        # setting new base price to lower of the two
        base_price = min(new_open, new_price)

        # complete the trade
        complete_trade(og_side, base_price)

    # if last order was a buy
    elif og_side == "BUY":

        # setting first base price based on open
        new_open = _open * 1.001
        # setting second base price based on original order
        new_price = og_price * 1.001

        # setting new base price to higher of the two
        base_price = max(new_open, new_price)

        # complete the trade
        complete_trade(og_side, base_price)


def complete_trade(og_side: str, base_price: float) -> None:
    """completes the trade and prints as such"""

    # if old order was a sell order
    if og_side == "SELL":

        # get WBTC balance
        balance = client.get_asset_balance(asset='WBTC')

        # makes sure there's enough balance to initiate trade
        assert (balance["free"] >= 0.0001
                and balance["free"] * base_price >= 0.0001)

        # create limit buy order
        order = client.order_limit_buy(
            symbol='WBTCBTC',
            quantity=floor(balance["free"] * 10000) / 10000,
            price=floor(base_price * 100000) / 100000)

        print("put in an order to buy", order["origQty"], "WBTC for",
              order["price"])

    # if old order was a buy order
    elif og_side == "BUY":

        # get BTC balance
        balance = client.get_asset_balance(asset='BTC')

        # makes sure there's enough balance to initiate trade
        assert (balance["free"] >= 0.0001
                and balance["free"] / base_price >= 0.0001)

        # create limit sell order
        order = client.order_limit_sell(
            symbol='WBTCBTC',
            quantity=floor(balance["free"] * 10000) / 10000,
            price=ceil(base_price * 100000) / 100000)

        print("put in an order to sell", order["origQty"], "WBTC for",
              order["price"])


################################################################################


def start() -> None:
    """start of the program"""

    # gets server time in UNIX
    server_time = client.get_server_time()

    # makes server time readable to normal people
    readable_time = datetime.datetime.fromtimestamp(
        round(server_time["serverTime"]) / 1000).strftime('%Y-%m-%d %H:%M:%S')

    print(server_time["serverTime"], "-", readable_time)

    # loop forever
    while True:

        # gets last order created
        last_trade = client.get_all_orders(symbol="WBTCBTC", limit=1)

        # starts main function
        main(last_trade)

        # sleeps for 61 seconds for funzies
        sleep(61)


start()

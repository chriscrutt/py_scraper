# for type-hints
from typing import List, Optional

# for rounding with prices and amounts
from math import ceil, floor

# for readability for unix time
import datetime

from time import sleep

# import other funcs to make everything more readable
from misc_funcs import median, quant_round

from binance.exceptions import BinanceAPIException

#########################################################

# import stuff for apis
# from apis import api_key, api_secret

#########################################################


# start of the function, shows us basic stats & returns all current prices
def header(orders) -> tuple:

    # gets server time in UNIX
    server_time = client.get_server_time()

    # makes server time readable to normal people
    readable_time = datetime.datetime.fromtimestamp(
        round(server_time["serverTime"]) / 1000).strftime('%Y-%m-%d %H:%M:%S')

    # gets current bid/ask and etc for WBTCBTC
    pair_data = client.get_ticker(symbol="WBTCBTC")

    # get's last price of coin
    last_price = float(pair_data["lastPrice"])

    # get's candles from last 21 daily candles
    candle_data = client.get_klines(symbol="WBTCBTC",
                                    interval="4h",
                                    limit="21")

    # gets median highs and lows from candle data
    high_median, low_median = median(candle_data)

    # gets amount of orders currently open
    num_orders = len(orders)

    # prints all the data we just got
    print(readable_time, "| Open Orders =", num_orders, "| High Median ≈",
          high_median, "| Low Median ≈", low_median, "| Last price =",
          last_price)

    # returns all the different prices we got for WBTCBTC
    return_val = [
        low_median, pair_data["bidPrice"], high_median, pair_data["askPrice"],
        last_price, pair_data["weightedAvgPrice"]
    ]

    return [float(i) for i in return_val]


#########################################################


# gets wbtc and btc balances (free & locked into order)
def get_balances() -> List[float]:
    btc = client.get_asset_balance(asset='BTC')
    btc_f = float(btc["free"])
    btc_l = float(btc["locked"])

    wbtc = client.get_asset_balance(asset='WBTC')
    wbtc_f = float(wbtc["free"])
    wbtc_l = float(wbtc["locked"])

    return [btc_f, btc_l, wbtc_f, wbtc_l]


#########################################################


# figure out the price to trade at based on info given
def set_order_price(
    prices: List[float],
    side: str,
    order: Optional[dict]  # pylint: disable=E1136
) -> Optional[float]:  # pylint: disable=E1136

    low = prices[0]
    high = prices[2]

    # if an order is given
    if order:

        # get that order's old price
        old_price = float(order["price"])

        try:
            # if this is to be a buy order
            if side == "SIDE_BUY":
                # find lowest trading price & return it
                prices.append(old_price - old_price * 0.00076)
                price = floor(min(prices) * 100000) / 100000
                return price
            # if this is to be a sell order
            elif side == "SIDE_SELL":
                # find highest trading price & return it
                prices.append(old_price + old_price * 0.00076)
                price = ceil(max(prices) * 100000) / 100000
                return price
        except TypeError:
            print("ERROR! old price =", old_price, "\ntotal order =", order)
            raise Exception(
                "TypeError: can't multiply sequence by non-int of type 'float'"
            )

    # if an order is not given
    else:

        # if this is to be a buy order
        if side == "SIDE_BUY":
            # find lowest trading price
            price = floor(min(prices) * 100000) / 100000
            # create a base that the price must be below
            base_price = high - high * 0.00076
            # if it's too high, return None
            if price > base_price:
                print("highest buyable price is:", price,
                      "which is over our max price of:", base_price)
                return None
            # if it passes, return the new price!
            return price

        # if this is to be a sell order
        elif side == "SIDE_SELL":
            # find highest trading price
            price = ceil(max(prices) * 100000) / 100000
            # create a base that the price must be above
            base_price = low + low * 0.00076
            # if it's too low, return None
            if price < base_price:
                print("lowest sellable price is:", price,
                      "which is under our min price of:", base_price)
                return None
            # if it passes, return the new price!
            return price


#########################################################


# creates a buy/sell order based on given data
def create_order(
        prices: List[float],
        side: str,
        order: Optional[dict],  # pylint: disable=E1136
) -> Optional[dict]:  # pylint: disable=E1136

    # gets best prices
    price = set_order_price(prices, side, order)

    # if there isn't a price, return None
    if price is None:
        return None

    balances = get_balances()

    # get balance converted to WBTC
    balance = balances[2] + balances[3] + (balances[0] + balances[1]) / price

    # get quantity of WBTC that should be traded
    quantity = quant_round(balance / 190)

    # if order is to be sold
    if side == "SIDE_SELL":
        # if there's enough WBTC available do a trade & return it
        if quantity < balances[2]:
            try:
                final_order = client.order_limit_sell(symbol='WBTCBTC',
                                                      quantity=quantity,
                                                      price=price)
                print("YAYYYYY - put in an order to SELL",
                      final_order["origQty"], "WBTC for", final_order["price"],
                      "BTC a pop!!!")
                return final_order

            except BinanceAPIException:
                print("!!! NO BALANCE ERROR !!!")
                return None

        # if not print so & return None
        else:
            print("insufficient balance to sell. Have", balances[2],
                  "WBTC but need", quantity)
            return None

    # if order is to be sold
    if side == "SIDE_BUY":
        # if there's enough BTC available do a trade & return it
        if quantity * price < balances[0]:
            try:
                final_order = client.order_limit_buy(symbol='WBTCBTC',
                                                     quantity=quantity,
                                                     price=price)
                print("YAYYYYY - put in an order to BUY",
                      final_order["origQty"], "WBTC for", final_order["price"],
                      "BTC a pop!!!")
                return final_order

            except BinanceAPIException:
                print("!!! NO BALANCE ERROR !!!")
                return None

        # if not print so & return None
        else:
            print("insufficient balance to buy. Have", balances[0],
                  "BTC but need", quantity * price)
            return None


#########################################################


# looking through old orders in order to update them
def check_orders(header: List[float], orders: List[dict]) -> List[dict]:

    # this will be used to store new orders made
    new_orders: List[dict] = []

    # going through each open order
    for i in range(len(orders)):

        # get the current order status
        order_status = client.get_order(symbol='WBTCBTC',
                                        orderId=orders[i]["orderId"])

        # if the order has been filled, create a new one
        if order_status["status"] == "FILLED":
            # create the inverse order
            if order_status["side"] == "SELL":
                print("hey! a sell order has been filled!")
                try:
                    new_order = create_order(header, "SIDE_BUY", order_status)
                except:
                    sleep(61)
                    new_order = create_order(header, "SIDE_BUY", order_status)
            elif order_status["side"] == "BUY":
                print("hey! a buy order has been filled!")
                try:
                    new_order = create_order(header, "SIDE_SELL", order_status)
                except:
                    sleep(61)
                    new_order = create_order(header, "SIDE_SELL", order_status)
            else:
                raise Exception("no specificed side for order creation\n",
                                order_status)

        # if the order hasn't been filled
        else:
            new_order = None

        # if there was a new order placed, delete old one & add new to new list
        if new_order:
            orders[i] = None
            new_orders.append(new_order)

    # update old list by extending all the new orders
    orders.extend(new_orders)

    orders = [i for i in orders if i]

    # return all the orders now
    return orders


#########################################################


# function for all the marbles
def main(lient, orders: List[dict]) -> List[dict]:

    global client
    client = lient

    head = header(orders)

    orders = check_orders(head, orders)

    buy_order = create_order(head, "SIDE_BUY", None)
    if buy_order:
        orders.append(buy_order)

    sell_order = create_order(head, "SIDE_SELL", None)
    if sell_order:
        orders.append(sell_order)

    return orders


#########################################################
# for type-hints
from typing import List, Optional

# for rounding with prices and amounts
from math import ceil, floor

# for readability for unix time
import datetime

from time import sleep

# import other funcs to make everything more readable
from misc_funcs import median, quant_round

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


def header(orders) -> tuple:

    server_time = client.get_server_time()

    readable_time = datetime.datetime.fromtimestamp(
        round(server_time["serverTime"]) / 1000).strftime('%Y-%m-%d %H:%M:%S')

    pair_data = client.get_ticker(symbol="WBTCBTC")
    last_price = float(pair_data["lastPrice"])

    candle_data = client.get_klines(symbol="WBTCBTC",
                                    interval="1d",
                                    limit="21")

    high_median, low_median = median(candle_data)

    num_orders = len(orders)

    print(readable_time, "| Open Orders =", num_orders, "| High Median ≈",
          high_median, "| Low Median ≈", low_median, "| Last price =",
          round(last_price * 100000) / 100000)

    return_val = [
        low_median, pair_data["bidPrice"], high_median, pair_data["askPrice"],
        last_price, pair_data["weightedAvgPrice"]
    ]

    return [float(i) for i in return_val]


def get_balances() -> List[float]:
    btc = client.get_asset_balance(asset='BTC')
    btc_f = float(btc["free"])
    btc_l = float(btc["locked"])

    wbtc = client.get_asset_balance(asset='WBTC')
    wbtc_f = float(wbtc["free"])
    wbtc_l = float(wbtc["locked"])

    return [btc_f, btc_l, wbtc_f, wbtc_l]


def set_order_price(
    prices: List[float],
    bid: float,
    ask: float,
    side: str,
    order: Optional[dict]  # pylint: disable=E1136
) -> Optional[float]:  # pylint: disable=E1136

    if order:
        old_price = order["price"]

        if side == "SIDE_BUY":
            prices.append(old_price - old_price * 0.00076)
            price = floor(min(prices) * 100000) / 100000
            return price
        elif side == "SIDE_SELL":
            prices.append(old_price + old_price * 0.00076)
            price = ceil(max(prices) * 100000) / 100000
            return price

    else:
        if side == "SIDE_BUY":
            price = floor(min(prices) * 100000) / 100000
            base_price = ask - ask * 0.00076
            if price > base_price:
                print("highest buyable price is:", price,
                      "which is over our max price of:", base_price)
                return None
            return price

        elif side == "SIDE_SELL":
            price = ceil(max(prices) * 100000) / 100000
            base_price = bid + bid * 0.00076
            if price < base_price:
                print("lowest sellable price is:", price,
                      "which is under our min price of:", base_price)
                return None
            return price


def create_order(
    prices: List[float],
    bid: float,
    ask: float,
    side: str,
    order: Optional[dict],  # pylint: disable=E1136
    balances: List[float]
) -> Optional[dict]:  # pylint: disable=E1136

    price = set_order_price(prices, bid, ask, side, order)

    if price is None:
        return None

    balance = balances[2] + balances[3] + (balances[0] + balances[1]) / price

    quantity = quant_round(balance / 190)

    if side == "SIDE_SELL":
        if quantity < balance[2]:
            final_order = client.order_limit_sell(symbol='WBTCBTC',
                                                  quantity=quantity,
                                                  price=price)
            print("YAYYYYY - put in an order to SELL", final_order["origQty"],
                  "WBTC for", final_order["price"], "BTC a pop!!!")
            return final_order

        else:
            print("insufficient balance to sell. Have", balance[0], "WBTC but need",
                  quantity)
            return None

    if side == "SIDE_BUY":
        if quantity * price < balance[0]:
            final_order = client.order_limit_buy(symbol='WBTCBTC',
                                                 quantity=quantity,
                                                 price=price)
            print("YAYYYYY - put in an order to BUY", final_order["origQty"],
                  "WBTC for", final_order["price"], "BTC a pop!!!")
            return final_order
        else:
            print("insufficient balance to buy. Have", balance[0], "BTC but need",
                  quantity)
            return None


def check_orders(header: List[float], orders: List[dict],
                 balances: List[float]) -> List[dict]:

    new_orders: List[dict] = []

    price_data = header
    bid = price_data[1]
    ask = price_data[3]

    for i in range(len(orders)):
        order_status = client.get_order(symbol='WBTCBTC',
                                        orderId=orders[i]["orderId"])

        if order_status["status"] == "FILLED":
            if order_status["side"] == "SELL":
                new_order = create_order(price_data, bid, ask, "SIDE_BUY",
                                         order_status, balances)
            elif order_status["side"] == "BUY":
                new_order = create_order(price_data, bid, ask, "SIDE_SELL",
                                         order_status, balances)
            else:
                raise Exception("no specificed side for order creation\n", order_status)

        else:
            new_order = None

        if new_order:
            del orders[i]
            new_orders.append(new_order)

    orders.extend(new_orders)

    return orders


def main(orders: List[dict]) -> List[dict]:
    head = header(orders)
    bid = head[1]
    ask = head[3]

    balances = get_balances()

    orders = check_orders(head, orders, balances)

    buy_order = create_order(head, bid, ask, "SIDE_BUY", None, balances)
    if buy_order:
        orders.append(buy_order)

    sell_order = create_order(head, bid, ask, "SIDE_SELL", None, balances)
    if sell_order:
        orders.append(sell_order)

    return orders


orders = client.get_open_orders(symbol='WBTCBTC')

main(orders)
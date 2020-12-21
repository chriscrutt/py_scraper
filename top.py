from base import main

from apis import apis

from binance.client import Client

from time import sleep


def init(apis):
    for api in apis:
        client = Client(apis[api]["pub"], apis[api]["priv"])
        orders = client.get_open_orders(symbol='WBTCBTC')
        apis[api]["orders"] = orders
        apis[api]["client"] = client

    return apis


def start(apis):
    apiss = init(apis)
    counter = 0
    while True:
        try:
            for api in apiss:
                print("\n" + api)
                new_orders = main(apiss[api]["client"], apiss[api]["orders"])
                apiss[api]["orders"] = new_orders
                sleep(21)

            counter += 1

            if counter >= 40:
                print("\nrestarting\n")
                start(apis)

        except Exception as e:
            print(f"\n\nmajor error\n\n{e}\n\n")
            sleep(61)
            start(apis)


start(apis)
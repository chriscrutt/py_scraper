from binance.client import Client

from apis import apis

from time import time


def delete(apis):
    print("start")
    for api in apis:
        client = Client(apis[api]["pub"], apis[api]["priv"])
        client.cancel_all_orders(symbol='WBTCBTC')
        print(f"deleted all {api} orders")
        
    print("finished.")
        
delete(apis)
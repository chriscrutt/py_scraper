# Tutorial (or whatever)
## prereques
1. get python 3 (I'm on 3.9.0) - follow [this tut](https://www.tutorialdocs.com/tutorial/python3/setup-guide.html) & find your operating system
    - check your python version by doing `python --version`
        - if it is not python 3 try `python3 --version`
            - if that doesn't work you did something wrong
        - substitute `python` and `pip` for `python3` and `pip3` (respectively) throughout this tut
2. make sure you have the binance api helper module installed
    - `pip install python-binance`
3. create a binance account [here](https://www.binance.com/en/register?ref=50675748)
4. create an api key [here](https://www.binance.com/en/support/articles/360002502072-How-to-create-API)
5. have at least 0.025 BTC in your spot trading account

## file wise
1. clone or download the zip file of this git repo to your computer
2. open this project folder in your favorite [IDE](https://www.techradar.com/best/best-ide-for-python) (I use vs code)
3. create a new file called apis.py
4. paste this into that file:
    ```py
    apis = {
    "acount": {
        "pub":
        "PUBLIC",
        "priv":
        "PRIVATE"
    }
    ```
    substituting `PUBLIC` and `PRIVATE` with your public and private keys, respectively (as well as `account` with a fun name if you'd like)
5. right now the program is defaulted to making at least 0.076% per trade (0.001% over minimum fee)
    - if you are using BNB to take the place of fees, don't change anything
    - if you aren't using BNB (or don't know what this means), change all occurences of `0.00076` to `0.00101` in the `base.py` file
    - if you know what you're doing (or don't), change it to whatever you want

## running
run the program with `python /path/to/py_scraper/top.py` substituting `/path/to` with... the... path to top.py
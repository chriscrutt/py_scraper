# TODO:
## seperate functions
- [x] create UNIX time to readable time func
- [x] round for price of crypto
- [x] round for quantity of crypto
- [x] median function
- [x] finding percent changed function
- [x] sleep func

## api functions
- [x] candles sticks func
- [x] current price func
- [x] is order fulfilled func
- [x] book ticker func (gets current ask and bid)
- [x] balance func
- [x] buy/sell funcs

## other stuff
- [x] seperate page for APIs

## running bot
- [ ] display header
    - [x] time
    - [ ] # open orders
    - [ ] median high/low price
    - [x] and last price
- [ ] get median highs and lows of past 21 days
- [ ] get available & total balance
- [ ] take what is higher, ask or median high price
    - if the percentage difference between that & bid price > 0.16%
        - (wbtc a + wbtc o + (btc a + btc o) / price) / 190 = quantity
        - see if WBTC balance available > quantity
        - create sell order for quantity & highest price
- [ ] take what is lower, bid or median low price
    - if the percentage difference between that & ask price > 0.16%
        - (wbtc a + wbtc o + (btc a + btc o) / price) / 190 = quantity
        - see if BTC balance available > quantity * lowest price
        - create sell order for quantity & lowest price
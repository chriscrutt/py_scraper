from typing import List, Union

from math import ceil, floor


def quant_round(quant: Union[str, float]) -> float:  # pylint: disable=E1136  # pylint/issues/3139
    return floor(float(quant) * 10000) / 10000


def percent_change(new: float, old: float) -> float:
    return (new - old) / old


# get median of an array
def median(candles: List[float]) -> float:

    # creating an array for all highs and lows of candles, as well as volume
    high: List[float] = []
    low: List[float] = []

    # appends highs and lows of candles to respective arrays, as well as volume
    for candle in candles:
        high.append(float(candle[2]))
        low.append(float(candle[3]))

    n = len(candles)
    index = n // 2

    # Sample with an odd number of observations
    if n % 2:
        return sorted(high)[index], sorted(low)[index]

    # Sample with an even number of observations
    return price_round(sum(sorted(high)[index - 1:index + 1]) /
                       2), price_round(
                           sum(sorted(low)[index - 1:index + 1]) / 2)
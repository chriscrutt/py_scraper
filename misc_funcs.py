from typing import List

# get median of an array
def my_median(sample: List[float]) -> float:
    n = len(sample)
    index = n // 2

    # Sample with an odd number of observations
    if n % 2:
        return sorted(sample)[index]

    # Sample with an even number of observations
    return sum(sorted(sample)[index - 1:index + 1]) / 2


def price_round(price: float) -> float:
    return round(price * 100000) / 100000

def quant_round(quant: float) -> float:
    return round(quant * 10000) / 10000

def percent_change(new: float, old: float) -> float:
    return (new - old) / old
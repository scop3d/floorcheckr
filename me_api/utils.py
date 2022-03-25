from collections import Counter
import datetime
import time
import urllib3
import numpy as np


class Utils:
    # parse blocktime to user-friendly time
    def unix_to_date(unix_date: int):
        return datetime.datetime.utcfromtimestamp(unix_date).strftime(
            "%Y-%m-%d %H:%M:%S%p"
        )

    # returns sol
    def lamports_to_sol(lamports: float) -> float:
        return lamports * 0.000000001

    # returns lamports
    def sol_to_lamports(sol: float) -> float:
        return sol * 1000000000

    # returns median of a list
    def median(l: list):
        half = len(l) // 2
        l.sort()
        if not len(l) % 2:
            return (l[half - 1] + l[half]) / 2.0
        return l[half]

    # returns frequency count of a list
    def count(l: list):
        return dict(Counter(l))

    def validate_unit(unit: str):
        if unit.lower() not in ["sol", "lamports"]:
            raise ValueError("unit should be 'sol' or 'lamports'")

    def reject_outliers(data, m=2):
        return abs(data - np.mean(data)) < m * np.std(data)

    def prettify_symbol(symbol: str):
        return symbol.replace("_", " ").strip().title()

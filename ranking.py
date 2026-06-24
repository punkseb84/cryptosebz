# ==========================================================
# RANKING
# V6
# ==========================================================

from config import (
    TREND_WEIGHT,
    RVOL_WEIGHT,
    DISTANCE_WEIGHT
)


# ==========================================================
# CALCOLO SCORE
# ==========================================================

def calculate_score(

    trend_score,
    rvol,
    distance

):

    rvol = min(rvol, 5)

    score = (

        trend_score * TREND_WEIGHT

        +

        rvol * RVOL_WEIGHT

        -

        distance * DISTANCE_WEIGHT

    )

    return round(score, 2)


# ==========================================================
# ORDINA LISTA
# ==========================================================

def sort_by_score(items):

    return sorted(

        items,

        key=lambda x: x["score"],

        reverse=True

    )


# ==========================================================
# TOP N
# ==========================================================

def top(items, limit):

    return sort_by_score(items)[:limit]


# ==========================================================
# CREA RECORD
# ==========================================================

def build_record(

    symbol,

    close,

    resistance,

    support,

    distance,

    trend_score,

    rvol,

    score

):

    return {

        "symbol": symbol,

        "close": close,

        "support": support,

        "resistance": resistance,

        "distance": distance,

        "trend_score": trend_score,

        "rvol": rvol,

        "score": score

    }


# ==========================================================
# WATCHLIST
# ==========================================================

def add_watchlist(

    watchlist,

    record,

    max_distance

):

    if record["distance"] <= max_distance:

        watchlist.append(record)

    return watchlist


# ==========================================================
# PRE LONG
# ==========================================================

def add_prelong(

    prelong,

    record,

    max_distance,

    min_rvol

):

    if (

        record["trend_score"] >= 2

        and

        record["distance"] <= max_distance

        and

        record["rvol"] >= min_rvol

    ):

        prelong.append(record)

    return prelong


# ==========================================================
# ELIMINA DUPLICATI
# ==========================================================

def remove_duplicates(

    watchlist,

    prelong

):

    pre_symbols = {

        item["symbol"]

        for item in prelong

    }

    return [

        item

        for item in watchlist

        if item["symbol"] not in pre_symbols

    ]


# ==========================================================
# DEBUG
# ==========================================================

def print_score(

    symbol,

    score

):

    print(

        f"{symbol}"

        f" | SCORE={score:.2f}"

    )

# ==========================================================
# RANKING
# V6.1
# ==========================================================

from config import (
    TREND_WEIGHT,
    RVOL_WEIGHT,
    DISTANCE_WEIGHT,
    RVOL_CAP
)


# ==========================================================
# CALCOLO SCORE
# ==========================================================

def calculate_score(
    trend_score,
    rvol,
    distance
):

    # Limita il peso del volume
    rvol = min(rvol, RVOL_CAP)

    score = (

        trend_score * TREND_WEIGHT

        +

        rvol * RVOL_WEIGHT

        -

        distance * DISTANCE_WEIGHT

    )

    return round(score, 2)


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
# PRE-LONG
# ==========================================================

def add_prelong(
    pre_long,
    record,
    max_distance,
    min_rvol
):

    trend = record["trend_score"]

    distance = record["distance"]

    rvol = record["rvol"]

    if (

        (
            trend == 3

            or

            (
                trend == 2
                and rvol >= 2
                and distance <= max_distance
            )

        )

        and

        rvol >= min_rvol

    ):

        pre_long.append(record)

    return pre_long


# ==========================================================
# RIMUOVE I DUPLICATI
# ==========================================================

def remove_duplicates(
    watchlist,
    pre_long
):

    pre_symbols = {

        p["symbol"]

        for p in pre_long

    }

    return [

        w

        for w in watchlist

        if w["symbol"] not in pre_symbols

    ]


# ==========================================================
# ORDINA PER SCORE
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
# DEBUG
# ==========================================================

def print_score(record):

    print(

        f"{record['symbol']}"

        f" | Score={record['score']:.1f}"

        f" | Trend={record['trend_score']}/3"

        f" | RVOL={record['rvol']:.2f}"

        f" | Dist={record['distance']:.2f}%"

    )

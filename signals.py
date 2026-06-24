# ==========================================================
# SIGNALS
# V6
# ==========================================================

from patterns import (
    calculate_risk,
    take_profit,
    swing_stop
)


# ==========================================================
# LONG SETUP
# ==========================================================

def build_long_signal(

    symbol,

    entry,

    support,

    candle_low,

    resistance,

    rvol,

    trend_score

):

    if support is not None:

        stop = support

    else:

        stop = candle_low

        risk = calculate_risk(
        entry,
        stop
    )

    if risk <= 0:

        return None

    tp1 = take_profit(
        entry,
        risk,
        2
    )

    tp2 = take_profit(
        entry,
        risk,
        3
    )

    reward = tp1 - entry

    rr = reward / risk

    return {

        "symbol": symbol,

        "entry": entry,

        "stop": stop,

        "tp1": tp1,

        "tp2": tp2,

        "risk": risk,

        "rr": rr,

        "trend_score": trend_score,

        "resistance": resistance,

        "rvol": rvol

    }


# ==========================================================
# LONG CONDITION
# ==========================================================

def is_long(

    trend_score,

    breakout,

    rvol,

    rvol_min

):

    return (

        (
    trend_score == 3
    or
    (
        trend_score == 2
        and rvol >= 2
        and distance <= 1.5
    )
)

        and

        breakout

        and

        rvol >= rvol_min

    )


# ==========================================================
# PRE LONG
# ==========================================================

def is_prelong(

    trend_score,

    distance,

    rvol,

    distance_limit,

    rvol_min

):

    return (

        trend_score >= 2

        and

        distance <= distance_limit

        and

        rvol >= rvol_min

    )


# ==========================================================
# WATCHLIST
# ==========================================================

def is_watchlist(

    distance,

    limit

):

    return distance <= limit


# ==========================================================
# CREA RECORD
# ==========================================================

def signal_record(

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
# DEBUG
# ==========================================================

def print_signal(signal):

    print(

        f"{signal['symbol']}"

        f" LONG"

        f" Entry={signal['entry']:.2f}"

        f" Stop={signal['stop']:.2f}"

        f" TP1={signal['tp1']:.2f}"

        f" TP2={signal['tp2']:.2f}"

    )

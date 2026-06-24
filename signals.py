# ==========================================================
# SIGNALS
# V6.1
# ==========================================================

from config import (
    TP1_RR,
    TP2_RR
)

from patterns import (
    calculate_risk,
    take_profit
)


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

        trend_score >= 2

        and

        breakout

        and

        rvol >= rvol_min

    )


# ==========================================================
# PRE-LONG CONDITION
# ==========================================================

def is_prelong(
    trend_score,
    distance,
    rvol,
    distance_limit,
    rvol_min
):

    return (

        (

            trend_score == 3

            or

            (

                trend_score == 2

                and

                rvol >= 2

            )

        )

        and

        distance <= distance_limit

        and

        rvol >= rvol_min

    )


# ==========================================================
# WATCHLIST CONDITION
# ==========================================================

def is_watchlist(
    distance,
    limit
):

    return distance <= limit


# ==========================================================
# BUILD LONG SIGNAL
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

    # ------------------------------------------
    # STOP LOSS
    # ------------------------------------------

    if support is not None:

        stop = support

    else:

        stop = candle_low

    # ------------------------------------------
    # RISK
    # ------------------------------------------

    risk = calculate_risk(
        entry,
        stop
    )

    if risk <= 0:

        return None

    # ------------------------------------------
    # TAKE PROFIT
    # ------------------------------------------

    tp1 = take_profit(
        entry,
        risk,
        TP1_RR
    )

    tp2 = take_profit(
        entry,
        risk,
        TP2_RR
    )

    reward = tp1 - entry

    rr = reward / risk

    # ------------------------------------------
    # RECORD
    # ------------------------------------------

    return {

        "symbol": symbol,

        "entry": entry,

        "stop": stop,

        "risk": round(risk, 4),

        "tp1": tp1,

        "tp2": tp2,

        "rr": round(rr, 2),

        "trend_score": trend_score,

        "resistance": resistance,

        "rvol": round(rvol, 2)

    }


# ==========================================================
# WATCHLIST RECORD
# ==========================================================

def watchlist_record(
    symbol,
    close,
    support,
    resistance,
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

        "rvol": round(rvol, 2),

        "score": round(score, 2)

    }


# ==========================================================
# PRELONG RECORD
# ==========================================================

def prelong_record(
    symbol,
    close,
    distance,
    trend_score,
    rvol,
    score
):

    return {

        "symbol": symbol,

        "close": close,

        "distance": distance,

        "trend_score": trend_score,

        "rvol": round(rvol, 2),

        "score": round(score, 2)

    }


# ==========================================================
# DEBUG
# ==========================================================

def print_signal(signal):

    print(

        f"{signal['symbol']}"

        f" | Entry={signal['entry']:.2f}"

        f" | Stop={signal['stop']:.2f}"

        f" | TP1={signal['tp1']:.2f}"

        f" | TP2={signal['tp2']:.2f}"

        f" | RR={signal['rr']:.2f}"

    )

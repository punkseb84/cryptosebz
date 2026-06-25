# ==========================================================
# SIGNALS
# V6.1
# ==========================================================

from config import (
    MAX_RESISTANCE_EXTENSION_PERCENT,
    MAX_SIGNAL_RISK_PERCENT,
    MIN_BREAKOUT_BODY_PERCENT,
    MIN_BREAKOUT_CLOSE_ABOVE_RESISTANCE,
    MIN_LONG_TREND_SCORE,
    MIN_SIGNAL_RISK_PERCENT,
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

        trend_score >= MIN_LONG_TREND_SCORE

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

def valid_breakout_quality(
    entry,
    open_price,
    candle_low,
    resistance
):

    if resistance is None or entry <= 0:

        return False

    breakout_extension = ((entry - resistance) / resistance) * 100

    if breakout_extension < MIN_BREAKOUT_CLOSE_ABOVE_RESISTANCE * 100:

        return False

    if breakout_extension > MAX_RESISTANCE_EXTENSION_PERCENT:

        return False

    candle_range = entry - candle_low
    candle_body = entry - open_price

    if candle_range <= 0 or candle_body <= 0:

        return False

    return (candle_body / candle_range) >= MIN_BREAKOUT_BODY_PERCENT


def build_long_signal(
    symbol,
    entry,
    support,
    candle_low,
    resistance,
    rvol,
    trend_score,
    open_price=None
):

    # ------------------------------------------
    # QUALITÀ BREAKOUT
    # ------------------------------------------

    if open_price is not None and not valid_breakout_quality(
        entry,
        open_price,
        candle_low,
        resistance
    ):

        return None

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

    risk_percent = (risk / entry) * 100

    if (
        risk_percent < MIN_SIGNAL_RISK_PERCENT
        or
        risk_percent > MAX_SIGNAL_RISK_PERCENT
    ):

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

        "risk_percent": round(risk_percent, 2),

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

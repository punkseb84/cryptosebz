# ==========================================================
# PATTERNS
# ==========================================================


# ==========================================================
# SWING HIGHS
# ==========================================================

def find_swing_highs(df):

    swing_highs = []

    for i in range(2, len(df) - 2):

        high = float(df.iloc[i]["high"])

        if (
            high > float(df.iloc[i - 1]["high"])
            and high > float(df.iloc[i - 2]["high"])
            and high > float(df.iloc[i + 1]["high"])
            and high > float(df.iloc[i + 2]["high"])
        ):

            swing_highs.append(high)

    return swing_highs


# ==========================================================
# SWING LOWS
# ==========================================================

def find_swing_lows(df):

    swing_lows = []

    for i in range(2, len(df) - 2):

        low = float(df.iloc[i]["low"])

        if (
            low < float(df.iloc[i - 1]["low"])
            and low < float(df.iloc[i - 2]["low"])
            and low < float(df.iloc[i + 1]["low"])
            and low < float(df.iloc[i + 2]["low"])
        ):

            swing_lows.append(low)

    return swing_lows


# ==========================================================
# RESISTENZA VALIDA PIÙ VICINA
# ==========================================================

def valid_resistance(close, swing_highs):

    valid = []

    for level in swing_highs:

        distance = ((level - close) / close) * 100

        if distance >= 1:

            valid.append(level)

    if not valid:

        return None

    return min(valid)


# ==========================================================
# SUPPORTO PIÙ VICINO
# (almeno 0.5% sotto il prezzo)
# ==========================================================

def nearest_support(close, swing_lows):

    supports = [

        level

        for level in swing_lows

        if level < close * 0.995

    ]

    if not supports:

        return None

    return max(supports)


# ==========================================================
# DISTANZA %
# ==========================================================

def distance_percent(price, level):

    if level is None:

        return None

    return ((level - price) / price) * 100


# ==========================================================
# BREAKOUT
# ==========================================================

def breakout(

    previous_close,
    current_close,
    current_open,
    resistance,
    buffer

):

    if resistance is None:

        return False

    return (

        previous_close <= resistance

        and

        current_close > resistance * (1 + buffer)

        and

        current_close > current_open

    )


# ==========================================================
# STOP LOSS
# ==========================================================

def swing_stop(

    support,
    candle_low

):

    if support is not None:

        return support

    return candle_low


# ==========================================================
# RISCHIO
# ==========================================================

def calculate_risk(

    entry,
    stop

):

    return entry - stop


# ==========================================================
# TAKE PROFIT
# ==========================================================

def take_profit(

    entry,
    risk,
    rr

):

    return entry + (risk * rr)


# ==========================================================
# RETEST
# ==========================================================

def retest(

    low,
    resistance,
    tolerance=0.002

):

    if resistance is None:

        return False

    return abs(low - resistance) / resistance <= tolerance


# ==========================================================
# DEBUG
# ==========================================================

def print_levels(

    symbol,
    support,
    resistance

):

    print(

        f"{symbol}"

        f" | Support={support}"

        f" | Resistance={resistance}"

    )

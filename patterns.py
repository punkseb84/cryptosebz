# ==========================================================
# PATTERNS
# V6
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
# RESISTENZA PIU' VICINA
# ==========================================================

def nearest_resistance(close, swing_highs):

    resistances = [

        x

        for x in swing_highs

        if x > close

    ]

    if not resistances:

        return None

    return min(resistances)


# ==========================================================
# SUPPORTO PIU' VICINO
# ==========================================================

def nearest_support(close, swing_lows):

    supports = [

        x

        for x in swing_lows

        if x < close

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

    return (

        (level - price)

        / price

    ) * 100


# ==========================================================
# FILTRO RESISTENZE
# ==========================================================

def valid_resistance(close, swing_highs):

    valid = []

    for level in swing_highs:

        distance = (

            (level - close)

            / close

        ) * 100

        if distance >= 1:

            valid.append(level)

    if not valid:

        return None

    return min(valid)


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

        and current_close > resistance * (1 + buffer)

        and current_close > current_open

    )


# ==========================================================
# RITEST
# (V7)
# ==========================================================

def retest(

    low,

    resistance,

    tolerance=0.002

):

    if resistance is None:

        return False

    return (

        abs(low - resistance)

        / resistance

    ) <= tolerance


# ==========================================================
# STOP SU SWING LOW
# ==========================================================

def swing_stop(

    support,

    fallback_low

):

    if support is None:

        return fallback_low

    return support


# ==========================================================
# RISK
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
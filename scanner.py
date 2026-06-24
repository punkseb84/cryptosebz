from config import (
    COINS,
    WATCHLIST_DISTANCE,
    PRELONG_DISTANCE,
    BREAKOUT_BUFFER,
    RVOL_MIN,
    MAX_WATCHLIST,
    MAX_PRELONG
)

from utils import (
    get_ohlc,
    enough_history,
    log
)

from indicators import (
    add_ema,
    calculate_rvol,
    calculate_trend_score,
    last_candle,
    previous_close
)

from patterns import (
    find_swing_highs,
    find_swing_lows,
    valid_resistance,
    nearest_support,
    distance_percent,
    breakout
)

from ranking import (
    calculate_score,
    build_record,
    add_watchlist,
    add_prelong
)

from signals import (
    is_long,
    build_long_signal
)

from telegram_bot import (
    build_message,
    send_message
)


def run_scanner():

    watchlist = []
    pre_long = []
    signals = []

    for symbol, pair in COINS.items():

        try:

            # =====================================
            # DOWNLOAD DATI
            # =====================================

            df = get_ohlc(pair)

            if not enough_history(df):
                continue

            # =====================================
            # INDICATORI
            # =====================================

            df = add_ema(df)

            candle = last_candle(df)

            close = candle["close"]
            open_price = candle["open"]
            low = candle["low"]

            prev_close = previous_close(df)

            trend_score = calculate_trend_score(df)

            rvol = calculate_rvol(df)

            # =====================================
            # PATTERN
            # =====================================

            swing_highs = find_swing_highs(df)
            swing_lows = find_swing_lows(df)

            resistance = valid_resistance(
                close,
                swing_highs
            )

            if resistance is None:
                continue

            support = nearest_support(
                close,
                swing_lows
            )

            distance = distance_percent(
                close,
                resistance
            )

            if distance is None:
                continue

            # =====================================
            # SCORE
            # =====================================

            score = calculate_score(
                trend_score,
                rvol,
                distance
            )

            record = build_record(
                symbol=symbol,
                close=close,
                resistance=resistance,
                support=support,
                distance=distance,
                trend_score=trend_score,
                rvol=rvol,
                score=score
            )

            # =====================================
            # WATCHLIST
            # =====================================

            watchlist = add_watchlist(
                watchlist,
                record,
                WATCHLIST_DISTANCE
            )

            # =====================================
            # PRE LONG
            # =====================================

            pre_long = add_prelong(
                pre_long,
                record,
                PRELONG_DISTANCE,
                RVOL_MIN
            )

            # =====================================
            # BREAKOUT
            # =====================================

            is_breakout = breakout(
                previous_close=prev_close,
                current_close=close,
                current_open=open_price,
                resistance=resistance,
                buffer=BREAKOUT_BUFFER
            )

            # =====================================
            # LONG
            # =====================================

            if is_long(
                trend_score=trend_score,
                breakout=is_breakout,
                rvol=rvol,
                rvol_min=RVOL_MIN
            ):

                signal = build_long_signal(
                    symbol=symbol,
                    entry=close,
                    support=support,
                    candle_low=low,
                    resistance=resistance,
                    rvol=rvol,
                    trend_score=trend_score
                )

                if signal is not None:
                    signals.append(signal)

            log(
                symbol,
                f"Close={close:.2f} "
                f"Res={resistance:.2f} "
                f"Dist={distance:.2f}% "
                f"RVOL={rvol:.2f}"
            )

        except Exception as e:

            log(symbol, f"Errore: {e}")

    # =====================================================
    # RANKING FINALE
    # =====================================================

    pre_long = sorted(
        pre_long,
        key=lambda x: x["score"],
        reverse=True
    )[:MAX_PRELONG]

    pre_symbols = {
        p["symbol"]
        for p in pre_long
    }

    watchlist = [
        w
        for w in watchlist
        if w["symbol"] not in pre_symbols
    ]

    watchlist = sorted(
        watchlist,
        key=lambda x: x["score"],
        reverse=True
    )[:MAX_WATCHLIST]

    signals = sorted(
        signals,
        key=lambda x: (
            x["trend_score"],
            x["rvol"]
        ),
        reverse=True
    )

    # =====================================================
    # TELEGRAM
    # =====================================================

    message = build_message(

        signals=signals,

        pre_long=pre_long,

        watchlist=watchlist

    )

    send_message(message)

    # =====================================================
    # REPORT FINALE
    # =====================================================

    print()

    print("=" * 60)

    print("SCAN COMPLETATO")

    print(f"LONG      : {len(signals)}")

    print(f"PRE-LONG  : {len(pre_long)}")

    print(f"WATCHLIST : {len(watchlist)}")

    print("=" * 60)

    print()
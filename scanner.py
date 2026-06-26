from config import (
    COINS,
    TIMEFRAME_CONFIRM_15M,
    TIMEFRAME_CONFIRM_1H,
    TIMEFRAME_MAIN,
)

from utils import enough_history, get_ohlc, log

from indicators import add_indicators, average_volume, last_candle, previous_candle

from signals import (
    all_conditions_met,
    build_signal,
    long_conditions,
    previous_support_resistance,
    short_conditions,
    support_resistance,
)

from telegram_bot import build_message, send_message


_sent_signals = set()


def _is_duplicate(signal):
    key = (
        signal["symbol"],
        signal["direction"],
        signal["candle_time"],
    )

    if key in _sent_signals:
        return True

    _sent_signals.add(key)
    return False


def _load_timeframes(pair):
    df_5m = add_indicators(get_ohlc(pair, interval=TIMEFRAME_MAIN))
    df_15m = add_indicators(get_ohlc(pair, interval=TIMEFRAME_CONFIRM_15M))
    df_1h = add_indicators(get_ohlc(pair, interval=TIMEFRAME_CONFIRM_1H))

    return df_5m, df_15m, df_1h


def run_scanner():
    signals = []
    coins_scanned = 0

    for symbol, pair in COINS.items():
        try:
            df_5m, df_15m, df_1h = _load_timeframes(pair)

            if not (
                enough_history(df_5m)
                and enough_history(df_15m)
                and enough_history(df_1h)
            ):
                continue

            candle_5m = last_candle(df_5m)
            previous_5m = previous_candle(df_5m)
            candle_15m = last_candle(df_15m)
            candle_1h = last_candle(df_1h)
            avg_vol = average_volume(df_5m)
            support, resistance = support_resistance(df_5m)
            previous_support, previous_resistance = previous_support_resistance(df_5m)

            coins_scanned += 1

            long_checks = long_conditions(
                candle_5m=candle_5m,
                previous_5m=previous_5m,
                candle_15m=candle_15m,
                candle_1h=candle_1h,
                avg_volume=avg_vol,
                support=support,
                previous_resistance=previous_resistance,
            )

            short_checks = short_conditions(
                candle_5m=candle_5m,
                previous_5m=previous_5m,
                candle_15m=candle_15m,
                candle_1h=candle_1h,
                avg_volume=avg_vol,
                resistance=resistance,
                previous_support=previous_support,
            )

            for direction, checks in (("LONG", long_checks), ("SHORT", short_checks)):
                if all_conditions_met(checks):
                    signal = build_signal(
                        symbol=symbol,
                        direction=direction,
                        entry=candle_5m["close"],
                        atr=candle_5m["atr"],
                        candle_time=candle_5m["time"],
                    )

                    if signal is not None and not _is_duplicate(signal):
                        signals.append(signal)
                        send_message(build_message(signal))

            log(
                symbol,
                f"Close={candle_5m['close']:.2f} RSI={candle_5m['rsi']:.2f} "
                f"MACD_H={candle_5m['macd_hist']:.6f} Vol={candle_5m['volume']:.2f}/{avg_vol:.2f} "
                f"Support={support:.2f} Resistance={resistance:.2f}",
            )

        except Exception as e:
            log(symbol, f"Errore: {e}")

    print()
    print("=" * 60)
    print("SCAN COMPLETATO")
    print(f"COINS   : {coins_scanned}")
    print(f"SEGNALI : {len(signals)}")
    print("=" * 60)
    print()

    return signals

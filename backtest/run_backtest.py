# ==========================================================
# CRYPTO SCANNER BACKTEST
# ==========================================================

import argparse
import os

if not os.environ.get("TELEGRAM_BOT_TOKEN"):
    os.environ["TELEGRAM_BOT_TOKEN"] = "dummy"

if not os.environ.get("TELEGRAM_CHAT_ID"):
    os.environ["TELEGRAM_CHAT_ID"] = "dummy"

from backtest.engine import grid_search, run_backtest
from backtest.loader import load_history
from backtest.report import (
    export_equity_curve_csv,
    export_grid_csv,
    export_trades_csv,
    print_best_grid,
    print_summary,
)


def _float_list(value):

    return [
        float(item.strip())
        for item in value.split(",")
        if item.strip()
    ]


def parse_args():

    parser = argparse.ArgumentParser(
        description="Backtest e Grid Search per Crypto Scanner"
    )

    parser.add_argument("--symbol", default="BTC")
    parser.add_argument("--pair", default="XBTUSD")
    parser.add_argument("--output-dir", default="backtest/reports")
    parser.add_argument("--rvol-min", type=float, default=1.20)
    parser.add_argument("--prelong-distance", type=float, default=1.5)
    parser.add_argument("--breakout-buffer", type=float, default=0.005)
    parser.add_argument("--grid-search", action="store_true")
    parser.add_argument("--rvol-values", default="1.0,1.2,1.5,2.0")
    parser.add_argument("--prelong-values", default="0.75,1.0,1.5,2.0,3.0")
    parser.add_argument("--breakout-values", default="0.0025,0.005,0.0075,0.01")

    return parser.parse_args()


def main():

    args = parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    df = load_history(args.pair)

    backtest = run_backtest(
        symbol=args.symbol,
        df=df,
        rvol_min=args.rvol_min,
        prelong_distance=args.prelong_distance,
        breakout_buffer=args.breakout_buffer,
    )

    trades_path = os.path.join(args.output_dir, "trades.csv")
    equity_path = os.path.join(args.output_dir, "equity_curve.csv")

    export_trades_csv(
        backtest["trades"],
        trades_path,
    )
    export_equity_curve_csv(
        backtest["metrics"]["equity_curve"],
        equity_path,
    )

    print_summary(backtest["metrics"])
    print(f"Report trade esportato: {trades_path}")
    print(f"Equity curve esportata: {equity_path}")

    if args.grid_search:
        results = grid_search(
            symbol=args.symbol,
            df=df,
            rvol_values=_float_list(args.rvol_values),
            prelong_values=_float_list(args.prelong_values),
            breakout_values=_float_list(args.breakout_values),
        )

        grid_path = os.path.join(args.output_dir, "grid_search.csv")
        export_grid_csv(results, grid_path)
        print_best_grid(results)
        print(f"Grid Search esportata: {grid_path}")


if __name__ == "__main__":

    main()

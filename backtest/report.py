# ==========================================================
# BACKTEST REPORT
# ==========================================================

import csv
import json


TRADE_FIELDS = [
    "symbol",
    "entry_time",
    "entry",
    "stop",
    "tp1",
    "tp2",
    "exit_time",
    "exit",
    "exit_reason",
    "profit",
    "profit_percent",
    "rvol",
    "trend_score",
    "resistance",
    "rvol_min",
    "prelong_distance",
    "breakout_buffer",
]


GRID_FIELDS = [
    "symbol",
    "rvol_min",
    "prelong_distance",
    "breakout_buffer",
    "profit_factor",
    "win_rate",
    "net_profit",
    "max_drawdown",
    "trade_count",
]


def export_trades_csv(trades, path):

    with open(path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=TRADE_FIELDS,
        )
        writer.writeheader()
        writer.writerows(trades)


def export_grid_csv(results, path):

    with open(path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=GRID_FIELDS,
        )
        writer.writeheader()
        writer.writerows(results)


def export_equity_curve_csv(curve, path):

    with open(path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["step", "equity"])

        for step, equity in enumerate(curve):
            writer.writerow([step, equity])


def print_summary(metrics):

    printable = dict(metrics)
    printable["equity_curve"] = json.dumps(
        printable.get("equity_curve", [])
    )

    for key, value in printable.items():
        print(f"{key}: {value}")


def print_best_grid(results, limit=10):

    print("\nMigliori combinazioni per Profit Factor")
    print("-" * 80)

    for row in results[:limit]:
        print(
            "RVOL_MIN={rvol_min} | "
            "PRELONG_DISTANCE={prelong_distance} | "
            "BREAKOUT_BUFFER={breakout_buffer} | "
            "PF={profit_factor:.2f} | "
            "WR={win_rate:.2f}% | "
            "NP={net_profit:.2f} | "
            "Trades={trade_count}".format(**row)
        )

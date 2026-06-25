# ==========================================================
# BACKTEST METRICS
# ==========================================================


def profit_factor(trades):

    gross_profit = sum(
        trade["profit"]
        for trade in trades
        if trade["profit"] > 0
    )

    gross_loss = abs(sum(
        trade["profit"]
        for trade in trades
        if trade["profit"] < 0
    ))

    if gross_loss == 0:
        return float("inf") if gross_profit > 0 else 0.0

    return gross_profit / gross_loss


def win_rate(trades):

    if not trades:
        return 0.0

    winners = sum(
        1
        for trade in trades
        if trade["profit"] > 0
    )

    return (winners / len(trades)) * 100


def net_profit(trades):

    return sum(
        trade["profit"]
        for trade in trades
    )


def equity_curve(trades, initial_equity=0.0):

    equity = initial_equity
    curve = [equity]

    for trade in trades:
        equity += trade["profit"]
        curve.append(equity)

    return curve


def max_drawdown(curve):

    if not curve:
        return 0.0

    peak = curve[0]
    worst = 0.0

    for value in curve:
        peak = max(peak, value)
        drawdown = peak - value
        worst = max(worst, drawdown)

    return worst


def calculate_metrics(trades, initial_equity=0.0):

    curve = equity_curve(
        trades,
        initial_equity=initial_equity
    )

    return {
        "profit_factor": profit_factor(trades),
        "win_rate": win_rate(trades),
        "net_profit": net_profit(trades),
        "max_drawdown": max_drawdown(curve),
        "trade_count": len(trades),
        "equity_curve": curve,
    }

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from common import ensure_dirs, load_orders_daily


def _load_forecast(paths) -> pd.DataFrame:
    forecast_path = paths.processed_dir / "forecast_output.csv"
    if not forecast_path.exists():
        return pd.DataFrame()
    return pd.read_csv(forecast_path, parse_dates=["date"])


def _format_pct(value: float) -> str:
    if np.isnan(value):
        return "n/a"
    return f"{value:.1f}%"


def main() -> None:
    paths = ensure_dirs()
    df = load_orders_daily().sort_values("date")

    start_date = df["date"].min().date()
    end_date = df["date"].max().date()
    avg_orders = df["orders"].mean()
    median_orders = df["orders"].median()

    window = min(30, len(df) // 2)
    early_avg = df["orders"].iloc[:window].mean()
    late_avg = df["orders"].iloc[-window:].mean()
    growth_pct = (late_avg - early_avg) / early_avg * 100 if early_avg else float("nan")

    df["weekday"] = df["date"].dt.day_name()
    weekday_avg = df.groupby("weekday")["orders"].mean()
    top_day = weekday_avg.idxmax()
    top_day_value = weekday_avg.max()

    rolling_std = df["orders"].rolling(7).std()
    early_vol = rolling_std.iloc[:window].mean()
    late_vol = rolling_std.iloc[-window:].mean()
    vol_change_pct = (late_vol - early_vol) / early_vol * 100 if early_vol else float("nan")

    forecast_df = _load_forecast(paths)
    forecast_summary = "Forecast data not generated yet."
    if not forecast_df.empty:
        next_7 = forecast_df.head(7)["forecast"].mean()
        next_14 = forecast_df.head(14)["forecast"].mean()
        next_30 = forecast_df.head(30)["forecast"].mean()
        forecast_summary = (
            f"Expected avg daily orders: 7d={next_7:.0f}, "
            f"14d={next_14:.0f}, 30d={next_30:.0f}."
        )

    insights = [
        f"Data range: {start_date} to {end_date}.",
        f"Average daily orders: {avg_orders:.1f} (median {median_orders:.1f}).",
        f"Demand change: {_format_pct(growth_pct)} from early vs late period.",
        f"Strongest weekday: {top_day} (avg {top_day_value:.1f} orders).",
        f"Volatility change (7d std): {_format_pct(vol_change_pct)}.",
        forecast_summary,
    ]

    recommendations = [
        "Align staffing and fulfillment capacity with weekly peaks.",
        "Watch high-volatility weeks for inventory and SLA risk.",
        "Use the 30-day forecast to stage promotions and logistics capacity.",
        "Monitor for shifts in weekday pattern as an early warning signal.",
    ]

    insights_path = paths.reports_dir / "insights.md"
    with insights_path.open("w", encoding="utf-8") as f:
        f.write("# Key Insights\n\n")
        for item in insights:
            f.write(f"- {item}\n")

    recommendations_path = paths.reports_dir / "recommendations.md"
    with recommendations_path.open("w", encoding="utf-8") as f:
        f.write("# Recommendations\n\n")
        for item in recommendations:
            f.write(f"- {item}\n")


if __name__ == "__main__":
    main()

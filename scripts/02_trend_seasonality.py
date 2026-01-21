from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from common import load_orders_daily, save_figure


def main() -> None:
    sns.set_theme(style="whitegrid")
    df = load_orders_daily()
    df = df.sort_values("date")

    df["rolling_7d"] = df["orders"].rolling(7).mean()
    df["rolling_30d"] = df["orders"].rolling(30).mean()

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["date"], df["orders"], color="#94a3b8", linewidth=1, label="Actual")
    ax.plot(df["date"], df["rolling_7d"], color="#2563eb", linewidth=1.5, label="7D MA")
    ax.plot(df["date"], df["rolling_30d"], color="#16a34a", linewidth=1.5, label="30D MA")
    ax.set_title("Trend with Rolling Means")
    ax.set_xlabel("Date")
    ax.set_ylabel("Orders")
    ax.legend()
    save_figure(fig, "trend_rolling_means.png")
    plt.close(fig)

    df["weekday"] = df["date"].dt.day_name()
    weekday_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    weekday_avg = (
        df.groupby("weekday")["orders"].mean().reindex(weekday_order)
    )

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(x=weekday_avg.index, y=weekday_avg.values, ax=ax, color="#2563eb")
    ax.set_title("Average Orders by Weekday")
    ax.set_xlabel("Weekday")
    ax.set_ylabel("Average Orders")
    ax.tick_params(axis="x", rotation=30)
    save_figure(fig, "weekday_average_orders.png")
    plt.close(fig)


if __name__ == "__main__":
    main()

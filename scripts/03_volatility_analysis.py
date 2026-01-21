from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from common import ensure_dirs, load_orders_daily, save_figure


def main() -> None:
    sns.set_theme(style="whitegrid")
    df = load_orders_daily()
    df = df.sort_values("date")

    df["rolling_std_7d"] = df["orders"].rolling(7).std()
    df["rolling_std_30d"] = df["orders"].rolling(30).std()

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["date"], df["rolling_std_7d"], color="#ef4444", label="7D Std")
    ax.plot(df["date"], df["rolling_std_30d"], color="#f97316", label="30D Std")
    ax.set_title("Rolling Volatility (Std Dev)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Orders Std Dev")
    ax.legend()
    save_figure(fig, "rolling_volatility.png")
    plt.close(fig)

    threshold = df["rolling_std_7d"].quantile(0.95)
    high_vol = df[df["rolling_std_7d"] >= threshold][
        ["date", "orders", "rolling_std_7d"]
    ].dropna(subset=["rolling_std_7d"])

    paths = ensure_dirs()
    high_vol.to_csv(paths.reports_dir / "volatility_windows.csv", index=False)


if __name__ == "__main__":
    main()

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from common import load_orders_daily, save_figure


def main() -> None:
    sns.set_theme(style="whitegrid")
    df = load_orders_daily()

    print("Rows:", len(df))
    print("Date range:", df["date"].min(), "to", df["date"].max())
    print("Missing values:\n", df.isna().sum())
    duplicates = df.duplicated(subset=["date"]).sum()
    print("Duplicate dates:", duplicates)
    print("Summary stats:\n", df["orders"].describe())

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["date"], df["orders"], color="#2563eb", linewidth=1)
    ax.set_title("Daily Orders Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Orders")
    save_figure(fig, "orders_over_time.png")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.histplot(df["orders"], bins=30, kde=True, ax=ax, color="#16a34a")
    ax.set_title("Distribution of Daily Orders")
    ax.set_xlabel("Orders")
    save_figure(fig, "orders_distribution.png")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(4, 4))
    sns.boxplot(y=df["orders"], ax=ax, color="#f97316")
    ax.set_title("Daily Orders Boxplot")
    ax.set_ylabel("Orders")
    save_figure(fig, "orders_boxplot.png")
    plt.close(fig)


if __name__ == "__main__":
    main()

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from statsmodels.tsa.holtwinters import ExponentialSmoothing, SimpleExpSmoothing

from common import ensure_dirs, load_orders_daily, mape, save_figure


@dataclass
class ForecastResult:
    model_name: str
    forecast: pd.Series
    lower: pd.Series
    upper: pd.Series


def _split_train_test(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    if len(df) >= 120:
        test_size = 30
    elif len(df) >= 60:
        test_size = 21
    else:
        test_size = max(7, int(len(df) * 0.2))
    train = df.iloc[:-test_size]
    test = df.iloc[-test_size:]
    return train, test


def _baseline_forecast(df: pd.DataFrame) -> pd.Series:
    return df["orders"].rolling(7).mean().shift(1)


def _fit_ets(train: pd.Series, seasonal_periods: int = 7) -> ExponentialSmoothing:
    try:
        model = ExponentialSmoothing(
            train,
            trend="add",
            seasonal="add",
            seasonal_periods=seasonal_periods,
        )
        return model.fit(optimized=True)
    except Exception:
        return SimpleExpSmoothing(train).fit(optimized=True)


def _prediction_interval(forecast: pd.Series, residuals: pd.Series) -> Tuple[pd.Series, pd.Series]:
    sigma = np.nanstd(residuals)
    lower = forecast - 1.96 * sigma
    upper = forecast + 1.96 * sigma
    lower = lower.clip(lower=0)
    return lower, upper


def main() -> None:
    sns.set_theme(style="whitegrid")
    df = load_orders_daily().sort_values("date")
    df = df.set_index("date").asfreq("D")
    if df["orders"].isna().any():
        # Fill missing calendar days to preserve daily frequency for ETS.
        df["orders"] = df["orders"].fillna(0)

    train, test = _split_train_test(df)
    baseline_series = _baseline_forecast(df)

    baseline_test = baseline_series.loc[test.index]
    baseline_mask = baseline_test.notna()
    if baseline_mask.any():
        baseline_mae = np.mean(
            np.abs(test.loc[baseline_mask, "orders"] - baseline_test[baseline_mask])
        )
        baseline_mape = mape(
            test.loc[baseline_mask, "orders"].values,
            baseline_test[baseline_mask].values,
        )
    else:
        baseline_mae = float("nan")
        baseline_mape = float("nan")

    ets_model = _fit_ets(train["orders"])
    ets_test_forecast = ets_model.forecast(len(test))

    ets_mae = np.mean(np.abs(test["orders"] - ets_test_forecast))
    ets_mape = mape(test["orders"].values, ets_test_forecast.values)

    horizon = 30
    future_forecast = ets_model.forecast(horizon)
    future_index = pd.date_range(df.index.max() + pd.Timedelta(days=1), periods=horizon)
    future_forecast.index = future_index

    residuals = train["orders"] - ets_model.fittedvalues
    lower, upper = _prediction_interval(future_forecast, residuals)

    results = [
        ForecastResult(
            model_name="ets",
            forecast=future_forecast,
            lower=lower,
            upper=upper,
        )
    ]

    paths = ensure_dirs()
    output_rows = []
    for result in results:
        for date, value in result.forecast.items():
            output_rows.append(
                {
                    "date": date.date(),
                    "forecast": float(value),
                    "lower": float(result.lower.loc[date]),
                    "upper": float(result.upper.loc[date]),
                    "model": result.model_name,
                }
            )
    output_df = pd.DataFrame(output_rows)
    output_path = paths.processed_dir / "forecast_output.csv"
    output_df.to_csv(output_path, index=False)

    metrics_df = pd.DataFrame(
        [
            {
                "model": "baseline_7d_ma",
                "mae": baseline_mae,
                "mape": baseline_mape,
            },
            {
                "model": "ets",
                "mae": ets_mae,
                "mape": ets_mape,
            },
        ]
    )
    metrics_df.to_csv(paths.reports_dir / "forecast_metrics.csv", index=False)

    fig, ax = plt.subplots(figsize=(10, 4))
    window_start = max(0, len(df) - 120)
    recent = df.iloc[window_start:]
    ax.plot(recent.index, recent["orders"], label="Actual", color="#1f2937", linewidth=1)
    ax.plot(test.index, ets_test_forecast, label="ETS (Test)", color="#2563eb")
    ax.plot(test.index, baseline_test, label="7D MA Baseline", color="#16a34a")
    ax.set_title("Test Forecast vs Actual")
    ax.set_xlabel("Date")
    ax.set_ylabel("Orders")
    ax.legend()
    save_figure(fig, "forecast_test_comparison.png")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(recent.index, recent["orders"], label="Actual", color="#1f2937", linewidth=1)
    ax.plot(future_index, future_forecast, label="ETS Forecast", color="#2563eb")
    ax.fill_between(future_index, lower, upper, color="#93c5fd", alpha=0.3)
    ax.set_title("30-Day Demand Forecast")
    ax.set_xlabel("Date")
    ax.set_ylabel("Orders")
    ax.legend()
    save_figure(fig, "forecast_30_day.png")
    plt.close(fig)


if __name__ == "__main__":
    main()

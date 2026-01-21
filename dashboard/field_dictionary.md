# Tableau Field Dictionary

This project uses pre-aggregated daily orders and forecast outputs. The fields below are designed for Tableau.

## Data Sources

### CSV tables (Tableau Public workflow)
- orders_daily.csv
- forecast_output.csv

### data/processed/orders_daily.csv
- date (Date): Order purchase date (daily grain).
- orders (Number): Daily order count after filtering canceled/unavailable.

### data/processed/forecast_output.csv
- date (Date): Forecast date (future days).
- forecast (Number): Point forecast for daily orders.
- lower (Number): 95% lower bound.
- upper (Number): 95% upper bound.
- model (String): Forecast model name (default: ets).

### reports/forecast_metrics.csv (optional KPI sheet)
- model (String): Model name.
- mae (Number): Mean absolute error on test window.
- mape (Number): Mean absolute percentage error on test window.

### reports/volatility_windows.csv (optional)
- date (Date): Date of high volatility.
- orders (Number): Orders on that date.
- rolling_std_7d (Number): 7-day rolling std dev.

## Recommended Calculated Fields (Tableau)

Use these on `orders_daily.csv`.

- Weekday
  - `DATENAME('weekday', [date])`

- Month
  - `DATENAME('month', [date])`

- 7D Moving Average
  - `WINDOW_AVG(SUM([orders]), -6, 0)`

- 30D Moving Average
  - `WINDOW_AVG(SUM([orders]), -29, 0)`

- 7D Rolling Std
  - `WINDOW_STDEV(SUM([orders]), -6, 0)`

- Latest Date
  - `WINDOW_MAX(MAX([date]))`

- Latest Orders
  - `IF MAX([date]) = WINDOW_MAX(MAX([date])) THEN SUM([orders]) END`

## Join / Relationship Guidance
- For historical charts, use `orders_daily` only.
- For forecast charts, use `forecast_output` as the primary source.
- To overlay actuals on forecast, blend `orders_daily` to `forecast_output` using `date`.

# Tableau Postgres Setup (Public Edition)

Tableau Public does not support the PostgreSQL connector. Use the Hyper extracts instead:
- `dashboard/extracts/orders_daily.hyper`
- `dashboard/extracts/forecast_output.hyper`

## 2) Ensure CSVs exist
The template packages extracts built from:
- `data/processed/orders_daily.csv`
- `data/processed/forecast_output.csv`

## 3) Open in Tableau
- Open Tableau Desktop Public Edition
- Connect -> Hyper -> select `dashboard/extracts/orders_daily.hyper`
- Add another data source -> Hyper -> select `dashboard/extracts/forecast_output.hyper`
Note: Build the dashboards using `dashboard/dashboard_template.md`.

## 4) Build dashboards
Use `dashboard/dashboard_template.md` to create the 3 dashboards:
- Demand Overview
- Volatility & Stability
- Forecast Outlook

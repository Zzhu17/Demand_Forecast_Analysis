# Tableau Dashboard Template (Multi-Dashboard)

Use a 3-dashboard workbook so the narrative is clearer and the layout feels less crowded.

## Data Sources
- Primary (historical): `data/processed/orders_daily.csv`
- Forecast: `data/processed/forecast_output.csv`
- Optional KPIs: `reports/forecast_metrics.csv`

## Dashboard 1: Demand Overview

### Header KPI Strip
- Latest Date
- Latest Orders
- 7D Avg Orders
- 30D Avg Orders

### Main Area (two-column)
Left:
- Daily Orders Trend (line)
- Add 7D and 30D moving averages (table calcs)

Right:
- Weekday Seasonality (bar)
- Monthly Seasonality (bar or heatmap)

### Filters
- Date range

## Dashboard 2: Volatility & Stability

### Top Row
- Rolling Volatility (7D std line)

### Bottom Row
- High Volatility Dates (table using `reports/volatility_windows.csv`)
- Optional: Boxplot of daily orders

### Filters
- Date range

## Dashboard 3: Forecast Outlook

### Main Area
- Forecast Line with Prediction Band (forecast_output.csv)
- Optional overlay: last 30 days of actuals (blend with orders_daily.csv)

### Side Panel
- Forecast KPIs: next 7/14/30 day average
- Model metrics table (from `forecast_metrics.csv`)

### Filters
- Model (if multiple)

## Styling Notes
- Keep a clean, light theme for DA presentation.
- Use consistent colors:
  - Actual: dark gray (#1F2937)
  - 7D MA: blue (#2563EB)
  - 30D MA: green (#16A34A)
  - Forecast: blue (#2563EB)
  - Interval band: light blue (#93C5FD, 30% opacity)

## Export
- Export dashboard images to `dashboard/` for reporting.

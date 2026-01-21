<<<<<<< HEAD
# Demand_Forecast_Analysis
=======
# E-Commerce Demand Analysis & Forecasting

## Project Overview
DA-style demand analysis for an e-commerce business. The goal is to understand historical demand behavior, quantify trend/seasonality/volatility, and produce a reasonable short-term forecast that can be turned into operational guidance. This project prioritizes clarity and business usefulness over model complexity.

## Analysis Direction (DA)
- Understand demand evolution over time
- Identify weekly/monthly seasonality
- Measure volatility shifts and risk periods
- Build short-term demand expectations (7/14/30 days)
- Translate insights into operational recommendations

## Business Questions
- Is order volume growing or stabilizing?
- Is there clear weekly or monthly seasonality?
- Is demand volatility increasing?
- What is the short-term demand outlook (7/14/30 days)?
- What does this imply for operations and logistics?

## Data & KPI
Source: Olist public dataset (orders table).
- Grain: daily
- KPI: daily order count
- Key field: `order_purchase_timestamp`
- Filtering: excludes `canceled` and `unavailable` orders (adjust if needed)

Raw data: `raw/olist_orders_dataset.csv`

## Methods (SQL + Python)
SQL (PostgreSQL):
- Build daily aggregates for downstream analysis and Tableau.

Python:
- EDA and data quality checks
- Rolling trends (7d/30d) and weekday seasonality
- Rolling volatility (7d std) and high-volatility windows
- Forecasting: baseline (7d moving average) vs ETS, with metrics
- Business insights and recommendations from findings

Scripts:
1. `scripts/01_eda_orders.py`
2. `scripts/02_trend_seasonality.py`
3. `scripts/03_volatility_analysis.py`
4. `scripts/04_demand_forecast.py`
5. `scripts/05_business_insights.py`

## Key Findings
From `reports/insights.md`:
- Data range: 2016-09-04 to 2018-09-03
- Average daily orders: 159.9 (median 148.0)
- Demand change: 882.0% from early vs late period
- Strongest weekday: Tuesday (avg 181.1 orders)
- Volatility change (7d std): 381.7%

## Forecast Summary
Short-term expectations (from `reports/insights.md`):
- 7d avg: ~300 orders/day
- 14d avg: ~301 orders/day
- 30d avg: ~305 orders/day

Forecast output: `data/processed/forecast_output.csv`  
Metrics: `reports/forecast_metrics.csv`

## Tableau Output
Use CSVs in Tableau Public:
- `data/processed/orders_daily.csv`
- `data/processed/forecast_output.csv`

Dashboards (PNG exports):
- `reports/Dashboard1.png` (trend + moving averages + weekday seasonality)
- `reports/Dashboard2.png` (volatility + boxplot)
- `reports/Dashboard3.png` (forecast line + prediction band)

Tableau reference:
- Field dictionary: `dashboard/field_dictionary.md`
- Dashboard layout notes: `dashboard/dashboard_template.md`

Tableau Public extracts (optional):
- `dashboard/extracts/orders_daily.hyper`
- `dashboard/extracts/forecast_output.hyper`

## SQL Workflow (PostgreSQL)
From repo root:
```
psql -d <db_name> -f sql/01_daily_orders.sql
```
This writes: `data/processed/orders_daily.csv`

Forecast output table:
```
psql -d <db_name> -f sql/02_forecast_output.sql
```

## Setup
Create a virtual environment and install dependencies:
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run Analysis
```
python scripts/01_eda_orders.py
python scripts/02_trend_seasonality.py
python scripts/03_volatility_analysis.py
python scripts/04_demand_forecast.py
python scripts/05_business_insights.py
```

Outputs:
- Charts: `reports/figures/*.png`
- Forecast data: `data/processed/forecast_output.csv`
- Insights: `reports/insights.md`, `reports/recommendations.md`

## Project Structure
```
Demand_Forecast_Analysis/
├── raw/
├── data/
│   └── processed/
├── sql/
├── scripts/
├── reports/
│   └── figures/
├── dashboard/
├── README.md
└── requirements.txt
```

## Notes
- If `data/processed/orders_daily.csv` is missing, scripts will build it from `raw/olist_orders_dataset.csv` using the same filtering rule.
- Adjust the SQL filter to include/exclude order statuses based on your business definition.
- `scripts/04_demand_forecast.py` fills missing calendar days with 0 orders to preserve daily frequency.

## Next Steps (Optional)
- Add GMV and order item volume forecasts
- Tag anomalies/holidays for more explainable volatility spikes
>>>>>>> 664a4cc (Update)

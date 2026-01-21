
# Demand_Forecast_Analysis
# Demand Forecast Analysis (Business-Oriented)

Status
- Demand forecasting pipeline complete
- Model evaluation and error analysis implemented
- Business interpretation and scenario analysis added

## Project Overview
This project simulates a demand forecasting analysis workflow commonly used in e-commerce and supply chain planning. The goal is to understand historical demand behavior, quantify trend/seasonality/volatility, and produce a short-term forecast that can be translated into operational guidance. The priority is business usability over model complexity.

## Business Context & Objective
Demand forecasting here is not about maximizing model accuracy alone. The objective is to:
- Support inventory planning
- Reduce stockout risk
- Control excess inventory and holding costs
- Improve operational stability under seasonal demand patterns

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

## Forecasting Use Case
The forecast is intended to support medium-term planning decisions, such as:
- How much inventory to allocate for upcoming periods
- How to prepare for seasonal demand spikes
- How to balance service level against inventory cost

The output is designed to be interpretable and stable enough for operational use.

## Data & KPI
Source: Olist public dataset (orders table).
- Grain: daily
- KPI: daily order count
- Key field: `order_purchase_timestamp`
- Filtering: excludes `canceled` and `unavailable` orders (adjust if needed)
No external demand signals (promotions/pricing) are assumed.

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

## Forecasting Approach
Time-series forecasting models are trained on historical demand data. Model selection prioritizes:
- Interpretability
- Stability
- Ease of operational integration

Rather than optimizing for a single metric, the focus is on forecast behavior under different demand conditions.

## Evaluation Metrics
Forecast accuracy is evaluated using standard error metrics:
- MAE
- MAPE

These metrics are used to compare forecast performance, not as the sole decision criterion.

## Forecast Summary
Short-term expectations (from `reports/insights.md`):
- 7d avg: ~300 orders/day
- 14d avg: ~301 orders/day
- 30d avg: ~305 orders/day

Forecast output: `data/processed/forecast_output.csv`  
Metrics: `reports/forecast_metrics.csv`

## Forecast Error & Business Impact Mapping
Forecast errors translate directly into business risks:

| Forecast Error Type | Business Impact |
| --- | --- |
| Under-forecast | Stockouts, lost sales, reduced customer satisfaction |
| Over-forecast | Excess inventory, higher holding costs, capital lock-up |

As a result, forecasting decisions must consider error asymmetry, not just average accuracy.

## Scenario Analysis
To reflect real-world planning trade-offs, forecast results are interpreted under different scenarios:

- Conservative Forecast  
  Prioritizes stability and lower variance  
  → Lower stockout risk, higher inventory holding cost

- Aggressive Forecast  
  More responsive to recent demand changes  
  → Lower holding cost, higher risk of stockouts

This framing mirrors how forecasts are discussed in operational planning meetings.

## Business Implications
- Forecasts should align with service level targets, not just accuracy metrics
- Conservative forecasts may be preferred during peak seasons
- More aggressive forecasts may be acceptable during stable demand periods
- Forecast interpretation is as important as model selection

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
=======
## Limitations & Next Steps
- No real-time demand signals are included
- Forecasts are evaluated offline

Future improvements may include:
- Incorporating external drivers (promotions, pricing)
- Cost-weighted error metrics
- Integration with inventory optimization models

## Reproducibility
- Data preparation: `scripts/01_eda_orders.py`
- Trend/seasonality: `scripts/02_trend_seasonality.py`
- Volatility: `scripts/03_volatility_analysis.py`
- Forecasting: `scripts/04_demand_forecast.py`
- Business insights: `scripts/05_business_insights.py`

## Why This Reflects Real-World Practice
- Forecasting is framed as decision support
- Accuracy metrics are linked to operational risk
- Trade-offs are explicitly discussed
- Model complexity is secondary to business usability

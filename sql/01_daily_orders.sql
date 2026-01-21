-- Build daily orders table from Olist orders CSV.
-- Run from repo root:
--   psql -d <db_name> -f sql/01_daily_orders.sql

DROP TABLE IF EXISTS raw_orders;
CREATE TABLE raw_orders (
    order_id TEXT,
    customer_id TEXT,
    order_status TEXT,
    order_purchase_timestamp TIMESTAMP,
    order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP
);

\copy raw_orders FROM 'raw/olist_orders_dataset.csv' WITH (FORMAT csv, HEADER true);

DROP TABLE IF EXISTS orders_daily;
CREATE TABLE orders_daily AS
SELECT
    DATE(order_purchase_timestamp) AS date,
    COUNT(*) AS orders
FROM raw_orders
WHERE order_purchase_timestamp IS NOT NULL
  AND order_status NOT IN ('canceled', 'unavailable')
GROUP BY 1
ORDER BY 1;

\copy orders_daily TO 'data/processed/orders_daily.csv' WITH (FORMAT csv, HEADER true);

-- Load forecast output from CSV into Postgres.
-- Run after generating data/processed/forecast_output.csv.
--   psql -d <db_name> -f sql/02_forecast_output.sql

DROP TABLE IF EXISTS forecast_output;
CREATE TABLE forecast_output (
    date DATE,
    forecast DOUBLE PRECISION,
    lower DOUBLE PRECISION,
    upper DOUBLE PRECISION,
    model TEXT
);

\copy forecast_output FROM 'data/processed/forecast_output.csv' WITH (FORMAT csv, HEADER true);

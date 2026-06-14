# retail-customer360-snowflake-dbt-airflow

# Retail Customer 360 Data Platform

Production-style demo retail data engineering project using Snowflake, dbt, Airflow, Azure Blob Storage and Python.

## Objective

Build a Customer 360 analytics platform integrating POS sales, customer master, product CDC, loyalty events, inventory snapshots, promotions and store assortment data.

## Key Engineering Patterns

- Batch file ingestion
- API JSON ingestion
- CDC-style product changes
- Snowflake raw, curated and consumption layers
- dbt staging, intermediate and marts
- SCD Type 2 dimensions
- Incremental fact loading
- Data quality checks
- Audit and control tables
- Environment-driven deployment
- Airflow orchestration

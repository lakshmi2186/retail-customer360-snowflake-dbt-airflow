# Retail Customer 360 Data Platform Architecture

## 1. Architecture Overview

The Retail Customer 360 Data Platform provides a governed analytics environment for customer, sales, product, loyalty, inventory and replenishment reporting.

The platform follows a layered architecture pattern consisting of:

* Source Systems
* Cloud Landing Zone
* Snowflake Data Platform
* dbt Transformation Layer
* Business Consumption Layer
* Orchestration Layer
* Governance and Audit Framework

The solution is designed to support scalable batch processing, CDC-based ingestion, dimensional modelling, data quality validation and environment-driven deployments.

---

## 2. High Level Architecture

```text
Source Systems
       │
       ▼
Azure Blob Storage
       │
       ▼
Snowflake RAW Layer
       │
       ▼
dbt Staging Models
       │
       ▼
dbt Intermediate Models
       │
       ▼
dbt Dimensions and Facts
       │
       ▼
Business Consumption Marts
       │
       ▼
Reporting and Analytics Consumers
```

Apache Airflow orchestrates ingestion, transformation, testing and monitoring activities.

---

## 3. Source Systems

### POS Transactions

Purpose:

Store sales transactions.

Pattern:

Daily batch files.

Format:

CSV

---

### Customer Master

Purpose:

Customer profile and loyalty membership information.

Pattern:

Daily extract.

Format:

CSV

---

### Product Master

Purpose:

Product catalogue, supplier and pricing information.

Pattern:

CDC-based ingestion.

Format:

Database CDC feed.

---

### Loyalty Events

Purpose:

Points earned, redeemed and expired.

Pattern:

API ingestion.

Format:

JSON

---

### Inventory Snapshot

Purpose:

Daily stock position.

Pattern:

Daily ingestion.

Format:

JSON

---

### Promotions

Purpose:

Promotion and discount information.

Pattern:

Daily ingestion.

Format:

JSON

---

### Store Product Assortment

Purpose:

Store ranging information.

Pattern:

Incremental batch ingestion.

Format:

CSV

---

## 4. Landing Zone Architecture

Azure Blob Storage acts as the enterprise landing zone.

Container Structure:

```text
landing/
    pos/
    customer/
    inventory/
    promotions/
    assortment/

api/
    flybuys/

archive/

rejected/
```

Landing Zone Responsibilities:

* Source system decoupling
* Historical file retention
* Replay and reprocessing support
* File validation
* Audit tracking

---

## 5. Snowflake Architecture

Environment isolation is implemented at the database level.

```text
RETAIL_DEV
RETAIL_TEST
RETAIL_PROD
```

Each database contains the following schemas.

### RAW

Stores source-aligned data with minimal transformation.

Examples:

```text
raw_pos_transactions
raw_customer_master
raw_product_cdc
raw_inventory_snapshot
raw_flybuys_events
```

---

### CURATED

Stores cleansed and transformed data.

Contains:

* Staging models
* Intermediate models

Examples:

```text
stg_pos_transactions
stg_customers
int_sales_enriched
```

---

### CONSUMPTION

Stores dimensional models and business marts.

Contains:

* Dimensions
* Facts
* Business marts

Examples:

```text
dim_customer_scd2
dim_product_scd2
fact_sales
mart_customer_360
```

---

### AUDIT

Stores operational metadata.

Examples:

```text
audit_file_load
audit_pipeline_run
audit_data_quality
```

---

### CONFIG

Stores configuration-driven metadata.

Examples:

```text
pipeline_config
dq_rule_config
environment_config
```

---

## 6. dbt Architecture

The transformation layer is implemented using dbt Core.

Project Structure:

```text
models/

    staging/

    intermediate/

    marts/

        dimensions/

        facts/

        business/
```

### Staging Layer

Responsibilities:

* Standardisation
* Data type conversions
* JSON flattening
* Deduplication

---

### Intermediate Layer

Responsibilities:

* Business logic
* Reusable transformations
* Data enrichment

---

### Marts Layer

Responsibilities:

* Dimensional modelling
* Fact table creation
* Business metric calculations

---

## 7. Dimensional Model Architecture

### Dimensions

```text
dim_customer_scd2
dim_customer_current

dim_product_scd2
dim_product_current

dim_store
dim_date
```

### Facts

```text
fact_sales

fact_loyalty_activity

fact_inventory_snapshot

fact_store_product_assortment_snapshot
```

### Business Marts

```text
mart_customer_360

mart_daily_sales_comparison

mart_store_gap_scan

mart_replenishment_recommendation

mart_loyalty_customer_value
```

---

## 8. Orchestration Architecture

Apache Airflow controls all platform workflows.

Daily Pipeline:

```text
Validate Source Files
        │
        ▼
Load RAW Layer
        │
        ▼
Run dbt Staging
        │
        ▼
Run dbt Intermediate
        │
        ▼
Run dbt Dimensions
        │
        ▼
Run dbt Facts
        │
        ▼
Run dbt Marts
        │
        ▼
Run Data Quality Tests
        │
        ▼
Publish Results
```

---

## 9. Audit and Monitoring Framework

All platform executions are audited.

### File Audit

```text
file_name
source_system
record_count
load_status
load_timestamp
```

### Pipeline Audit

```text
pipeline_name
run_id
status
start_time
end_time
```

### Data Quality Audit

```text
rule_name
status
failed_records
validation_timestamp
```

---

## 10. Security and Governance

Security controls include:

* Role-based access control
* Environment isolation
* Least privilege access
* Audit logging
* Source-to-target lineage

Customer-sensitive information is exposed through controlled reporting views.

---

## 11. Deployment Strategy

Deployment is environment-driven.

```text
DEV
   │
   ▼
TEST
   │
   ▼
PROD
```

Deployment principles:

* Source controlled code
* Pull request approvals
* Automated validation
* Environment-specific configuration
* Controlled production releases

---

## 12. Future Enhancements

Potential future enhancements include:

* Snowpipe Streaming
* Real-time loyalty event ingestion
* Event-driven architectures
* Dynamic Tables
* Machine learning based replenishment recommendations
* Data observability integration

```sql
-- ============================================================
-- Script: 003_create_raw_tables.sql
-- Purpose: Create source-aligned RAW tables
-- Project: Retail Customer 360 Data Platform
-- Environment: Development
-- ============================================================

USE DATABASE RETAIL_DEV;
USE SCHEMA RAW;


-- ============================================================
-- 1. STORE MASTER
-- Grain: One row per store
-- Source format: CSV
-- ============================================================

CREATE TABLE IF NOT EXISTS RAW_STORE_MASTER (
    store_id               VARCHAR(20),
    store_name             VARCHAR(200),
    state                  VARCHAR(10),
    region                 VARCHAR(100),
    postcode               VARCHAR(10),
    store_format           VARCHAR(50),
    opening_date           DATE,
    active_flag            VARCHAR(1),

    source_file_name       VARCHAR,
    source_row_number      NUMBER,
    load_ts                TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);


-- ============================================================
-- 2. CUSTOMER MASTER
-- Grain: One row per customer per daily extract
-- Source format: CSV
-- ============================================================

CREATE TABLE IF NOT EXISTS RAW_CUSTOMER_MASTER (
    customer_id            VARCHAR(50),
    customer_hash_key      VARCHAR(100),
    postcode               VARCHAR(10),
    state                  VARCHAR(10),
    age_band               VARCHAR(20),
    gender_code            VARCHAR(10),
    loyalty_member_flag    VARCHAR(1),
    customer_segment       VARCHAR(50),
    customer_status        VARCHAR(30),
    last_updated_ts        TIMESTAMP_NTZ,

    source_file_name       VARCHAR,
    source_row_number      NUMBER,
    load_ts                TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);


-- ============================================================
-- 3. PRODUCT MASTER
-- Grain: One row per sellable product/SKU
-- Source format: CSV
-- ============================================================

CREATE TABLE IF NOT EXISTS RAW_PRODUCT_MASTER (
    product_id             VARCHAR(50),
    product_name           VARCHAR(300),
    brand                  VARCHAR(100),
    department             VARCHAR(100),
    category               VARCHAR(100),
    subcategory            VARCHAR(100),
    supplier_id            VARCHAR(50),
    cost_price             NUMBER(12, 2),
    selling_price          NUMBER(12, 2),
    product_status         VARCHAR(30),
    unit_of_measure VARCHAR(20),
    pack_size       NUMBER(10, 3),
    sellable_unit   VARCHAR(30),
    introduction_date DATE,
    source_file_name       VARCHAR,
    source_row_number      NUMBER,
    load_ts                TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);


-- ============================================================
-- 4. PRODUCT CDC
-- Grain: One row per product change event
-- Source format: CSV
-- ============================================================

CREATE TABLE IF NOT EXISTS RAW_PRODUCT_CDC (
    change_sequence        NUMBER,
    operation_type         VARCHAR(20),

    product_id             VARCHAR(50),
    product_name           VARCHAR(300),
    brand                  VARCHAR(100),
    department             VARCHAR(100),
    category               VARCHAR(100),
    subcategory            VARCHAR(100),
    supplier_id            VARCHAR(50),
    cost_price             NUMBER(12, 2),
    selling_price          NUMBER(12, 2),
    product_status         VARCHAR(30),
    unit_of_measure        VARCHAR(20),
    introduction_date      DATE,

    changed_attribute      VARCHAR(100),
    old_value              VARCHAR,
    new_value              VARCHAR,
    effective_from_ts      TIMESTAMP_NTZ,
    change_timestamp       TIMESTAMP_NTZ,

    source_file_name       VARCHAR,
    source_row_number      NUMBER,
    load_ts                TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);


-- ============================================================
-- 5. STORE-PRODUCT ASSORTMENT
-- Grain: One row per store-product ranging record
-- Source format: CSV
-- ============================================================

CREATE TABLE IF NOT EXISTS RAW_STORE_PRODUCT_ASSORTMENT (
    store_id                       VARCHAR(20),
    product_id                     VARCHAR(50),
    ranged_flag                    VARCHAR(1),
    ranging_start_date             DATE,
    ranging_end_date               DATE,
    replenishment_enabled_flag     VARCHAR(1),
    min_display_quantity           NUMBER,
    source_updated_ts              TIMESTAMP_NTZ,

    source_file_name               VARCHAR,
    source_row_number              NUMBER,
    load_ts                        TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);


-- ============================================================
-- 6. POS TRANSACTIONS
-- Grain: One row per transaction line item
-- Source format: CSV
-- ============================================================

CREATE TABLE IF NOT EXISTS RAW_POS_TRANSACTIONS (
    transaction_id          VARCHAR(100),
    transaction_line_id     NUMBER,
    store_id                 VARCHAR(20),
    customer_id              VARCHAR(50),
    product_id               VARCHAR(50),
    quantity                 NUMBER(10, 3),
    unit_price               NUMBER(12, 2),
    discount_amount          NUMBER(12, 2),
    tax_amount               NUMBER(12, 2),
    line_sales_amount        NUMBER(12, 2),
    payment_method           VARCHAR(50),
    transaction_timestamp    TIMESTAMP_NTZ,
    source_system            VARCHAR(100),

    source_file_name         VARCHAR,
    source_row_number        NUMBER,
    load_ts                  TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);


-- ============================================================
-- 7. INVENTORY SNAPSHOT
-- Grain in source payload:
-- One row per snapshot date, store and product
-- Source format: JSON
--
-- JSON is retained as VARIANT in RAW. It will be flattened and
-- typed in the dbt staging layer.
-- ============================================================

CREATE TABLE IF NOT EXISTS RAW_INVENTORY_SNAPSHOT (
    raw_payload             VARIANT,

    source_file_name        VARCHAR,
    source_row_number       NUMBER,
    load_ts                 TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);


-- ============================================================
-- 8. LOYALTY EVENTS
-- Grain in source payload: One row per loyalty event
-- Source format: JSON
--
-- JSON is retained as VARIANT in RAW. It will be flattened and
-- typed in the dbt staging layer.
-- ============================================================

CREATE TABLE IF NOT EXISTS RAW_LOYALTY_EVENTS (
    raw_payload             VARIANT,

    source_file_name        VARCHAR,
    source_row_number       NUMBER,
    load_ts                 TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);


-- ============================================================
-- 9. PROMOTIONS
-- Grain in source payload: One row per promotion-product record
-- Source format: JSON
--
-- Generator and ingestion logic will be added in a later step.
-- ============================================================

CREATE TABLE IF NOT EXISTS RAW_PROMOTIONS (
    raw_payload             VARIANT,

    source_file_name        VARCHAR,
    source_row_number       NUMBER,
    load_ts                 TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);
```

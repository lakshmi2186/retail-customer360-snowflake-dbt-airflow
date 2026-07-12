-- ============================================================
-- Script: 004_create_audit_tables.sql
-- Purpose: Create operational audit and monitoring tables
-- Project: Retail Customer 360 Data Platform
-- ============================================================

USE DATABASE RETAIL_DEV;
USE SCHEMA AUDIT;

CREATE TABLE IF NOT EXISTS PIPELINE_RUN (
    pipeline_run_id       VARCHAR(100),
    pipeline_name         VARCHAR(200),
    business_date         DATE,
    environment           VARCHAR(20),
    run_status            VARCHAR(30),
    start_ts              TIMESTAMP_NTZ,
    end_ts                TIMESTAMP_NTZ,
    records_processed     NUMBER,
    error_message         VARCHAR,
    triggered_by          VARCHAR(100),
    created_ts            TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

CREATE TABLE IF NOT EXISTS FILE_LOAD (
    file_load_id          VARCHAR(100),
    pipeline_run_id       VARCHAR(100),
    source_system         VARCHAR(100),
    source_file_name      VARCHAR,
    file_checksum         VARCHAR(256),
    target_table          VARCHAR(300),
    file_status           VARCHAR(30),
    rows_parsed           NUMBER,
    rows_loaded           NUMBER,
    rows_rejected         NUMBER,
    load_start_ts         TIMESTAMP_NTZ,
    load_end_ts           TIMESTAMP_NTZ,
    error_message         VARCHAR,
    created_ts            TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

CREATE TABLE IF NOT EXISTS DATA_QUALITY_RESULT (
    dq_result_id          VARCHAR(100),
    pipeline_run_id       VARCHAR(100),
    rule_name             VARCHAR(200),
    target_object         VARCHAR(300),
    rule_status           VARCHAR(30),
    records_checked       NUMBER,
    failed_record_count   NUMBER,
    failure_threshold     NUMBER,
    execution_ts          TIMESTAMP_NTZ,
    error_details         VARCHAR,
    created_ts            TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);
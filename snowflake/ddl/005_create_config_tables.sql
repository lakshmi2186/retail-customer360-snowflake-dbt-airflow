-- ============================================================
-- Script: 005_create_config_tables.sql
-- Purpose: Create metadata-driven pipeline configuration tables
-- Project: Retail Customer 360 Data Platform
-- ============================================================

USE DATABASE RETAIL_DEV;
USE SCHEMA CONFIG;

CREATE TABLE IF NOT EXISTS PIPELINE_CONFIG (
    pipeline_config_id    VARCHAR(100),
    source_name           VARCHAR(100),
    source_type           VARCHAR(50),
    stage_name            VARCHAR(300),
    file_pattern          VARCHAR,
    file_format_name      VARCHAR(300),
    target_table          VARCHAR(300),
    load_type             VARCHAR(30),
    execution_sequence    NUMBER,
    enabled_flag          VARCHAR(1),
    created_ts            TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_ts            TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

CREATE TABLE IF NOT EXISTS DQ_RULE_CONFIG (
    dq_rule_id            VARCHAR(100),
    source_name           VARCHAR(100),
    rule_name             VARCHAR(200),
    target_object         VARCHAR(300),
    rule_type             VARCHAR(100),
    rule_expression       VARCHAR,
    failure_threshold     NUMBER,
    severity              VARCHAR(20),
    enabled_flag          VARCHAR(1),
    created_ts            TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_ts            TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);
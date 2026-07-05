-- ============================================================
-- Script: 001_create_database_and_schemas.sql
-- Purpose: Create Snowflake development database and schemas
-- Project: Retail Customer 360 Data Platform
-- ============================================================

CREATE DATABASE IF NOT EXISTS RETAIL_DEV;

USE DATABASE RETAIL_DEV;

CREATE SCHEMA IF NOT EXISTS RAW;
CREATE SCHEMA IF NOT EXISTS CURATED;
CREATE SCHEMA IF NOT EXISTS CONSUMPTION;
CREATE SCHEMA IF NOT EXISTS AUDIT;
CREATE SCHEMA IF NOT EXISTS CONFIG;
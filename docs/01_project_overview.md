# Retail Customer 360 Data Platform

## 1. Project Overview

The Retail Customer 360 Data Platform is a production-style cloud data platform designed to consolidate customer, sales, product, loyalty, inventory and assortment data into a governed analytics environment.

The platform enables business users to perform customer behaviour analysis, loyalty program reporting, sales performance monitoring, inventory visibility, product performance tracking and store replenishment planning using a single source of truth.

The solution is implemented using Snowflake, dbt, Airflow, Azure Blob Storage and Python following modern data engineering best practices including dimensional modelling, SCD Type 2 processing, incremental loading, orchestration, data quality validation and environment-driven deployments.

---

## 2. Business Objectives

The platform is designed to support the following business capabilities:

### Customer 360 Analytics

* Understand customer purchasing behaviour.
* Analyse customer lifetime value.
* Identify high-value customer segments.
* Monitor customer loyalty engagement.
* Support targeted marketing initiatives.

### Sales Performance Reporting

* Daily sales reporting.
* Year-over-Year (YoY) sales analysis.
* Three-Year Year-over-Year (3YoY) trend analysis.
* Store performance monitoring.
* Product category performance analysis.

### Loyalty Program Analytics

* Points earned and redeemed analysis.
* Loyalty customer segmentation.
* Loyalty participation trends.
* Customer retention insights.

### Inventory and Availability

* Stock availability monitoring.
* Gap scan reporting.
* Product ranging compliance.
* Inventory position analysis.

### Replenishment Planning

* Store-level replenishment recommendations.
* Identification of low stock products.
* Reorder quantity calculations.
* Inventory optimisation support.

---

## 3. Key Business Questions

The platform should be able to answer the following questions:

### Customer

* Who are the highest value customers?
* How has customer spend changed over time?
* Which customers are at risk of becoming inactive?
* Which loyalty members generate the highest revenue?

### Sales

* What are total sales by day, week, month and year?
* What is the YoY and 3YoY growth by store and category?
* Which stores are outperforming expectations?
* Which products contribute the highest margin?

### Loyalty

* How frequently are loyalty points redeemed?
* What percentage of transactions include loyalty participation?
* Do loyalty customers spend more than non-loyalty customers?

### Product

* Which products have experienced significant cost changes?
* Which products are frequently purchased together?
* Which products are underperforming within a category?

### Inventory

* Which products are out of stock?
* Which products should be replenished?
* Which stores consistently experience availability issues?

---

## 4. Source Systems

The platform integrates data from multiple operational systems.

### POS Transactions

Daily transaction files containing sales activity from retail stores.

Format:

* CSV

Load Pattern:

* Daily batch ingestion

### Customer Master

Customer profile and loyalty membership information.

Format:

* CSV extract

Load Pattern:

* Daily batch ingestion

### Product Master

Product catalogue, pricing and supplier information.

Format:

* Database CDC feed

Load Pattern:

* Incremental CDC processing

### Loyalty Events

Customer loyalty activity including points earned and redeemed.

Format:

* REST API JSON

Load Pattern:

* API ingestion

### Inventory Snapshot

Daily inventory position by store and product.

Format:

* JSON

Load Pattern:

* Daily batch ingestion

### Promotion Feed

Promotion and discount event information.

Format:

* JSON

Load Pattern:

* Daily ingestion

### Store Product Assortment

Store ranging and product availability information.

Format:

* CSV

Load Pattern:

* Daily incremental ingestion

---

## 5. Technology Stack

| Layer                | Technology         |
| -------------------- | ------------------ |
| Cloud Storage        | Azure Blob Storage |
| Data Warehouse       | Snowflake          |
| Transformations      | dbt Core           |
| Orchestration        | Apache Airflow     |
| Programming Language | Python             |
| Source Control       | GitHub             |
| CI/CD                | GitHub Actions     |
| Documentation        | Markdown           |

---

## 6. Architectural Principles

The platform follows the following design principles:

### Scalability

The solution should support increasing transaction volumes without significant redesign.

### Reusability

Transformation logic should be modular and reusable across business domains.

### Data Quality

Data quality validations must be applied throughout the ingestion and transformation process.

### Governance

Data lineage, auditing and access controls must be implemented across all environments.

### Automation

All ingestion, transformation and validation activities should be orchestrated automatically.

### Environment Isolation

Development, test and production environments must remain logically separated.

---

## 7. High-Level Architecture

Source Systems

↓

Azure Blob Storage Landing Zone

↓

Snowflake RAW Layer

↓

dbt Staging Models

↓

dbt Intermediate Models

↓

dbt Dimensions and Facts

↓

Business Consumption Marts

↓

Reporting and Analytics Consumers

---

## 8. Success Criteria

The project will be considered successful when it demonstrates:

* End-to-end ingestion from multiple source patterns.
* CDC processing for product master data.
* SCD Type 2 implementation for customer and product dimensions.
* Incremental fact table loading.
* Automated orchestration using Airflow.
* Data quality validation framework.
* Audit and monitoring capabilities.
* Environment-driven deployment strategy.
* Production-ready documentation and governance controls.

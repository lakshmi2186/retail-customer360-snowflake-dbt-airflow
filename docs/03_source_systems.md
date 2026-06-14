# Source Systems Design

## 1. Purpose

This document defines the source systems used by the Retail Customer 360 Data Platform.

It describes:

* source system purpose
* ingestion pattern
* data format
* file naming conventions
* business keys
* expected volumes
* incremental loading approach

This document acts as the contract between source ingestion, Snowflake RAW tables and downstream dbt transformations.

---

## 2. Source System Summary

| Source                   | Business Purpose                                | Pattern    | Format | Frequency         |
| ------------------------ | ----------------------------------------------- | ---------- | ------ | ----------------- |
| POS Transactions         | Store sales transactions                        | Batch      | CSV    | Daily             |
| Customer Master          | Customer profile and loyalty membership         | Batch      | CSV    | Daily             |
| Product Master           | Product catalogue, pricing and supplier changes | CDC        | CSV    | Daily incremental |
| Loyalty Events           | Flybuys-style points activity                   | API / JSON | JSON   | Daily             |
| Inventory Snapshot       | Store-product stock position                    | Batch      | JSON   | Daily             |
| Promotions               | Active promotions and discount rules            | Batch      | JSON   | Daily             |
| Store Product Assortment | Store ranging and product availability          | Batch      | CSV    | Daily             |

---

## 3. Assumed Retail Scale

For the initial MVP, the platform simulates a medium-sized retail business.

| Entity                        |          Approximate Volume |
| ----------------------------- | --------------------------: |
| Stores                        |                          50 |
| Products                      |                       2,000 |
| Customers                     |                      20,000 |
| Daily Transactions            |                      25,000 |
| Daily Transaction Lines       |             60,000 - 80,000 |
| Daily Loyalty Events          |              5,000 - 10,000 |
| Daily Inventory Snapshot Rows |                     100,000 |
| Promotions                    | 100 - 300 active promotions |
| Store-Product Assortment Rows |                     100,000 |

These volumes are intentionally large enough to demonstrate realistic data engineering patterns while remaining manageable for a portfolio-scale Snowflake environment.

---

## 4. POS Transactions

### Business Description

POS transactions represent sales completed in physical stores. Each transaction can contain one or more products.

### Ingestion Pattern

Daily batch CSV file.

### Grain

One row per transaction line item.

### File Location

```text
landing/pos/
```

### File Name Pattern

```text
pos_transactions_YYYYMMDD.csv
```

Example:

```text
pos_transactions_20260614.csv
```

### Business Key

```text
transaction_id + transaction_line_id
```

### Source Columns

| Column                | Description                                          |
| --------------------- | ---------------------------------------------------- |
| transaction_id        | Unique transaction identifier                        |
| transaction_line_id   | Unique line within transaction                       |
| store_id              | Store where transaction occurred                     |
| customer_id           | Customer identifier, nullable for anonymous purchase |
| product_id            | Product purchased                                    |
| quantity              | Quantity sold                                        |
| unit_price            | Selling price per unit                               |
| discount_amount       | Discount applied to line                             |
| tax_amount            | GST/tax amount                                       |
| payment_method        | Payment method                                       |
| transaction_timestamp | Transaction timestamp                                |
| source_system         | Source system name                                   |

### Incremental Load Logic

Load new transaction lines based on:

```text
transaction_id + transaction_line_id
```

Duplicate transaction lines should be rejected or ignored based on the ingestion control logic.

---

## 5. Customer Master

### Business Description

Customer Master contains customer profile information and loyalty membership status.

### Ingestion Pattern

Daily CSV extract.

### Grain

One row per customer per extract.

### File Location

```text
landing/customer/
```

### File Name Pattern

```text
customer_master_YYYYMMDD.csv
```

### Business Key

```text
customer_id
```

### Source Columns

| Column              | Description                    |
| ------------------- | ------------------------------ |
| customer_id         | Unique customer identifier     |
| customer_hash_key   | Hashed customer identity       |
| postcode            | Customer postcode              |
| state               | Customer state                 |
| age_band            | Age group                      |
| gender_code         | Optional demographic code      |
| loyalty_member_flag | Loyalty membership indicator   |
| customer_segment    | Bronze, Silver, Gold, Platinum |
| customer_status     | Active, Inactive, Closed       |
| last_updated_ts     | Source update timestamp        |

### Incremental / SCD Logic

Customer Master is loaded daily. Changes to key descriptive attributes are tracked in `dim_customer_scd2`.

Tracked attributes include:

* postcode
* state
* loyalty_member_flag
* customer_segment
* customer_status

---

## 6. Product Master CDC

### Business Description

Product Master contains product catalogue, supplier, category and pricing information. Product changes are captured using a CDC-style feed.

### Ingestion Pattern

Daily CDC extract.

### Grain

One row per product change event.

### File Location

```text
landing/product_cdc/
```

### File Name Pattern

```text
product_cdc_YYYYMMDD.csv
```

### Business Key

```text
product_id + change_sequence
```

### Source Columns

| Column            | Description                     |
| ----------------- | ------------------------------- |
| change_sequence   | Ordered CDC sequence number     |
| operation_type    | INSERT, UPDATE, DELETE          |
| product_id        | Product identifier              |
| product_name      | Product name                    |
| brand             | Product brand                   |
| category          | Product category                |
| subcategory       | Product subcategory             |
| supplier_id       | Supplier identifier             |
| cost_price        | Product cost price              |
| selling_price     | Product selling price           |
| product_status    | Active, Discontinued, Suspended |
| effective_from_ts | Source effective timestamp      |
| change_timestamp  | CDC change timestamp            |

### SCD Logic

Product changes are used to maintain `dim_product_scd2`.

Tracked attributes include:

* product_name
* brand
* category
* subcategory
* supplier_id
* cost_price
* selling_price
* product_status

---

## 7. Loyalty Events

### Business Description

Loyalty Events represent Flybuys-style customer activity such as points earned, points redeemed and points expired.

### Ingestion Pattern

API JSON ingestion.

### File Location

```text
api/flybuys/
```

### File Name Pattern

```text
loyalty_events_YYYYMMDD.json
```

### Business Key

```text
event_id
```

### JSON Example

```json
{
  "event_id": "EVT10001",
  "customer_id": "CUST10001",
  "transaction_id": "TXN90001",
  "event_type": "POINTS_EARNED",
  "points": 120,
  "event_timestamp": "2026-06-14T10:30:00",
  "channel": "STORE"
}
```

### Event Types

```text
POINTS_EARNED
POINTS_REDEEMED
POINTS_EXPIRED
BONUS_POINTS
```

---

## 8. Inventory Snapshot

### Business Description

Inventory Snapshot captures daily stock position by store and product.

### Ingestion Pattern

Daily JSON file.

### Grain

One row per store, product and snapshot date.

### File Location

```text
landing/inventory/
```

### File Name Pattern

```text
inventory_snapshot_YYYYMMDD.json
```

### Business Key

```text
store_id + product_id + snapshot_date
```

### JSON Example

```json
{
  "snapshot_date": "2026-06-14",
  "store_id": "STORE001",
  "product_id": "PROD10001",
  "stock_on_hand": 45,
  "stock_reserved": 3,
  "stock_in_transit": 10,
  "reorder_point": 20,
  "reorder_quantity": 50
}
```

---

## 9. Promotions

### Business Description

Promotions define temporary discounts or campaign offers for products.

### Ingestion Pattern

Daily JSON file.

### File Location

```text
landing/promotions/
```

### File Name Pattern

```text
promotions_YYYYMMDD.json
```

### Business Key

```text
promotion_id
```

### JSON Example

```json
{
  "promotion_id": "PROMO1001",
  "product_id": "PROD10001",
  "promotion_type": "PERCENT_DISCOUNT",
  "discount_percent": 20,
  "start_date": "2026-06-10",
  "end_date": "2026-06-20",
  "campaign_name": "Winter Value Campaign"
}
```

---

## 10. Store Product Assortment

### Business Description

Store Product Assortment defines whether a product is ranged and available for sale in a particular store.

### Ingestion Pattern

Daily CSV file.

### Grain

One row per store-product ranging record.

### File Location

```text
landing/assortment/
```

### File Name Pattern

```text
store_product_assortment_YYYYMMDD.csv
```

### Business Key

```text
store_id + product_id + ranging_start_date
```

### Source Columns

| Column                     | Description                        |
| -------------------------- | ---------------------------------- |
| store_id                   | Store identifier                   |
| product_id                 | Product identifier                 |
| ranged_flag                | Whether product is ranged in store |
| ranging_start_date         | Start date of ranging              |
| ranging_end_date           | End date of ranging                |
| replenishment_enabled_flag | Whether product can be replenished |
| min_display_quantity       | Minimum display quantity           |
| source_updated_ts          | Source update timestamp            |

---

## 11. Source Control and Replay Strategy

All files landed in Azure Blob Storage are retained before archival.

Rejected files are moved to:

```text
rejected/
```

Successfully processed files are moved to:

```text
archive/
```

This supports:

* auditability
* replay
* debugging
* backfill processing

---

## 12. Design Decisions

### POS as Batch

POS is implemented as daily batch ingestion because the MVP supports daily reporting. If near-real-time reporting is required later, the architecture can be extended to streaming ingestion.

### Customer Master as Daily Extract

Customer Master is implemented as a daily batch extract because profile changes do not require intra-day reporting in this MVP.

### Product Master as CDC

Product Master uses CDC because product pricing, cost, supplier and status changes directly affect historical margin reporting and SCD Type 2 processing.

### Loyalty Events as JSON

Loyalty events are represented as JSON to demonstrate semi-structured ingestion and API-style processing.

### Inventory as Daily Snapshot

Inventory is modelled as a daily snapshot because replenishment and gap scan reporting require point-in-time stock position by store and product.

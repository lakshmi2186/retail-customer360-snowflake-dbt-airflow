# Source Data Generators

This folder contains Python scripts used to generate realistic source data for the Retail Customer 360 Data Platform.

The generated files simulate operational retail systems including POS, product master, customer master, loyalty events, inventory snapshots and store-product assortment.

## Generator Execution Order

Run the scripts in the following order:

```bash
python python/generators/generate_stores.py
python python/generators/generate_products.py
python python/generators/generate_customers.py
python python/generators/generate_product_cdc.py
python python/generators/generate_store_product_assortment.py
python python/generators/generate_inventory_snapshot.py
python python/generators/generate_loyalty_events.py
python python/generators/generate_pos_transactions.py
```

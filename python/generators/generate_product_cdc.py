import random
from datetime import datetime
from pathlib import Path

import pandas as pd


INPUT_PATH = Path("data/generated/product/product_master.csv")
OUTPUT_PATH = Path("data/generated/product_cdc/product_cdc_20260621.csv")

CHANGE_PERCENTAGE = 0.05

CHANGE_TYPES = ["selling_price", "cost_price", "supplier_id", "product_status"]
CHANGE_WEIGHTS = [45, 30, 15, 10]


def calculate_change_count(total_products: int) -> int:
    """Calculate number of product records to include in the CDC extract."""
    return round(total_products * CHANGE_PERCENTAGE)


def apply_product_change(row: pd.Series) -> pd.Series:
    """Apply one realistic product attribute change to a product record."""
    change_type = random.choices(
        CHANGE_TYPES,
        weights=CHANGE_WEIGHTS,
        k=1,
    )[0]

    row["changed_attribute"] = change_type

    if change_type == "selling_price":
        old_value = row["selling_price"]
        new_value = round(old_value * random.uniform(0.90, 1.10), 2)

        row["old_value"] = old_value
        row["new_value"] = new_value
        row["selling_price"] = new_value

    elif change_type == "cost_price":
        old_value = row["cost_price"]
        new_value = round(old_value * random.uniform(0.95, 1.15), 2)

        row["old_value"] = old_value
        row["new_value"] = new_value
        row["cost_price"] = new_value

    elif change_type == "supplier_id":
        old_value = row["supplier_id"]
        new_value = f"SUP{random.randint(1000, 9999)}"

        row["old_value"] = old_value
        row["new_value"] = new_value
        row["supplier_id"] = new_value

    elif change_type == "product_status":
        old_value = row["product_status"]
        possible_statuses = ["Active", "Discontinued", "Suspended"]

        # Avoid setting the same status again.
        possible_statuses = [
            status for status in possible_statuses if status != old_value
        ]

        new_value = random.choice(possible_statuses)

        row["old_value"] = old_value
        row["new_value"] = new_value
        row["product_status"] = new_value

    return row


def generate_product_cdc() -> pd.DataFrame:
    """Generate a CDC-style product change extract."""
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_PATH}. "
            "Run generate_products.py first."
        )

    products_df = pd.read_csv(INPUT_PATH)

    change_count = calculate_change_count(len(products_df))

    changed_products_df = products_df.sample(
        n=change_count,
        random_state=42,
    ).copy()

    changed_rows = []

    for _, row in changed_products_df.iterrows():
        updated_row = apply_product_change(row.copy())
        changed_rows.append(updated_row)

    cdc_df = pd.DataFrame(changed_rows)

    current_timestamp = datetime.now()

    cdc_df.insert(0, "change_sequence", range(1, len(cdc_df) + 1))
    cdc_df.insert(1, "operation_type", "UPDATE")

    cdc_df["effective_from_ts"] = current_timestamp
    cdc_df["change_timestamp"] = current_timestamp

    return cdc_df


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    cdc_df = generate_product_cdc()
    cdc_df.to_csv(OUTPUT_PATH, index=False)

    print(f"Generated {len(cdc_df)} product CDC records")
    print(f"Output file: {OUTPUT_PATH}")
    print("Change distribution:")
    print(cdc_df["changed_attribute"].value_counts())


if __name__ == "__main__":
    main()
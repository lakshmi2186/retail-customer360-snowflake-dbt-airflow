import json
import random
from datetime import datetime
from pathlib import Path

import pandas as pd


ASSORTMENT_INPUT_PATH = Path("data/generated/assortment/store_product_assortment.csv")
OUTPUT_PATH = Path("data/generated/inventory/inventory_snapshot_20260621.json")

SNAPSHOT_DATE = "2026-06-21"


def generate_stock_on_hand(replenishment_enabled_flag: str) -> int:
    """Generate realistic stock-on-hand quantity."""
    if replenishment_enabled_flag == "N":
        return random.choices(
            [0, random.randint(1, 5)],
            weights=[80, 20],
            k=1,
        )[0]

    stock_scenario = random.choices(
        ["out_of_stock", "low_stock", "normal_stock", "high_stock"],
        weights=[5, 15, 70, 10],
        k=1,
    )[0]

    if stock_scenario == "out_of_stock":
        return 0

    if stock_scenario == "low_stock":
        return random.randint(1, 10)

    if stock_scenario == "normal_stock":
        return random.randint(11, 80)

    return random.randint(81, 200)


def generate_inventory_snapshot() -> list[dict]:
    """Generate daily inventory snapshot records."""
    if not ASSORTMENT_INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Input file not found: {ASSORTMENT_INPUT_PATH}. "
            "Run generate_store_product_assortment.py first."
        )

    assortment_df = pd.read_csv(ASSORTMENT_INPUT_PATH)

    ranged_assortment_df = assortment_df[
        assortment_df["ranged_flag"] == "Y"
    ].copy()

    inventory_records = []

    for _, row in ranged_assortment_df.iterrows():
        stock_on_hand = generate_stock_on_hand(
            row["replenishment_enabled_flag"]
        )

        stock_reserved = random.randint(0, min(stock_on_hand, 5))
        stock_in_transit = random.choices(
            [0, random.randint(5, 50)],
            weights=[70, 30],
            k=1,
        )[0]

        reorder_point = random.randint(10, 30)
        reorder_quantity = random.randint(20, 100)

        inventory_records.append(
            {
                "snapshot_date": SNAPSHOT_DATE,
                "store_id": str(row["store_id"]),
                "product_id": str(row["product_id"]),
                "stock_on_hand": stock_on_hand,
                "stock_reserved": stock_reserved,
                "stock_in_transit": stock_in_transit,
                "reorder_point": reorder_point,
                "reorder_quantity": reorder_quantity,
                "source_updated_ts": datetime.now().isoformat(),
            }
        )

    return inventory_records


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    inventory_records = generate_inventory_snapshot()

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        json.dump(inventory_records, file, indent=2)

    print(f"Generated {len(inventory_records)} inventory snapshot records")
    print(f"Output file: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
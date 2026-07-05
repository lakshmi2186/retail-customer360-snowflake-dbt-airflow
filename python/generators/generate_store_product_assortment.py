import random
from datetime import datetime
from pathlib import Path

import pandas as pd
from faker import Faker


STORE_INPUT_PATH = Path("data/generated/store/store_master.csv")
PRODUCT_INPUT_PATH = Path("data/generated/product/product_master.csv")
OUTPUT_PATH = Path("data/generated/assortment/store_product_assortment.csv")


def determine_ranged_flag(product_status: str) -> str:
    """Determine whether a product is ranged in a store based on product status."""
    if product_status == "Active":
        return random.choices(["Y", "N"], weights=[85, 15], k=1)[0]

    if product_status == "Suspended":
        return random.choices(["Y", "N"], weights=[20, 80], k=1)[0]

    if product_status == "Discontinued":
        return random.choices(["Y", "N"], weights=[10, 90], k=1)[0]

    return "N"


def determine_replenishment_enabled(ranged_flag: str, product_status: str) -> str:
    """Determine whether replenishment is enabled for a store-product combination."""
    if ranged_flag == "N":
        return "N"

    if product_status != "Active":
        return "N"

    return random.choices(["Y", "N"], weights=[90, 10], k=1)[0]


def generate_store_product_assortment() -> pd.DataFrame:
    """Generate store-product assortment records."""
    if not STORE_INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Input file not found: {STORE_INPUT_PATH}. "
            "Run generate_stores.py first."
        )

    if not PRODUCT_INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Input file not found: {PRODUCT_INPUT_PATH}. "
            "Run generate_products.py first."
        )

    fake = Faker("en_AU")

    stores_df = pd.read_csv(STORE_INPUT_PATH)
    products_df = pd.read_csv(PRODUCT_INPUT_PATH)

    rows = []

    for _, store in stores_df.iterrows():
        for _, product in products_df.iterrows():
            ranged_flag = determine_ranged_flag(product["product_status"])
            replenishment_enabled_flag = determine_replenishment_enabled(
                ranged_flag=ranged_flag,
                product_status=product["product_status"],
            )

            ranging_start_date = fake.date_between(
                start_date="-5y",
                end_date="-30d",
            )

            ranging_end_date = None

            if ranged_flag == "N":
                ranging_end_date = fake.date_between(
                    start_date=ranging_start_date,
                    end_date="today",
                )

            rows.append(
                {
                    "store_id": str(store["store_id"]),
                    "product_id": str(product["product_id"]),
                    "ranged_flag": ranged_flag,
                    "ranging_start_date": ranging_start_date,
                    "ranging_end_date": ranging_end_date,
                    "replenishment_enabled_flag": replenishment_enabled_flag,
                    "min_display_quantity": random.randint(1, 20),
                    "source_updated_ts": datetime.now(),
                }
            )

    return pd.DataFrame(rows)


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    assortment_df = generate_store_product_assortment()
    assortment_df.to_csv(OUTPUT_PATH, index=False)

    print(f"Generated {len(assortment_df)} store-product assortment records")
    print(f"Output file: {OUTPUT_PATH}")
    print("Ranged flag distribution:")
    print(assortment_df["ranged_flag"].value_counts())


if __name__ == "__main__":
    main()
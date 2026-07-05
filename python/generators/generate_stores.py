import random
from pathlib import Path

import pandas as pd
from faker import Faker


OUTPUT_PATH = Path("data/generated/master/store_master.csv")
TOTAL_STORES = 50

STATE_DISTRIBUTION = {
    "VIC": 20,
    "NSW": 15,
    "QLD": 8,
    "SA": 4,
    "WA": 3,
}

STORE_FORMATS = ["Metro", "Regional", "Local"]


def generate_unique_store_ids(count: int) -> list[str]:
    """Generate unique 4-digit store IDs."""
    store_ids = set()

    while len(store_ids) < count:
        store_ids.add(str(random.randint(1000, 9999)))

    return list(store_ids)


def generate_stores() -> pd.DataFrame:
    fake = Faker("en_AU")
    store_ids = generate_unique_store_ids(TOTAL_STORES)

    rows = []
    index = 0

    for state, store_count in STATE_DISTRIBUTION.items():
        for _ in range(store_count):
            store_id = store_ids[index]
            suburb = fake.city()

            rows.append(
                {
                    "store_id": store_id,
                    "store_name": f"{suburb} Store",
                    "state": state,
                    "region": random.choice(["Metro", "Regional"]),
                    "postcode": fake.postcode(),
                    "store_format": random.choice(STORE_FORMATS),
                    "opening_date": fake.date_between(start_date="-20y", end_date="-1y"),
                    "active_flag": "Y",
                }
            )

            index += 1

    return pd.DataFrame(rows)


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    stores_df = generate_stores()
    stores_df.to_csv(OUTPUT_PATH, index=False)

    print(f"Generated {len(stores_df)} stores")
    print(f"Output file: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
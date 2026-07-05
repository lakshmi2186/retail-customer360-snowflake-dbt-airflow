import random
import hashlib
from pathlib import Path

import pandas as pd
from faker import Faker


OUTPUT_PATH = Path("data/generated/customer/customer_master.csv")
TOTAL_CUSTOMERS = 20000

STATES = ["VIC", "NSW", "QLD", "SA", "WA"]
AGE_BANDS = ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
SEGMENTS = ["Bronze", "Silver", "Gold", "Platinum"]
CUSTOMER_STATUS = ["Active", "Inactive", "Closed"]


def hash_customer_identity(email: str) -> str:
    return hashlib.sha256(email.lower().encode("utf-8")).hexdigest()


def generate_customer_id(index: int) -> str:
    return str(50000000 + index)


def generate_customers() -> pd.DataFrame:
    fake = Faker("en_AU")
    rows = []

    for index in range(1, TOTAL_CUSTOMERS + 1):
        email = fake.unique.email()
        loyalty_flag = random.choices(["Y", "N"], weights=[75, 25], k=1)[0]

        if loyalty_flag == "Y":
            segment = random.choices(
                SEGMENTS,
                weights=[45, 30, 18, 7],
                k=1,
            )[0]
        else:
            segment = "Non-Loyalty"

        rows.append(
            {
                "customer_id": generate_customer_id(index),
                "customer_hash_key": hash_customer_identity(email),
                "postcode": fake.postcode(),
                "state": random.choice(STATES),
                "age_band": random.choice(AGE_BANDS),
                "gender_code": random.choice(["F", "M", "U"]),
                "loyalty_member_flag": loyalty_flag,
                "customer_segment": segment,
                "customer_status": random.choices(
                    CUSTOMER_STATUS,
                    weights=[90, 8, 2],
                    k=1,
                )[0],
                "last_updated_ts": fake.date_time_between(start_date="-2y", end_date="now"),
            }
        )

    return pd.DataFrame(rows)


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    customers_df = generate_customers()
    customers_df.to_csv(OUTPUT_PATH, index=False)

    print(f"Generated {len(customers_df)} customers")
    print(f"Output file: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd


CUSTOMER_INPUT_PATH = Path("data/generated/customer/customer_master.csv")
STORE_INPUT_PATH = Path("data/generated/store/store_master.csv")
OUTPUT_PATH = Path("data/generated/loyalty/loyalty_events_20260621.json")

BUSINESS_DATE = "2026-06-21"
TOTAL_EVENTS = 8000

EVENT_TYPES = ["POINTS_EARNED", "POINTS_REDEEMED", "POINTS_EXPIRED", "BONUS_POINTS"]
EVENT_WEIGHTS = [65, 20, 5, 10]


def generate_event_id(index: int) -> str:
    """Generate a loyalty event business key."""
    return f"EVT{str(index).zfill(10)}"


def generate_event_timestamp() -> str:
    """Generate an event timestamp within the business day."""
    base_datetime = datetime.fromisoformat(f"{BUSINESS_DATE}T00:00:00")
    random_seconds = random.randint(0, 86399)
    return (base_datetime + timedelta(seconds=random_seconds)).isoformat()


def generate_points(event_type: str) -> int:
    """Generate points based on the loyalty event type."""
    if event_type == "POINTS_EARNED":
        return random.randint(10, 500)

    if event_type == "POINTS_REDEEMED":
        return random.randint(100, 5000)

    if event_type == "POINTS_EXPIRED":
        return random.randint(50, 1500)

    if event_type == "BONUS_POINTS":
        return random.randint(100, 2000)

    return 0


def generate_loyalty_events() -> list[dict]:
    """Generate Flybuys-style loyalty event records."""
    if not CUSTOMER_INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Input file not found: {CUSTOMER_INPUT_PATH}. "
            "Run generate_customers.py first."
        )

    if not STORE_INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Input file not found: {STORE_INPUT_PATH}. "
            "Run generate_stores.py first."
        )

    customers_df = pd.read_csv(CUSTOMER_INPUT_PATH)
    stores_df = pd.read_csv(STORE_INPUT_PATH)

    loyalty_customers_df = customers_df[
        customers_df["loyalty_member_flag"] == "Y"
    ].copy()

    if loyalty_customers_df.empty:
        raise ValueError("No loyalty customers found in customer master.")

    customer_ids = loyalty_customers_df["customer_id"].astype(str).tolist()
    store_ids = stores_df["store_id"].astype(str).tolist()

    events = []

    for index in range(1, TOTAL_EVENTS + 1):
        event_type = random.choices(
            EVENT_TYPES,
            weights=EVENT_WEIGHTS,
            k=1,
        )[0]

        events.append(
            {
                "event_id": generate_event_id(index),
                "customer_id": random.choice(customer_ids),
                "transaction_id": None,
                "store_id": random.choice(store_ids),
                "event_type": event_type,
                "points": generate_points(event_type),
                "event_timestamp": generate_event_timestamp(),
                "channel": random.choice(["STORE", "ONLINE", "APP"]),
                "source_system": "FLYBUYS_SIM",
                "source_updated_ts": datetime.now().isoformat(),
            }
        )

    return events


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    loyalty_events = generate_loyalty_events()

    with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
        json.dump(loyalty_events, file, indent=2)

    print(f"Generated {len(loyalty_events)} loyalty events")
    print(f"Output file: {OUTPUT_PATH}")

    event_type_counts = {}
    for event in loyalty_events:
        event_type_counts[event["event_type"]] = (
            event_type_counts.get(event["event_type"], 0) + 1
        )

    print("Event type distribution:")
    for event_type, count in event_type_counts.items():
        print(f"{event_type}: {count}")


if __name__ == "__main__":
    main()
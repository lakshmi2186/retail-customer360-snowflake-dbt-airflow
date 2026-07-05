import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd


STORE_INPUT_PATH = Path("data/generated/store/store_master.csv")
PRODUCT_INPUT_PATH = Path("data/generated/product/product_master.csv")
CUSTOMER_INPUT_PATH = Path("data/generated/customer/customer_master.csv")
ASSORTMENT_INPUT_PATH = Path("data/generated/assortment/store_product_assortment.csv")

OUTPUT_PATH = Path("data/generated/pos/pos_transactions_20260621.csv")

BUSINESS_DATE = "2026-06-21"
TOTAL_TRANSACTIONS = 25000
IDENTIFIED_CUSTOMER_PERCENTAGE = 0.70

PAYMENT_METHODS = ["Card", "Cash", "Gift Card", "Digital Wallet"]
PAYMENT_WEIGHTS = [70, 10, 5, 15]


def generate_transaction_id(index: int) -> str:
    """Generate a transaction business key."""
    return f"TXN{str(index).zfill(10)}"


def generate_transaction_timestamp() -> str:
    """Generate a transaction timestamp within the business day."""
    base_datetime = datetime.fromisoformat(f"{BUSINESS_DATE}T00:00:00")
    random_seconds = random.randint(0, 86399)
    return (base_datetime + timedelta(seconds=random_seconds)).isoformat()


def choose_customer(customer_ids: list[str]) -> str | None:
    """Return a customer ID for identified transactions, otherwise anonymous."""
    is_identified = random.random() < IDENTIFIED_CUSTOMER_PERCENTAGE

    if not is_identified:
        return None

    return random.choice(customer_ids)


def generate_quantity() -> int:
    """Generate realistic purchase quantity."""
    return random.choices(
        [1, 2, 3, 4, 5],
        weights=[60, 25, 10, 3, 2],
        k=1,
    )[0]


def calculate_discount(gross_amount: float) -> float:
    """Apply discount to a subset of transaction lines."""
    has_discount = random.choices(
        [True, False],
        weights=[20, 80],
        k=1,
    )[0]

    if not has_discount:
        return 0.0

    discount_percentage = random.choice([0.05, 0.10, 0.15, 0.20])
    return round(gross_amount * discount_percentage, 2)


def generate_pos_transactions() -> pd.DataFrame:
    """Generate POS transaction line records."""
    for input_path in [
        STORE_INPUT_PATH,
        PRODUCT_INPUT_PATH,
        CUSTOMER_INPUT_PATH,
        ASSORTMENT_INPUT_PATH,
    ]:
        if not input_path.exists():
            raise FileNotFoundError(
                f"Input file not found: {input_path}. "
                "Run the upstream generators first."
            )

    stores_df = pd.read_csv(STORE_INPUT_PATH)
    products_df = pd.read_csv(PRODUCT_INPUT_PATH)
    customers_df = pd.read_csv(CUSTOMER_INPUT_PATH)
    assortment_df = pd.read_csv(ASSORTMENT_INPUT_PATH)

    active_assortment_df = assortment_df[
        assortment_df["ranged_flag"] == "Y"
    ].copy()

    active_products_df = products_df[
        products_df["product_status"] == "Active"
    ].copy()

    # Only allow products that are both active and ranged.
    active_assortment_df = active_assortment_df.merge(
        active_products_df[["product_id", "selling_price"]],
        on="product_id",
        how="inner",
    )

    store_ids = stores_df["store_id"].astype(str).tolist()
    customer_ids = customers_df[
        customers_df["customer_status"] == "Active"
    ]["customer_id"].astype(str).tolist()

    # Create a lookup of ranged products by store to avoid invalid sales.
    products_by_store = {
        str(store_id): group[["product_id", "selling_price"]].to_dict("records")
        for store_id, group in active_assortment_df.groupby("store_id")
    }

    rows = []

    for transaction_index in range(1, TOTAL_TRANSACTIONS + 1):
        transaction_id = generate_transaction_id(transaction_index)
        store_id = random.choice(store_ids)
        customer_id = choose_customer(customer_ids)
        payment_method = random.choices(
            PAYMENT_METHODS,
            weights=PAYMENT_WEIGHTS,
            k=1,
        )[0]
        transaction_timestamp = generate_transaction_timestamp()

        available_products = products_by_store.get(str(store_id), [])

        if not available_products:
            continue

        line_count = random.choices(
            [1, 2, 3, 4, 5, 6],
            weights=[15, 25, 25, 18, 12, 5],
            k=1,
        )[0]

        selected_products = random.sample(
            available_products,
            k=min(line_count, len(available_products)),
        )

        for line_index, product in enumerate(selected_products, start=1):
            quantity = generate_quantity()
            unit_price = round(float(product["selling_price"]), 2)

            gross_amount = round(quantity * unit_price, 2)
            discount_amount = calculate_discount(gross_amount)
            line_sales_amount = round(gross_amount - discount_amount, 2)

            # GST is included in most Australian retail prices.
            # This calculates the GST component assuming 10% GST-inclusive pricing.
            tax_amount = round(line_sales_amount / 11, 2)

            rows.append(
                {
                    "transaction_id": transaction_id,
                    "transaction_line_id": line_index,
                    "store_id": str(store_id),
                    "customer_id": customer_id,
                    "product_id": str(product["product_id"]),
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "discount_amount": discount_amount,
                    "tax_amount": tax_amount,
                    "line_sales_amount": line_sales_amount,
                    "payment_method": payment_method,
                    "transaction_timestamp": transaction_timestamp,
                    "source_system": "POS_SIM",
                }
            )

    return pd.DataFrame(rows)


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    pos_df = generate_pos_transactions()
    pos_df.to_csv(OUTPUT_PATH, index=False)

    print(f"Generated {len(pos_df)} POS transaction lines")
    print(f"Output file: {OUTPUT_PATH}")
    print("Customer attribution:")
    print(pos_df["customer_id"].isna().value_counts())


if __name__ == "__main__":
    main()
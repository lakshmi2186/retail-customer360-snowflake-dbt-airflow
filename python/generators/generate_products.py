import random
from pathlib import Path

import pandas as pd
from faker import Faker


OUTPUT_PATH = Path("data/generated/product/product_master.csv")
TOTAL_PRODUCTS = 2000

DEPARTMENTS = {
    "Grocery": {
        "Pantry": ["Rice", "Pasta", "Canned Food", "Sauces"],
        "Breakfast": ["Cereal", "Oats", "Spreads"],
        "Snacks": ["Chips", "Biscuits", "Crackers"],
    },
    "Fresh Produce": {
        "Fruit": ["Apples", "Bananas", "Berries", "Citrus"],
        "Vegetables": ["Leafy Greens", "Root Vegetables", "Tomatoes"],
    },
    "Dairy": {
        "Milk": ["Full Cream Milk", "Lite Milk", "Plant Milk"],
        "Cheese": ["Block Cheese", "Sliced Cheese", "Soft Cheese"],
        "Yoghurt": ["Greek Yoghurt", "Flavoured Yoghurt"],
    },
    "Bakery": {
        "Bread": ["White Bread", "Wholemeal Bread", "Sourdough"],
        "Pastry": ["Croissants", "Muffins", "Donuts"],
    },
    "Frozen": {
        "Frozen Meals": ["Pizza", "Ready Meals", "Frozen Snacks"],
        "Frozen Vegetables": ["Peas", "Corn", "Mixed Vegetables"],
    },
    "Liquor": {
        "Beer": ["Lager", "Pale Ale", "Craft Beer"],
        "Wine": ["Red Wine", "White Wine", "Sparkling Wine"],
    },
    "Health & Beauty": {
        "Personal Care": ["Shampoo", "Conditioner", "Body Wash"],
        "Health": ["Vitamins", "First Aid", "Pain Relief"],
    },
    "Household": {
        "Cleaning": ["Laundry", "Dishwashing", "Surface Cleaner"],
        "Paper Goods": ["Toilet Paper", "Tissues", "Paper Towel"],
    },
    "Pet": {
        "Pet Food": ["Dog Food", "Cat Food", "Pet Treats"],
        "Pet Care": ["Litter", "Grooming"],
    },
}

BRANDS = [
    "HomeChoice",
    "FreshFarm",
    "DailyValue",
    "NatureBest",
    "Urban Pantry",
    "Golden Harvest",
    "PureLife",
    "Aussie Select",
    "Market Lane",
    "Budget Buy",
]

UOM = ["EA", "KG", "G", "L", "ML"]

PACK_SIZE_OPTIONS = {
    "EA": [1, 2, 4, 6, 12, 24],
    "KG": [0.5, 1, 2, 5],
    "G": [100, 250, 500, 750],
    "L": [0.5, 1, 2, 3],
    "ML": [250, 375, 500, 750],
}


def generate_product_id(index: int) -> str:
    return str(10000000 + index)


def generate_products() -> pd.DataFrame:
    fake = Faker("en_AU")
    rows = []

    for index in range(1, TOTAL_PRODUCTS + 1):
        department = random.choice(list(DEPARTMENTS.keys()))
        category = random.choice(list(DEPARTMENTS[department].keys()))
        subcategory = random.choice(DEPARTMENTS[department][category])

        brand = random.choice(BRANDS)

        cost_price = round(random.uniform(1.0, 80.0), 2)
        margin_multiplier = random.uniform(1.15, 1.65)
        selling_price = round(cost_price * margin_multiplier, 2)

        product_status = random.choices(
            ["Active", "Discontinued", "Suspended"],
            weights=[92, 5, 3],
            k=1,
        )[0]

        product_name = f"{brand} {subcategory} {random.choice(['Small', 'Regular', 'Large', 'Family Pack'])}"
        
        unit_of_measure = random.choice(UOM)
        pack_size = random.choice(PACK_SIZE_OPTIONS[unit_of_measure])

        if unit_of_measure == "EA":
            sellable_unit = f"{pack_size} Pack" if pack_size > 1 else "Each"
        else:
            sellable_unit = f"{pack_size}{unit_of_measure}"
        rows.append(
            {
                "product_id": generate_product_id(index),
                "product_name": product_name,
                "brand": brand,
                "department": department,
                "category": category,
                "subcategory": subcategory,
                "supplier_id": f"SUP{random.randint(1000, 9999)}",
                "cost_price": cost_price,
                "selling_price": selling_price,
                "product_status": product_status,
                "unit_of_measure": unit_of_measure,
                "pack_size": pack_size,
                "sellable_unit": sellable_unit,
                "introduction_date": fake.date_between(start_date="-10y", end_date="-30d"),
            }
        )

    return pd.DataFrame(rows)


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    products_df = generate_products()
    products_df.to_csv(OUTPUT_PATH, index=False)

    print(f"Generated {len(products_df)} products")
    print(f"Output file: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
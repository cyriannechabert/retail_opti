import pandas as pd
import random
from datetime import datetime, timedelta

# --- CONFIGURATION ---
NUM_PRODUCTS = 500    # How many unique items to generate
NUM_SALES = 5000      # How many transactions to simulate
NUM_STOCK = 800       # How many stock batches to receive

# --- STEP 1: PROCEDURAL PRODUCT GENERATOR ---
# We define "Blueprints" for categories to ensure data looks real.
# e.g., We won't generate "Coca Cola - Ham", only "Coca Cola - Soda".

blueprints = {
    "Dairy": {
        "brands": ["Danone", "Yoplait", "Président", "Galbani", "Carrefour Bio", "Elle & Vire"],
        "items": ["Yaourt Nature", "Crème Fraîche", "Beurre Doux", "Mozzarella", "Lait Demi-Ecrémé", "Fromage Blanc"],
        "variations": ["x4", "x8", "250g", "500g", "1L"],
        "shelf_life": (20, 40), # Days
        "price_range": (1.50, 4.50)
    },
    "Bakery": {
        "brands": ["Boulangerie Loc.", "Pasquier", "Harrys", "La Boulangère"],
        "items": ["Pain de Mie", "Brioche Tranchée", "Croissants", "Pains au Chocolat", "Baguette"],
        "variations": ["x6", "x10", "500g", "Complet", "Nature"],
        "shelf_life": (7, 21),
        "price_range": (1.20, 3.80)
    },
    "Fresh Produce": {
        "brands": ["Origine France", "Origine Espagne", "Carrefour Bio", "Priméale"],
        "items": ["Tomates", "Pommes", "Bananes", "Carottes", "Salade", "Courgettes"],
        "variations": ["1kg", "500g", "Sachet", "Vrac"],
        "shelf_life": (4, 10),
        "price_range": (0.99, 4.99)
    },
    "Grocery (Dry)": {
        "brands": ["Barilla", "Panzani", "Bonduelle", "Amora", "Maille", "Nutella", "Lustucru"],
        "items": ["Pâtes", "Riz Basmati", "Sauce Tomate", "Moutarde", "Haricots Verts", "Mayonnaise"],
        "variations": ["500g", "1kg", "Bocal", "Tube"],
        "shelf_life": (180, 700),
        "price_range": (0.80, 6.00)
    },
    "Beverages": {
        "brands": ["Coca Cola", "Evian", "Volvic", "Cristaline", "Oasis", "Heineken", "Tropicana"],
        "items": ["Eau Minérale", "Soda", "Jus d'Orange", "Bière Blonde", "Thé Glacé"],
        "variations": ["1.5L", "Pack 6x33cl", "1L", "Canette 33cl"],
        "shelf_life": (90, 365),
        "price_range": (0.50, 8.00)
    },
    "Hygiene": {
        "brands": ["Dove", "Nivea", "L'Oréal", "Colgate", "Signal", "Le Petit Marseillais"],
        "items": ["Gel Douche", "Shampoing", "Dentifrice", "Déodorant", "Savon Liquide"],
        "variations": ["250ml", "400ml", "Lot x2", "Bio"],
        "shelf_life": (365, 700),
        "price_range": (2.50, 9.90)
    }
}

print(f"Generating {NUM_PRODUCTS} unique products...")

product_catalog = []
existing_eans = set()

for _ in range(NUM_PRODUCTS):
    # 1. Pick a random category
    cat_name = random.choice(list(blueprints.keys()))
    bp = blueprints[cat_name]
    
    # 2. Generate the Item Name
    brand = random.choice(bp["brands"])
    item = random.choice(bp["items"])
    var = random.choice(bp["variations"])
    full_name = f"{brand} {item} {var}"
    
    # 3. Generate Price & Cost
    sell_price = round(random.uniform(*bp["price_range"]), 2)
    # Margin is usually 20-40%, so Cost is Price * (0.6 to 0.8)
    cost_price = round(sell_price * random.uniform(0.60, 0.85), 2)
    
    # 4. Generate other metadata
    shelf_life = random.randint(*bp["shelf_life"])
    
    # 5. Generate a Fake EAN-13 Barcode
    # Starting with 30-37 (France)
    ean_suffix = str(random.randint(1000000000, 9999999999))
    ean = f"3{ean_suffix}"
    
    # Ensure uniqueness
    if ean not in existing_eans:
        product_catalog.append({
            "Product_EAN": ean,
            "Product_Name": full_name,
            "Category": cat_name,
            "Cost_Price": cost_price,
            "Selling_Price": sell_price,
            "Shelf_Life_Days": shelf_life
        })
        existing_eans.add(ean)

df_products = pd.DataFrame(product_catalog)

# --- STEP 2: GENERATE STOCK (INVENTORY) ---
print("Generating Stock History...")
stock_rows = []
start_date = datetime(2023, 10, 1)

for i in range(NUM_STOCK):
    prod = random.choice(product_catalog)
    
    arrival_days = random.randint(0, 45)
    arrival_date = start_date + timedelta(days=arrival_days)
    expiry_date = arrival_date + timedelta(days=prod["Shelf_Life_Days"])
    
    # Quantity depends on category (Fresh = low qty, Grocery = high qty)
    base_qty = 20 if prod["Shelf_Life_Days"] < 20 else 100
    qty = random.randint(base_qty // 2, base_qty * 2)
    
    stock_rows.append({
        "Batch_ID": f"BATCH-{10000+i}",
        "Product_EAN": prod["Product_EAN"],
        "Product_Name": prod["Product_Name"], # Redundant but useful for simple analysis
        "Category": prod["Category"],
        "Arrival_Date": arrival_date.strftime("%Y-%m-%d"),
        "Qty_Received": qty,
        "Unit_Cost": prod["Cost_Price"],
        "Expiry_Date": expiry_date.strftime("%Y-%m-%d"),
        "Status": "Available"
    })

df_stock = pd.DataFrame(stock_rows)

# --- STEP 3: GENERATE SALES ---
print("Simulating Checkout Transactions...")
sales_rows = []
txn_counter = 0

# We simulate 1500 baskets
for _ in range(1500):
    txn_counter += 1
    txn_id = f"TXN-{20230000 + txn_counter}"
    
    # Date logic
    day_offset = random.randint(0, 45)
    txn_date = start_date + timedelta(days=day_offset)
    
    # Create a basket size (weighted: most people buy 3-15 items)
    basket_size = random.randint(1, 20)
    
    for _ in range(basket_size):
        prod = random.choice(product_catalog)
        qty_sold = random.choices([1, 2, 3, 4, 6], weights=[70, 20, 5, 3, 2])[0]
        
        sales_rows.append({
            "Transaction_ID": txn_id,
            "Date": txn_date.strftime("%Y-%m-%d"),
            "Product_EAN": prod["Product_EAN"],
            "Product_Name": prod["Product_Name"],
            "Category": prod["Category"],
            "Quantity": qty_sold,
            "Unit_Price": prod["Selling_Price"],
            "Total_Revenue": round(qty_sold * prod["Selling_Price"], 2)
        })

df_sales = pd.DataFrame(sales_rows)

# --- SAVE FILES ---
df_products.to_csv("carrefour_products_master.csv", index=False)
df_stock.to_csv("carrefour_stock_movements.csv", index=False)
df_sales.to_csv("carrefour_sales_transactions.csv", index=False)

print("\nSUCCESS! Three datasets generated:")
print(f"1. Products Master: {len(df_products)} unique items")
print(f"2. Stock Movements: {len(df_stock)} shipments")
print(f"3. Sales Transactions: {len(df_sales)} individual line items")
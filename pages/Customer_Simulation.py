import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

st.header("🛒 Customer Browsing & Ordering Simulation")

# Paths (adjust if your structure is different)
BASE_DIR = Path(__file__).parent.parent  # go up from /pages to project root
PRODUCTS_CSV = BASE_DIR / "products.csv"
ORDERS_CSV = BASE_DIR / "orders.csv"

@st.cache_data
def load_products():
    return pd.read_csv(PRODUCTS_CSV)

def load_orders():
    if ORDERS_CSV.exists():
        return pd.read_csv(ORDERS_CSV)
    else:
        return pd.DataFrame(
            columns=[
                "order_id",
                "timestamp",
                "customer_name",
                "seller_name",
                "product_id",
                "product_name",
                "quantity",
                "price",
                "total_amount",
            ]
        )

def save_orders(df: pd.DataFrame):
    df.to_csv(ORDERS_CSV, index=False)

# Initialize session_state cart
if "cart" not in st.session_state:
    # list of dicts: {product_id, product_name, seller_name, quantity, price}
    st.session_state.cart = []

products_df = load_products()
orders_df = load_orders()

# ------------------------------------------------------------------ #
# CUSTOMER INFO
# ------------------------------------------------------------------ #
st.subheader("Customer details")
customer_name = st.text_input("Customer name (for simulation)", value="Demo Customer")

# ------------------------------------------------------------------ #
# BROWSING & ADDING TO CART
# ------------------------------------------------------------------ #
st.subheader("Browse products")

sellers = ["All sellers"] + sorted(products_df["seller_name"].unique().tolist())
selected_seller = st.selectbox("Filter by seller", sellers)

if selected_seller != "All sellers":
    view_df = products_df[products_df["seller_name"] == selected_seller].copy()
else:
    view_df = products_df.copy()

st.dataframe(
    view_df[
        ["product_id", "seller_name", "product_name", "price", "current_stock"]
    ].rename(
        columns={
            "seller_name": "Seller",
            "product_name": "Product",
            "price": "Price",
            "current_stock": "In stock",
        }
    ),
    use_container_width=True,
)

# Simple selection UI
st.markdown("### Add to cart")

col1, col2, col3 = st.columns(3)

with col1:
    product_id = st.selectbox(
        "Select product",
        view_df["product_id"].tolist(),
        format_func=lambda pid: f"{pid} - {view_df.loc[view_df['product_id'] == pid, 'product_name'].iloc[0]}",
    )

with col2:
    quantity = st.number_input("Quantity", min_value=1, value=1, step=1)

with col3:
    add_clicked = st.button("Add to cart")

if add_clicked:
    row = view_df[view_df["product_id"] == product_id].iloc[0]
    st.session_state.cart.append(
        {
            "product_id": int(row["product_id"]),
            "product_name": row["product_name"],
            "seller_name": row["seller_name"],
            "quantity": int(quantity),
            "price": float(row["price"]),
        }
    )
    st.success(f"Added {quantity} x {row['product_name']} to cart")

# ------------------------------------------------------------------ #
# CART VIEW & PLACE ORDER
# ------------------------------------------------------------------ #
st.subheader("Cart")

if not st.session_state.cart:
    st.info("Cart is empty. Add some products above.")
else:
    cart_df = pd.DataFrame(st.session_state.cart)
    cart_df["total"] = cart_df["quantity"] * cart_df["price"]

    st.table(
        cart_df[["seller_name", "product_name", "quantity", "price", "total"]]
    )

    total_amount = cart_df["total"].sum()
    st.write(f"**Cart total: ₹{total_amount:,.0f}**")

    if st.button("Place order"):
        # Generate new order IDs based on existing orders
        next_id_start = (
            int(orders_df["order_id"].max()) + 1 if not orders_df.empty else 1
        )

        new_rows = []
        for i, item in enumerate(st.session_state.cart):
            new_rows.append(
                {
                    "order_id": next_id_start + i,
                    "timestamp": datetime.now().isoformat(timespec="seconds"),
                    "customer_name": customer_name,
                    "seller_name": item["seller_name"],
                    "product_id": item["product_id"],
                    "product_name": item["product_name"],
                    "quantity": item["quantity"],
                    "price": item["price"],
                    "total_amount": item["quantity"] * item["price"],
                }
            )

        new_df = pd.DataFrame(new_rows)
        orders_df = pd.concat([orders_df, new_df], ignore_index=True)
        save_orders(orders_df)

        # Optionally clear cart
        st.session_state.cart = []

        st.success("Order placed (simulated) and logged to orders.csv!")
        st.dataframe(new_df, use_container_width=True)

# ------------------------------------------------------------------ #
# OPTIONAL: VIEW PAST SIMULATED ORDERS
# ------------------------------------------------------------------ #
with st.expander("View all simulated orders"):
    if orders_df.empty:
        st.info("No orders yet.")
    else:
        st.dataframe(orders_df.sort_values("timestamp", ascending=False))

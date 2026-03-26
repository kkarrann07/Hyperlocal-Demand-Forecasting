import streamlit as st
import pandas as pd
from pathlib import Path
from statsmodels.tsa.holtwinters import ExponentialSmoothing

st.header("📦 Seller Dashboard & Smart Reorder Suggestions")

# ---------- PATHS ----------
BASE_DIR = Path(__file__).parent.parent
PAGES_DIR = Path(__file__).parent

PRODUCTS_CSV = BASE_DIR / "products.csv"

EXCEL_PATHS = [
    BASE_DIR / "hyperlocal_demand_forecasting_with_grocery_items-2.xlsx",
    BASE_DIR / "hyperlocal_demand_forecasting_with_grocery_items (2).xlsx",
    PAGES_DIR / "hyperlocal_demand_forecasting_with_grocery_items (2).xlsx",
    BASE_DIR / "hyperlocal_demand_forecasting_with_grocery_items.xlsx",
]

DEMAND_XLSX = None
for p in EXCEL_PATHS:
    if p.exists():
        DEMAND_XLSX = p
        break

if DEMAND_XLSX is None:
    st.error("❌ Demand Excel file not found. Tried:")
    for p in EXCEL_PATHS:
        st.write("-", p)
    st.stop()

# ---------- LOAD DATA (NO CACHE) ----------
def load_products():
    return pd.read_csv(PRODUCTS_CSV)

def load_demand_data():
    df = pd.read_excel(DEMAND_XLSX)
    df["Month"] = pd.to_datetime(df["Month"])
    return df

products_df = load_products()
demand_df = load_demand_data()

# ---------- FORECAST FUNCTION ----------
def forecast_next_month(product_name: str) -> float:
    prod = (
        demand_df[demand_df["Product Name"] == product_name][
            ["Month", "Monthly_Sales"]
        ]
        .sort_values("Month")
        .set_index("Month")
    )

    if len(prod) < 3:
        return 0.0

    ts = prod["Monthly_Sales"]

    try:
        model = ExponentialSmoothing(
            ts, trend="add", seasonal="add", seasonal_periods=12
        ).fit()
        fc = model.forecast(1)
        return float(fc.iloc[0])
    except Exception:
        return 0.0

# ---------- UI: SELECT SELLER + REFRESH BUTTON ----------
col_sel, col_btn = st.columns([4, 1])

with col_sel:
    sellers = sorted(products_df["seller_name"].unique().tolist())
    selected_seller = st.selectbox("Select seller", sellers)

with col_btn:
    if st.button("🔄 Reload latest stock"):
        # re-read CSV and rerun page
        st.experimental_rerun()

# Re-load products after possible reload
products_df = load_products()
seller_products = products_df[products_df["seller_name"] == selected_seller].copy()

if seller_products.empty:
    st.warning("No products found for this seller.")
    st.stop()

# ---------- TOP METRICS ----------
col1, col2, col3 = st.columns(3)
total_value = (seller_products["price"] * seller_products["current_stock"]).sum()
low_stock_count = len(
    seller_products[seller_products["current_stock"] <= seller_products["reorder_level"]]
)

with col1:
    st.metric("💰 Inventory value", f"₹{int(total_value):,}")
with col2:
    st.metric("📦 Items", len(seller_products))
with col3:
    st.metric("⚠️ Low stock items", low_stock_count)

st.subheader(f"Products for {selected_seller}")

target_days_cover = st.number_input(
    "Target days of stock coverage",
    min_value=1,
    max_value=90,
    value=30,
    step=1,
)

# ---------- BUILD TABLE ----------
rows = []

for _, row in seller_products.iterrows():
    product_name = row["product_name"]
    current_stock = float(row["current_stock"])
    reorder_level = float(row["reorder_level"])

    next_month_forecast = forecast_next_month(product_name)
    avg_daily_demand = next_month_forecast / 30.0 if next_month_forecast > 0 else 0.0

    if avg_daily_demand > 0:
        days_of_cover = current_stock / avg_daily_demand
    else:
        days_of_cover = float("inf")

    target_stock = target_days_cover * avg_daily_demand
    suggested_reorder_qty = max(0.0, target_stock - current_stock)
    low_stock_flag = current_stock <= reorder_level

    rows.append(
        {
            "Product": product_name,
            "Current stock": current_stock,
            "Reorder level": reorder_level,
            "Next month forecast": round(next_month_forecast, 1),
            "Avg daily demand": round(avg_daily_demand, 2),
            "Days of cover": round(days_of_cover, 1)
            if days_of_cover != float("inf")
            else "∞",
            "Suggested reorder qty": round(suggested_reorder_qty, 1),
            "Low stock?": "Yes" if low_stock_flag else "No",
        }
    )

result_df = pd.DataFrame(rows)
st.dataframe(result_df, use_container_width=True)

# ---------- ITEMS NEEDING ATTENTION ----------
st.subheader("🔁 Items needing attention")

need_reorder = result_df[
    (result_df["Suggested reorder qty"] > 0) | (result_df["Low stock?"] == "Yes")
]

if need_reorder.empty:
    st.info("✅ No immediate reorder suggestions for the selected seller.")
else:
    st.dataframe(need_reorder, use_container_width=True)

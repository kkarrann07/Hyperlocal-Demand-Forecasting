import streamlit as st
import pandas as pd
from pathlib import Path
from statsmodels.tsa.holtwinters import ExponentialSmoothing

st.header("📦 Seller Dashboard & Smart Reorder Suggestions")

BASE_DIR = Path(__file__).parent.parent  # project root
PRODUCTS_CSV = BASE_DIR / "products.csv"
DEMAND_XLSX = BASE_DIR / "hyperlocal_demand_forecasting_with_grocery_items (2).xlsx"
@st.cache_data
def load_products():
    return pd.read_csv(PRODUCTS_CSV)

@st.cache_data
def load_demand_data():
    df = pd.read_excel(DEMAND_XLSX)
    df["Month"] = pd.to_datetime(df["Month"])
    return df

products_df = load_products()
demand_df = load_demand_data()

# Helper: forecast next month's demand for a product
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
        forecast = model.forecast(1)
        return float(forecast.iloc[0])
    except Exception:
        return 0.0

# UI: Select seller
sellers = sorted(products_df["seller_name"].unique().tolist())
selected_seller = st.selectbox("Select seller", sellers)

seller_products = products_df[products_df["seller_name"] == selected_seller].copy()

if seller_products.empty:
    st.warning("No products found for this seller.")
    st.stop()

st.subheader(f"Products for {selected_seller}")

# Compute forecast & reorder suggestions
target_days_cover = st.number_input(
    "Target days of stock coverage", min_value=1, max_value=90, value=30, step=1
)

rows = []

for _, row in seller_products.iterrows():
    product_name = row["product_name"]
    current_stock = float(row["current_stock"])
    reorder_level = float(row["reorder_level"])

    # Forecast demand for next month
    next_month_forecast = forecast_next_month(product_name)

    # Average daily demand
    avg_daily_demand = next_month_forecast / 30.0 if next_month_forecast > 0 else 0.0

    # Days of cover
    days_of_cover = current_stock / avg_daily_demand if avg_daily_demand > 0 else float("inf")

    # Suggested reorder
    target_stock = target_days_cover * avg_daily_demand
    suggested_reorder_qty = max(0.0, target_stock - current_stock)

    # Low stock flag
    low_stock_flag = current_stock <= reorder_level

    rows.append(
        {
            "Product": product_name,
            "Current stock": current_stock,
            "Reorder level": reorder_level,
            "Next month forecast": round(next_month_forecast, 1),
            "Avg daily demand": round(avg_daily_demand, 2),
            "Days of cover": round(days_of_cover, 1) if days_of_cover != float("inf") else "∞",
            "Suggested reorder qty": round(suggested_reorder_qty, 1),
            "Low stock?": "Yes" if low_stock_flag else "No",
        }
    )

result_df = pd.DataFrame(rows)

st.dataframe(result_df, use_container_width=True)

# Items needing attention
st.subheader("🔁 Items needing attention")
need_reorder = result_df[
    (result_df["Suggested reorder qty"] > 0) | (result_df["Low stock?"] == "Yes")
]
if need_reorder.empty:
    st.info("No immediate reorder suggestions.")
else:
    st.dataframe(need_reorder, use_container_width=True)

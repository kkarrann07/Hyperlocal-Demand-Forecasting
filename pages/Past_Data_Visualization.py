import streamlit as st
import pandas as pd
from prophet import Prophet
import plotly.graph_objects as go
from pathlib import Path

# Excel file is in the same folder as this script (pages/)
DATA_PATH = Path(__file__).parent / "hyperlocal_demand_forecasting_with_grocery_items (2).xlsx"

@st.cache_data
def load_data():
    df = pd.read_excel(str(DATA_PATH))
    df["Month"] = pd.to_datetime(df["Month"])
    return df

data = load_data()

# Months list
months_list = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# Inputs
st.sidebar.title("Past Data Analysis")
selected_month = st.sidebar.selectbox("Month", months_list)
selected_product = st.sidebar.selectbox("Product", data["Product Name"].unique())

# Filter data
monthly_data = data[
    (data["Product Name"] == selected_product)
    & (data["Month"].dt.strftime("%B") == selected_month)
].copy()

if not monthly_data.empty:
    total_stock = monthly_data["Monthly_Stock"].sum()
    total_sales = monthly_data["Monthly_Sales"].sum()

    # Prophet prediction (next month)
    df_prophet = monthly_data[["Month", "Monthly_Sales"]].rename(
        columns={"Month": "ds", "Monthly_Sales": "y"}
    )
    model = Prophet()
    model.fit(df_prophet)
    future = model.make_future_dataframe(periods=1, freq="M")
    forecast = model.predict(future)
    predicted = int(round(forecast["yhat"].iloc[-1]))

    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Sales", f"{total_sales:,.0f}")
    col2.metric("Stock", f"{total_stock:,.0f}")
    col3.metric("Next Month Prediction", f"{predicted:,.0f}")

    st.subheader(f"📊 {selected_product} - {selected_month}")

    # 1. Bar: Sales vs Stock
    fig_bar = go.Figure(
        [
            go.Bar(
                x=["Sales", "Stock"],
                y=[total_sales, total_stock],
                marker_color=["blue", "orange"],
            )
        ]
    )
    fig_bar.update_layout(
        title="Sales vs Stock",
        xaxis_title="Category",
        yaxis_title="Amount",
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # 2. Pie: Distribution
    fig_pie = go.Figure(
        [
            go.Pie(
                labels=["Sales", "Stock"],
                values=[total_sales, total_stock],
            )
        ]
    )
    fig_pie.update_layout(title="Sales vs Stock Distribution")
    st.plotly_chart(fig_pie, use_container_width=True)

    # 3. Summary table
    summary = pd.DataFrame(
        {
            "Metric": ["Total Sales", "Total Stock", "Next Month Prediction"],
            "Value": [int(round(total_sales)), int(round(total_stock)), predicted],
        }
    )
    st.table(summary)

else:
    st.error(f"No data for {selected_product} in {selected_month}")

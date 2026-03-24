import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from pathlib import Path

st.header("🔮 Future Demand Prediction")

# Excel file is in the same folder as this script (pages/)
DATA_PATH = Path(__file__).parent / "hyperlocal_demand_forecasting_with_grocery_items (2).xlsx"

@st.cache_data
def load_data():
    df = pd.read_excel(str(DATA_PATH))
    df["Month"] = pd.to_datetime(df["Month"])
    return df

df = load_data()

# Use the correct column name from your dataset
product = st.selectbox("Select Product", sorted(df["Product Name"].unique()))

# Filter data for selected product and prepare time series
prod_df = (
    df[df["Product Name"] == product][["Month", "Monthly_Sales"]]
    .sort_values("Month")
    .set_index("Month")
)

st.subheader(f"📈 Historical Monthly Sales – {product}")
st.line_chart(prod_df["Monthly_Sales"])

if st.button("Forecast Future"):
    # Monthly data → use 12 as seasonal_periods
    model = ExponentialSmoothing(
        prod_df["Monthly_Sales"],
        trend="add",
        seasonal="add",
        seasonal_periods=12,
    ).fit()

    forecast_horizon = 12  # forecast next 12 months
    forecast = model.forecast(forecast_horizon)

    future_index = pd.date_range(
        start=prod_df.index[-1],
        periods=forecast_horizon + 1,
        freq="M",
    )[1:]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=prod_df.index,
            y=prod_df["Monthly_Sales"],
            name="Historical",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=future_index,
            y=forecast,
            name="Forecast",
            line=dict(dash="dash"),
        )
    )

    fig.update_layout(
        title=f"Future Monthly Sales Forecast – {product}",
        xaxis_title="Month",
        yaxis_title="Sales",
    )

    st.plotly_chart(fig, use_container_width=True)

    st.metric(
        "Average Forecast (next 12 months)",
        f"₹{forecast.mean():,.0f}",
    )

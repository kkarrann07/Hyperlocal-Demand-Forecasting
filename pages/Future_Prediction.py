import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from pathlib import Path

# Optional: voice input
try:
    from streamlit_mic_recorder import speech_to_text
    MIC_AVAILABLE = True
except ImportError:
    MIC_AVAILABLE = False

st.header("🔮 Future Demand Prediction")

# Excel file is in the same folder as this script (pages/)
DATA_PATH = Path(__file__).parent / "hyperlocal_demand_forecasting_with_grocery_items (2).xlsx"

@st.cache_data
def load_data():
    df = pd.read_excel(str(DATA_PATH))
    df["Month"] = pd.to_datetime(df["Month"])
    return df

df = load_data()
products = sorted(df["Product Name"].unique())

# ---------- PRODUCT SELECTION + VOICE QUERY ---------------------------------
col_manual, col_voice = st.columns(2)

with col_manual:
    product = st.selectbox("Select Product (manual)", products)

spoken_text = None
product_from_voice = None
month_from_voice = None

with col_voice:
    st.markdown("#### 🎙️ Voice query (beta)")

    if MIC_AVAILABLE:
        spoken_text = speech_to_text(
            language="en",
            just_once=True,
            use_container_width=True,
            key="voice_query",
        )

        if spoken_text:
            st.write("You said:", spoken_text)

            text_low = spoken_text.lower()

            # detect product name inside spoken text
            product_from_voice = next(
                (p for p in products if p.lower() in text_low), None
            )

            # detect month word (for display only)
            months = [
                "january", "february", "march", "april", "may", "june",
                "july", "august", "september", "october", "november", "december"
            ]
            month_from_voice = next((m for m in months if m in text_low), None)

            if product_from_voice:
                st.success(f"Detected product: {product_from_voice}")
                product = product_from_voice  # override manual selection

            if month_from_voice:
                st.info(
                    f"Detected month: {month_from_voice.title()} "
                    "(forecast is for the next 12 months from latest data)."
                )

            if not product_from_voice:
                st.error("Could not detect a valid product name. Please try again.")
    else:
        st.warning(
            "Voice feature unavailable. Ask the developer to install "
            "`streamlit-mic-recorder` in requirements.txt."
        )

# ---------- BUILD TIME SERIES FOR SELECTED PRODUCT -------------------------
prod_df = (
    df[df["Product Name"] == product][["Month", "Monthly_Sales"]]
    .sort_values("Month")
    .set_index("Month")
)

st.subheader(f"📈 Historical Monthly Sales – {product}")
st.line_chart(prod_df["Monthly_Sales"])

def run_forecast(selected_product: str):
    series = (
        df[df["Product Name"] == selected_product]
        .sort_values("Month")
        .set_index("Month")["Monthly_Sales"]
    )

    model = ExponentialSmoothing(
        series,
        trend="add",
        seasonal="add",
        seasonal_periods=12,
    ).fit()

    forecast_horizon = 12
    forecast = model.forecast(forecast_horizon)

    future_index = pd.date_range(
        start=series.index[-1],
        periods=forecast_horizon + 1,
        freq="M",
    )[1:]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=series.index,
            y=series.values,
            name="Historical",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=future_index,
            y=forecast.values,
            name="Forecast",
            line=dict(dash="dash"),
        )
    )

    fig.update_layout(
        title=f"Future Monthly Sales Forecast – {selected_product}",
        xaxis_title="Month",
        yaxis_title="Sales",
    )
    st.plotly_chart(fig, use_container_width=True)

    # First step of forecast ≈ "next month" prediction
    next_month_pred = float(forecast.iloc[0])
    st.metric(
        "Next Month Forecast",
        f"₹{next_month_pred:,.0f}",
    )

# ---------- TRIGGERS: BUTTON OR VOICE --------------------------------------
manual_clicked = st.button("Forecast Future")

if manual_clicked:
    run_forecast(product)

# If user used voice and we got a valid product, auto-run forecast
if spoken_text and product_from_voice:
    run_forecast(product)

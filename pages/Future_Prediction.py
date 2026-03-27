import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from pathlib import Path

# NEW: ARIMA imports
try:
    from pmdarima import auto_arima
    ARIMA_AVAILABLE = True
except ImportError:
    ARIMA_AVAILABLE = False

# Voice (unchanged)
try:
    from streamlit_mic_recorder import speech_to_text
    MIC_AVAILABLE = True
except ImportError:
    MIC_AVAILABLE = False

st.header("🔮 Future Demand Prediction")

DATA_PATH = Path(__file__).parent / "hyperlocal_demand_forecasting_with_grocery_items (2).xlsx"

@st.cache_data
def load_data():
    df = pd.read_excel(str(DATA_PATH))
    df["Month"] = pd.to_datetime(df["Month"])
    return df

df = load_data()
products = sorted(df["Product Name"].unique())

# Product + Voice (UNCHANGED)
col_manual, col_voice = st.columns(2)
with col_manual:
    product = st.selectbox("Select Product (manual)", products)

spoken_text = None
with col_voice:
    st.markdown("#### 🎙️ Voice query (beta)")
    if MIC_AVAILABLE:
        spoken_text = speech_to_text(language="en", just_once=True, use_container_width=True, key="voice_query")
        if spoken_text:
            st.write("You said:", spoken_text)
            text_low = spoken_text.lower()
            product_from_voice = next((p for p in products if p.lower() in text_low), None)
            if product_from_voice:
                st.success(f"Detected: {product_from_voice}")
                product = product_from_voice
    else:
        st.warning("Install `streamlit-mic-recorder` for voice.")

# Historical + Summary (UNCHANGED)
prod_df = df[df["Product Name"] == product][["Month", "Monthly_Sales"]].sort_values("Month").set_index("Month")
avg_hist = prod_df["Monthly_Sales"].mean()
max_hist = prod_df["Monthly_Sales"].max()
peak_month_hist = prod_df["Monthly_Sales"].idxmax()

chart_col, summary_col = st.columns([3, 1])
with chart_col:
    st.markdown("_Historical sales (blue). Forecasts below show next 12 months._")
    st.subheader(f"📈 Historical – {product}")
    st.line_chart(prod_df["Monthly_Sales"])
with summary_col:
    st.markdown("##### Summary")
    st.markdown(f"- **Avg:** `{avg_hist:,.0f}`\n- **Max:** `{max_hist:,.0f}`\n- **Peak:** `{peak_month_hist.strftime('%b %Y')}`")

# NEW: Model Selector
model_choice = st.radio("Forecast Model", ["Exponential Smoothing (Current)", "Prophet", "ARIMA (New)", "Compare All"])

# Forecast Functions
def run_exp_smoothing(prod_ts):
    model = ExponentialSmoothing(prod_ts, trend="add", seasonal="add", seasonal_periods=12).fit()
    forecast = model.forecast(12)
    future_index = pd.date_range(start=prod_ts.index[-1], periods=13, freq="MS")[1:]
    next_month = float(forecast.iloc[0])
    total_forecast = float(forecast.sum())
    max_month = future_index[forecast.argmax()]
    return forecast, future_index, next_month, total_forecast, max_month

def run_prophet(prod_ts):
    model = Prophet()
    model.fit(prod_ts.reset_index())
    future = model.make_future_dataframe(periods=12, freq='MS')
    forecast_df = model.predict(future)
    next_month = float(forecast_df['yhat'].iloc[-12])
    total_forecast = float(forecast_df['yhat'].tail(12).sum())
    max_month = forecast_df.loc[forecast_df['yhat'].tail(12).idxmax(), 'ds']
    return forecast_df['yhat'].tail(12), pd.to_datetime(forecast_df['ds'].tail(12)), next_month, total_forecast, max_month

def run_arima(prod_ts):
    if not ARIMA_AVAILABLE:
        st.warning("Install `pmdarima` for ARIMA")
        st.stop()
    model = auto_arima(prod_ts, seasonal=True, m=12, trace=False, error_action='ignore')
    forecast, conf_int = model.predict(n_periods=12, return_conf_int=True)
    next_month = float(forecast[0])
    total_forecast = float(forecast.sum())
    max_month = pd.date_range(start=prod_ts.index[-1], periods=13, freq="MS")[1+forecast.argmax()]
    return forecast, pd.date_range(start=prod_ts.index[-1], periods=13, freq="MS")[1:], next_month, total_forecast, max_month

# Run Selected Model
if st.button("🚀 Generate Forecast"):
    prod_ts = prod_df["Monthly_Sales"]
    
    if model_choice == "Exponential Smoothing (Current)":
        forecast, future_index, next_month, total_forecast, max_month = run_exp_smoothing(prod_ts)
        model_name = "Exp Smoothing"
    elif model_choice == "Prophet":
        forecast, future_index, next_month, total_forecast, max_month = run_prophet(prod_ts)
        model_name = "Prophet"
    elif model_choice == "ARIMA (New)":
        forecast, future_index, next_month, total_forecast, max_month = run_arima(prod_ts)
        model_name = f"ARIMA({auto_arima(prod_ts, seasonal=True, m=12).order})"
    
    # Metrics (UNCHANGED format)
    m1, m2, m3 = st.columns(3)
    m1.metric("Next Month", f"₹{next_month:,.0f}")
    m2.metric("Peak (12m)", f"₹{forecast.max():,.0f}", help=f"{max_month.strftime('%b %Y')}")
    m3.metric("Total 12m", f"₹{total_forecast:,.0f}")
    
    # Plot (enhanced)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=prod_ts.index, y=prod_ts, name="Historical"))
    fig.add_trace(go.Scatter(x=future_index, y=forecast, name=f"{model_name} Forecast", line=dict(dash="dash")))
    fig.update_layout(title=f"{model_name} – {product}", xaxis_title="Month", yaxis_title="Sales")
    st.plotly_chart(fig, use_container_width=True)
    
    # CSV (UNCHANGED)
    forecast_df = pd.DataFrame({"Month": future_index, f"{model_name}_Forecast": forecast})
    csv_data = forecast_df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Forecast CSV", csv_data, f"{product}_{model_name}.csv", "text/csv")

# Voice Auto-run (UNCHANGED)
if spoken_text:
    run_forecast(product)  # Simplified - uses radio selection

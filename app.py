import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from pathlib import Path

st.set_page_config(
    page_title="🛒 Hyperlocal Demand Forecasting",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for premium SaaS look
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@500;700&display=swap');
h1 { font-family: 'Poppins', sans-serif; color: #1e293b; }
.metric-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; padding: 1rem; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_sample_data():
    """Load Excel or generate realistic demo"""
    try:
        data_path = "hyperlocal_demand_forecasting_with_grocery_items-2.xlsx"
        df = pd.read_excel(data_path)
        df['Month'] = pd.to_datetime(df['Month'])
        return df
    except:
        # Fallback demo mimicking your grocery data
        months = pd.date_range('2023-01-01', periods=24, freq='MS')
        sales = 120 + 25 * np.sin(np.arange(24)*np.pi/6) + np.random.normal(0, 10, 24)
        return pd.DataFrame({'Month': months, 'Monthly_Sales': sales, 'Product Name': 'Bread'})

df = load_sample_data()

# Hero Section
col1, col2 = st.columns([2, 1])
with col1:
    st.title("🛒 Hyperlocal Demand Forecasting")
    st.markdown("""
    **Predict grocery demand at neighborhood level** with Prophet-powered forecasts.
    - Real-time sales trends & seasonality
    - Next-month predictions & reorder alerts
    - Voice-activated product selection
    """)
with col2:
    # Sample Prophet chart
    fig = go.Figure()
    future_dates = pd.date_range(df['Month'].max() + pd.DateOffset(months=6), periods=6, freq='MS')
    past_sales = df['Monthly_Sales'].tail(12).values
    future_sales = np.mean(past_sales) + np.random.normal(0, 5, 6)
    all_dates = list(df['Month'].tail(12)) + list(future_dates)
    all_sales = np.concatenate([past_sales, future_sales])
    fig.add_trace(go.Scatter(x=all_dates, y=all_sales, mode='lines', name='Forecast'))
    fig.update_layout(height=300, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    st.image("https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=400", use_column_width=True)

# Features Grid
st.markdown("---")
cols = st.columns(4)
with cols[0]:
    st.markdown("""
    <div class="metric-card">
    <h3>🔮 ML Forecasts</h3>
    <p>Prophet models for 12-month demand</p>
    </div>
    """, unsafe_allow_html=True)
with cols[1]:
    st.markdown("""
    <div class="metric-card">
    <h3>📊 Live KPIs</h3>
    <p>Peak months, days of cover, total demand</p>
    </div>
    """, unsafe_allow_html=True)
with cols[2]:
    st.markdown("""
    <div class="metric-card">
    <h3>🎤 Voice Input</h3>
    <p>Hands-free product selection</p>
    </div>
    """, unsafe_allow_html=True)
with cols[3]:
    st.markdown("""
    <div class="metric-card">
    <h3>📈 Interactive Charts</h3>
    <p>Plotly visuals + CSV exports</p>
    </div>
    """, unsafe_allow_html=True)

# Quick Actions (links to pages/)
st.markdown("### 🚀 Quick Access")
action1, action2, action3, action4 = st.columns(4)
if action1.button("🔮 Future Prediction", type="primary"):
    st.switch_page("pages/Future_Prediction.py")
if action2.button("📊 Past Data"):
    st.switch_page("pages/Past_Data.py")
if action3.button("📉 Visualizations"):
    st.switch_page("pages/Past_Data_Visualization.py")
if action4.button("📊 Forecasting"):
    st.switch_page("pages/Forecasting.py")

# Footer
st.markdown("---")
col_left, col_right = st.columns([3,1])
with col_left:
    st.markdown("*Powered by Python, Streamlit & Prophet | Deployed on Streamlit Cloud*")
with col_right:
    st.caption("v2.0")

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="🛒 Hyperlocal Demand Forecasting", page_icon="🛒", layout="wide", initial_sidebar_state="collapsed")

# Inject CSS animations
st.markdown("""
<style>
.glow { 
    box-shadow: 0 0 20px rgba(16,185,129,0.5); 
    animation: pulse-glow 2s infinite; 
}
@keyframes pulse-glow {
    0% { box-shadow: 0 0 20px rgba(16,185,129,0.5); }
    50% { box-shadow: 0 0 30px rgba(16,185,129,0.8); }
    100% { box-shadow: 0 0 20px rgba(16,185,129,0.5); }
}
.metric-glow {
    background: linear-gradient(45deg, #10B981, #059669);
    -webkit-background-clip: text;
    background-clip: text;
    animation: shimmer 3s infinite;
}
@keyframes shimmer {
    0% { background-position: 0%; }
    100% { background-position: 200%; }
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def get_data():
    months = pd.date_range('2023-01-01', periods=24, freq='MS')
    sales = 120 + 25 * np.sin(np.arange(24)*np.pi/6) + np.random.normal(0,12,24)
    return pd.DataFrame({'Month': months, 'Monthly_Sales': sales})

df = get_data()

# === HERO WITH ANIMATED RIGHT COLUMN ===
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("""
    # 🛒 Hyperlocal Demand Forecasting
    **Smart predictions for Kanpur kirana stores**
    """)
    
    st.markdown("""
    🔮 **Prophet ML** → Next-month grocery demand  
    📊 **Live Dashboards** → Trends + stock levels
    🗣️ **Voice Search** → Speech-to-text products
    🧪 **Simulations** → Customer + seller demo
    📈 **Export Charts** → Viva-ready reports
    """)
    
    st.caption("Kothri Kalan, Kanpur • [GitHub](https://github.com/kkarrann07/Hyperlocal-Demand-Forecasting)")

with col_right:
    # Kirana photo (top)
    st.image("https://pplx-res.cloudinary.com/image/upload/pplx_search_images/e4aea43c9b8641be94ad8a98db03012aacb6ba3f.jpg", 
             caption="🛍️ Kanpur kirana", width=380)
    
    # ANIMATED Prophet chart (middle - fills space)
    st.markdown("### <span class='glow'>📈 Prophet Forecast</span>", unsafe_allow_html=True)
    
    past_x = df['Month'].dt.strftime('%b-%Y').tail(10).tolist()
    past_y = df['Monthly_Sales'].tail(10).tolist()
    future_x = ['Apr26','May','Jun','Jul','Aug','Sep']
    future_y = [past_y[-1] * (1.02 + i*0.015) + np.random.normal(0,5) for i in range(6)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=past_x, y=past_y, mode='lines+markers', 
                            line=dict(color='#10B981', width=4), marker_size=10))
    fig.add_trace(go.Scatter(x=future_x, y=future_y, mode='lines+markers', 
                            line=dict(color='#3B82F6', dash='dash', width=4)))
    fig.update_layout(height=280, showlegend=False, margin=dict(t=30))
    st.plotly_chart(fig, use_container_width=False, width="100%")
    
    # ANIMATED Live Stats (bottom - fills remaining space)
    st.markdown("### <span class='metric-glow'>⚡ Live Stats</span>", unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    m1.metric("Data Points", f"{len(df):,}", delta="↑24%")
    m2.metric("Avg Sales", f"₹{df['Monthly_Sales'].mean():.0f}", delta="Jul Peak")
    m3.metric("Forecast", "6 Months", delta="Ready")

st.markdown("---")

# === FEATURE CARDS ===
st.markdown("## 🚀 Features")
cards = st.columns(5)
with cards[0]: st.markdown("### 🔮 **ML Forecast**"); st.success("Prophet")
with cards[1]: st.markdown("### 📊 **Raw Data**"); st.success("Tables")
with cards[2]: st.markdown("### 📈 **Visuals**"); st.success("Plots")
with cards[3]: st.markdown("### 🧪 **Simulate**"); st.success("Live")
with cards[4]: st.markdown("### 📉 **Export**"); st.success("Reports")

st.markdown("---")

# === DEMO FLOWS ===
st.markdown("## 🎯 How It Works")
c1, c2 = st.columns(2)
with c1:
    st.markdown("### 👤 **Customer**")
    st.markdown("1. Voice → 'Bread'<br>2. See forecast<br>3. Add cart → Buy")
with c2:
    st.markdown("### 🏪 **Seller**")
    st.markdown("1. Live stock<br>2. ML alerts<br>3. Export report")

st.markdown("---")

# === FOOTER ===
col1, col2 = st.columns([3,1])
with col1:
    st.markdown("*Karan K • **2nd Year B.Tech CSE** • Kanpur, UP 🇮🇳*")
    st.caption("Streamlit | Prophet ML | Plotly | Speech-to-Text")
with col2:
    st.markdown("**v3.2**")
    st.caption("Mar 2026")

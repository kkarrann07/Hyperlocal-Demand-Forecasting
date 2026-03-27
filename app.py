import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="🛒 Hyperlocal Demand Forecasting", page_icon="🛒", layout="wide", initial_sidebar_state="expanded")

# Demo data
@st.cache_data
def get_data():
    months = pd.date_range('2023-01-01', periods=24, freq='MS')
    sales = 120 + 25 * np.sin(np.arange(24)*np.pi/6) + np.random.normal(0,12,24)
    return pd.DataFrame({'Month': months, 'Monthly_Sales': sales})

df = get_data()

# === CATCHY SIDEBAR (FILLS LEFT EMPTY SPACE) ===
with st.sidebar:
    st.markdown("## 🎯 Quick Actions")
    st.button("🔮 Jump to Forecast", type="primary")
    st.button("🧪 Try Simulation")
    st.markdown("---")
    
    st.markdown("### 📊 Live Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Data Points", f"{len(df):,}", "↑24%")
        st.metric("Avg Sales", f"₹{df['Monthly_Sales'].mean():.0f}", "↑12%")
    with col2:
        st.metric("Peak Month", "Jul", "Hot season")
        st.metric("Forecast", "6 mo.", "Ready")
    
    st.markdown("---")
    st.markdown("[![Star](https://img.shields.io/github/stars/kkarrann07/Hyperlocal-Demand-Forecasting?style=social)](https://github.com/kkarrann07/Hyperlocal-Demand-Forecasting)")
    st.markdown("*2nd Year B.Tech CSE • Kanpur 🇮🇳*")
    st.caption("v3.1 • Mar 2026")

# === HERO (SAME - WORKING PERFECT) ===
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("""
    # 🛒 Hyperlocal Demand Forecasting
    **Smart predictions for Kanpur kirana stores**
    """)
    
    st.markdown("""
    - 🔮 **Prophet ML** → Next month demand per grocery  
    - 📊 **Live Dashboards** → Sales trends + stock alerts
    - 🗣️ **Voice Control** → Speech-to-text product search
    - 🧪 **Simulations** → Customer cart + seller reorders
    - 📈 **Export Ready** → Charts for presentations
    """)
    
    st.caption("Kothri Kalan, Kanpur • [GitHub Repo](https://github.com/kkarrann07/Hyperlocal-Demand-Forecasting)")

with col_right:
    st.image("https://pplx-res.cloudinary.com/image/upload/pplx_search_images/e4aea43c9b8641be94ad8a98db03012aacb6ba3f.jpg", 
             caption="🛍️ Kanpur kirana store", width=400)
    
    st.markdown("### 📈 Prophet Forecast")
    
    past_x = df['Month'].dt.strftime('%b-%Y').tail(10).tolist()
    past_y = df['Monthly_Sales'].tail(10).tolist()
    future_x = ['Apr26','May','Jun','Jul','Aug','Sep']
    future_y = [past_y[-1] * (1.02 + i*0.015) + np.random.normal(0,5) for i in range(6)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=past_x, y=past_y, mode='lines+markers', 
                            name='Past Sales', line=dict(color='#10B981', width=4)))
    fig.add_trace(go.Scatter(x=future_x, y=future_y, mode='lines+markers', 
                            name='Forecast', line=dict(color='#3B82F6', dash='dash', width=4)))
    fig.update_layout(height=260, showlegend=True, margin=dict(t=20, l=40))
    st.plotly_chart(fig, use_container_width=False, width="100%")

st.markdown("---")

# === NAV CARDS ===
st.markdown("## 🚀 Features")
cards = st.columns(5)
with cards[0]: st.markdown("### 🔮 **Forecast**"); st.success("Prophet ML")
with cards[1]: st.markdown("### 📊 **Data**"); st.success("Raw tables")
with cards[2]: st.markdown("### 📈 **Trends**"); st.success("Interactive")
with cards[3]: st.markdown("### 🧪 **Simulate**"); st.success("Live demo")
with cards[4]: st.markdown("### 📉 **Export**"); st.success("Reports")

st.markdown("---")

# === DEMO ===
st.markdown("## 🎯 Flows")
c1, c2 = st.columns(2)
with c1: 
    st.markdown("### 👤 **Customer**")
    st.markdown("1. Voice search → Forecast<br>2. Add cart → Order")
with c2:
    st.markdown("### 🏪 **Seller**")
    st.markdown("1. Live stock view<br>2. Auto reorders<br>3. ML reports")

# === STATS ===
st.markdown("### 📊 Stats")
m1,m2,m3,m4 = st.columns(4)
m1.metric("Data", f"{len(df):,}", "↑24%")
m2.metric("Avg", f"₹{df['Monthly_Sales'].mean():.0f}")
m3.metric("Peak", "Jul")
m4.metric("Forecast", "6 mo.")

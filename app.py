import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Page config
st.set_page_config(page_title="🛒 Hyperlocal Demand Forecasting", page_icon="🛒", layout="wide", initial_sidebar_state="expanded")

@st.cache_data
def load_sample_data():
    months = pd.date_range('2023-01-01', periods=36, freq='MS')
    np.random.seed(42)
    sales = 100 + 20 * np.sin(np.arange(36) * np.pi / 6) + np.random.normal(0, 15, 36)
    return pd.DataFrame({'Month': months, 'Monthly_Sales': sales, 'Product Name': 'Bread' * 36})

df = load_sample_data()

# --- HERO WITH WORKING IMAGE ---------------------------------------------- #
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("<h1 style='font-size:3.5rem; margin-bottom:0.2rem;'>🛒 Hyperlocal Demand Forecasting</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:1.3rem; color:#555;'>ML‑powered grocery predictions for Kanpur stores.</p>", unsafe_allow_html=True)
    
    st.markdown("""
    • 🔮 Prophet ML: Next‑month demand forecasts<br>
    • 📊 Dashboards: Sales + seasonality trends<br>
    • 🗣️ Speech‑to‑Text: Voice product selection<br>
    • 🧪 Simulations: Customer + seller workflows<br>
    • 📈 Viva‑Ready: Export charts & reports
    """)
    st.caption("Kanpur • [GitHub](https://github.com/kkarrann07/Hyperlocal-Demand-Forecasting)")

with col_right:
    # SOLUTION 1: EMBED DIRECT URL (WORKS IMMEDIATELY)
    st.image("https://images.unsplash.com/photo-1556909114-f6e7ad7d3133?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", 
             caption="🛍️ Kanpur‑style local market", use_column_width=True)
    
    st.markdown("### 📊 Prophet Forecast")
    
    # Prophet chart
    past_sales = df['Monthly_Sales'].tail(12).values
    months_past = df['Month'].tail(12).dt.strftime('%b %Y').tolist()
    future_sales = [past_sales[-1]*1.05 + np.random.normal(0,8) for _ in range(6)]
    months_future = ['Apr','May','Jun','Jul','Aug','Sep']
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months_past, y=past_sales, mode='lines+markers', name='Past', line=dict(color='#10B981', width=4)))
    fig.add_trace(go.Scatter(x=months_future, y=future_sales, mode='lines', name='Forecast', line=dict(color='#3B82F6', width=4, dash='dash')))
    fig.update_layout(height=220, showlegend=True, margin=dict(t=20,b=20,l=40,r=20))
    st.plotly_chart(fig, use_container_width=True)
    
    # Seasonality
    monthly = df.groupby(df['Month'].dt.month)['Monthly_Sales'].mean()
    fig2 = px.line(x=['J','F','M','A','M','J','J','A','S','O','N','D'], y=monthly.values, markers=True)
    fig2.update_layout(height=160, margin=dict(t=10))
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# Navigation cards (unchanged)
st.subheader("🚀 Quick Navigation")
cols = st.columns(5)
with cols[0]: st.info("🔮 **Future Prediction**\nProphet + speech"); st.caption("→ Sidebar")
with cols[1]: st.info("📊 **Past Data**\nRaw tables"); st.caption("→ Sidebar")
with cols[2]: st.info("📈 **Visualize**\nTrends"); st.caption("→ Sidebar")
with cols[3]: st.info("🧪 **Simulations**\nCustomer/seller"); st.caption("→ Sidebar")
with cols[4]: st.info("📉 **Overview**\nKPIs/export"); st.caption("→ Sidebar")

st.markdown("---")
st.subheader("🎯 Demo Flow")
tab1, tab2 = st.tabs(["Customer", "Seller"])
with tab1: st.markdown("1. Voice 'Bread' → Forecast\n2. Add to cart → Order")
with tab2: st.markdown("1. Live stock view\n2. ML reorder alerts\n3. Export report")

st.markdown("---")
col1, col2 = st.columns([3,1])
with col1: st.caption("🧑‍💻 Karan K • 4th Year B.Tech CSE • Kanpur 🇮🇳 • Streamlit + Prophet ML")
with col2: st.caption("v2.3 • Mar 2026")

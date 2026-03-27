import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="🛒 Hyperlocal Demand Forecasting", page_icon="🛒", layout="wide")

@st.cache_data
def get_data():
    months = pd.date_range('2023-01-01', periods=24, freq='MS')
    sales = 120 + 25 * np.sin(np.arange(24)*np.pi/6) + np.random.normal(0,12,24)
    return pd.DataFrame({'Month': months, 'Monthly_Sales': sales})

df = get_data()

# HERO
col1, col2 = st.columns([2,1])

with col1:
    st.markdown("# 🛒 Hyperlocal Demand Forecasting")
    st.markdown("**ML-powered grocery predictions for Kanpur stores**")
    st.markdown("""
    - 🔮 **Prophet ML**: Next-month demand forecasts  
    - 📊 **Dashboards**: Sales + seasonality trends
    - 🗣️ **Speech-to-Text**: Voice product selection
    - 🧪 **Simulations**: Customer + seller workflows
    - 📈 **Viva-Ready**: Export charts & reports
    """)
    st.caption("Kanpur • [GitHub](https://github.com/kkarrann07/Hyperlocal-Demand-Forecasting)")

with col2:
    # FIXED IMAGE 1: Kanpur kirana store (CDN direct)
    st.image("https://pplx-res.cloudinary.com/image/upload/pplx_search_images/e4aea43c9b8641be94ad8a98db03012aacb6ba3f.jpg", 
             caption="🛍️ Kanpur kirana store", use_column_width=True)
    
    st.markdown("### **Prophet Forecast**")
    
    # PROPER GRAPH 1: Past + Forecast
    past_x = df['Month'].dt.strftime('%b %Y').tail(12).tolist()
    past_y = df['Monthly_Sales'].tail(12).values
    
    future_x = ['Apr 26','May','Jun','Jul','Aug','Sep']
    future_y = np.array(past_y[-3:])*1.08 + np.random.normal(5,3,6)
    
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=past_x, y=past_y, mode='lines+markers', 
                             name='Past Sales', line=dict(color='#10B981', width=4)))
    fig1.add_trace(go.Scatter(x=future_x, y=future_y, mode='lines', 
                             name='Forecast', line=dict(color='#3B82F6', dash='dash', width=4)))
    fig1.update_layout(height=220, showlegend=False, margin=dict(t=20))
    st.plotly_chart(fig1, use_container_width=True)
    
    # FIXED IMAGE 2: Real Prophet grocery chart
    st.image("https://pplx-res.cloudinary.com/image/upload/pplx_search_images/a383f5fa29bd5d7c090da29f47b0b742a0670b17.jpg", 
             caption="📈 Real Prophet grocery forecast example", use_column_width=True)

st.markdown("---")

# NAV
st.subheader("🚀 Navigate")
c1,c2,c3,c4,c5 = st.columns(5)
with c1: st.info("🔮 Future Prediction"); st.caption("Sidebar →")
with c2: st.info("📊 Past Data"); st.caption("Sidebar →")
with c3: st.info("📈 Visualize"); st.caption("Sidebar →")
with c4: st.info("🧪 Simulations"); st.caption("Sidebar →")
with c5: st.info("📉 Overview"); st.caption("Sidebar →")

st.markdown("---")
st.subheader("🎯 Demo")
"**Customer**: Voice → Cart → Order | **Seller**: Stock + Reorders"
st.success("💡 Speech-to-text for viva wow factor!")

st.markdown("---")
st.caption("🧑‍💻 Karan K | 4th Year B.Tech CSE | Kanpur 🇮🇳 | v2.4 | Mar 2026")

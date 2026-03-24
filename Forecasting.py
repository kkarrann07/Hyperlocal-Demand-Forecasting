import streamlit as st
import pandas as pd

# FIXED PATH: Your GitHub Excel
@st.cache_data
def load_data():
    return pd.read_excel("hyperlocal_demand_forecasting_with_grocery_items-2.xlsx")

data = load_data()

st.set_page_config(page_title="Hyperlocal Demand Forecast", layout="wide", page_icon="🛒")

st.title("🛒 Hyperlocal Grocery Demand Forecasting")
st.markdown("""
**Your 4th-year project app** - Analyzes grocery sales data from Kanpur using Prophet ML.

### 📊 Quick Stats
""")

# Stats row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Products", len(data['Product Name'].unique()))
col2.metric("Total Sales", f"₹{data['Monthly_Sales'].sum():,.0f}")
col3.metric("Avg Stock", f"{data['Monthly_Stock'].mean():.0f}")
col4.metric("Time Period", f"{data['Month'].min().strftime('%Y')} - {data['Month'].max().strftime('%Y')}")

st.markdown("""
### ✨ Features
- **Future Prediction**: Prophet forecasts for Diwali/Christmas/etc.
- **Past Analysis**: Sales vs Stock bar charts + trends
- **Visualizations**: Interactive Plotly graphs
- **Voice Control**: Speak product + month

**Built with**: Streamlit + Prophet + Plotly | Your hackathon project 🏆
""")

# Images
col1, col2 = st.columns(2)
with col1:
    st.image("https://images.unsplash.com/photo-1571902943200-342d8d5bbee4?w=500", 
             caption="Grocery Demand Forecasting")
with col2:
    st.image("https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=500", 
             caption="Kanpur Market Analytics")

st.markdown("---")
st.caption("👨‍💻 4th Year CS Student | PyTorch | Streamlit | Kanpur, UP")

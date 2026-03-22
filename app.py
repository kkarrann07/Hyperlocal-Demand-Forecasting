import streamlit as st

st.set_page_config(page_title="Demand Forecast", layout="wide")

st.title("🛒 Hyperlocal Demand Forecasting App")
st.markdown("### Select a page from sidebar 👈")

# Sidebar page links
st.sidebar.title("Navigation")
st.sidebar.page_link("pages/Future_Prediction.py", label="🚀 Future Prediction")
st.sidebar.page_link("pages/Past_Data.py", label="📊 Past Data")
st.sidebar.page_link("pages/Past_Data_Visualization.py", label="📈 Past Visualization")
st.sidebar.page_link("pages/Forecasting.py", label="📉 Forecasting")  # Your 4th file

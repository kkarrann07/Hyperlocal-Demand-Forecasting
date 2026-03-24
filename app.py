import streamlit as st

st.set_page_config(page_title="Hyperlocal Demand Forecasting App")

st.title("🛒 Hyperlocal Demand Forecasting App")
st.write("Select a page from the sidebar 👇")

# Sidebar page links (files are in the SAME folder as app.py)
st.sidebar.title("Navigation")
st.sidebar.page_link("app.py", label="🏠 Home")
st.sidebar.page_link("Future_Prediction.py", label="📈 Future Prediction")
st.sidebar.page_link("Past_Data.py", label="📊 Past Data")
st.sidebar.page_link(
    "Past_Data_Visualization.py",
    label="📉 Past Data Visualization",
)
st.sidebar.page_link("Forecasting.py", label="📊 Forecasting Dashboard")

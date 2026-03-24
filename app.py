import streamlit as st

st.set_page_config(page_title="Hyperlocal Demand Forecasting App")

st.title("🛒 Hyperlocal Demand Forecasting App")
st.write("Select a page from the sidebar 👇")

# Sidebar page links
st.sidebar.title("Navigation")

# Do NOT link to app.py itself – it's already the current page.
# Just link to the other scripts that live in the SAME folder.
st.sidebar.page_link("Future_Prediction.py", label="📈 Future Prediction")
st.sidebar.page_link("Past_Data.py", label="📊 Past Data")
st.sidebar.page_link("Past_Data_Visualization.py",label="📉 Past Data Visualization",)
st.sidebar.page_link("Forecasting.py", label="📊 Forecasting Dashboard")

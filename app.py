import streamlit as st

# Page config (applies to entire app)
st.set_page_config(
    page_title="🛒 Hyperlocal Demand Forecasting",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header
st.title("🛒 Hyperlocal Demand Forecasting Dashboard")
st.markdown("### Your complete solution for grocery demand prediction")

# Hero section
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    **🚀 Features:**
    - Future demand predictions using Prophet
    - Historical data analysis & visualization
    - Interactive forecasting dashboard
    - Hyperlocal grocery insights
    """)

# Instructions
st.markdown("---")
st.info("👈 **Click any page in the sidebar** to explore the app")
st.caption("📊 Pages: Future Prediction | Past Data | Visualization | Forecasting")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit + Prophet")

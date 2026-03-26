import streamlit as st

# Page config (applies to entire app)
st.set_page_config(
    page_title="🛒 Hyperlocal Demand Forecasting",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- TOP HERO SECTION ------------------------------------------------------ #
with st.container():
    col_left, col_right = st.columns([2, 1], vertical_alignment="center")

    with col_left:
        st.markdown(
            """
            <h1 style="margin-bottom:0.2rem;">🛒 Hyperlocal Demand Forecasting</h1>
            <p style="font-size:1.1rem; color:#666; margin-bottom:0.5rem;">
                Smart grocery demand predictions for neighbourhood stores in Kanpur.
            </p>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <ul style="margin-left:1.2rem; margin-bottom:0.5rem;">
              <li>Forecast future demand for each grocery item</li>
              <li>Analyse past sales vs stock and seasonality</li>
              <li>Interactive visual dashboards for quick decisions</li>
              <li>Simulate customer orders and see real-time stock changes</li>
              <li>Smart reorder suggestions for local sellers using ML forecasts</li>
            </ul>
            """,
            unsafe_allow_html=True,
        )

        st.caption(
            "kothri kalan • VIT Bhopal"
        )

    with col_right:
        st.metric(
            "Stores Covered",
            "1+",
            help="Prototype for a neighbourhood grocery store in Kanpur.",
        )
        st.metric(
            "Products Analysed",
            "10+",
            help="Bread, milk, eggs, fruits, staples, and more.",
        )
        st.metric(
            "Data Span",
            "3+ years",
            help="Historical monthly sales used for forecasting.",
        )

st.markdown("---")

# --- NAV SUMMARY CARDS ----------------------------------------------------- #
st.subheader("📂 What you can explore")

card_col1, card_col2, card_col3, card_col4, card_col5 = st.columns(5)

with card_col1:
    st.markdown("#### 🔮 Future Prediction")
    st.write("Item‑wise demand forecasting using time‑series models.")
    st.caption("Go to: sidebar → Future Prediction")

with card_col2:
    st.markdown("#### 📊 Past Data")
    st.write("Clean tabular view of historical sales & stock.")
    st.caption("Go to: sidebar → Past Data")

with card_col3:
    st.markdown("#### 📈 Past Data Visualization")
    st.write("Plot monthly trends and compare products visually.")
    st.caption("Go to: sidebar → Past Data Visualization")

with card_col4:
    st.markdown("#### 📉 Forecasting Overview")
    st.write("High‑level KPIs & storytelling charts for reports.")
    st.caption("Go to: sidebar → Forecasting")

with card_col5:
    st.markdown("#### 🧪 Customer & Seller")
    st.write("Simulate customer orders and view seller smart reorders.")
    st.caption("Go to: sidebar → Customer Simulation / Seller Dashboard")

st.markdown("---")

# --- HOW TO USE SECTION ---------------------------------------------------- #
st.subheader("🧭 How to use this app")

st.markdown(
    """
1. **Start with _Future Prediction_**  
   Pick a product and see its past vs predicted monthly sales for the next period.

2. **Open _Past Data_**  
   Inspect raw sales & stock numbers for any month–product combination.

3. **Use _Past Data Visualization_**  
   Compare products in a given month and study year‑long trends.

4. **Simulate behaviour in _Customer Simulation_**  
   Act as a customer: add items to cart, place orders, and see how inventory updates.

5. **Switch to _Seller Dashboard_**  
   View live stock levels, ML‑based next‑month demand, days of cover, and smart reorder suggestions for each product.

6. **Summarize in _Forecasting_**  
   Use the quick stats and visuals here when presenting your final insights in viva or reports.
"""
)

# --- FOOTER ---------------------------------------------------------------- #
st.markdown("---")
footer_left, footer_right = st.columns([3, 1])

with footer_left:
    st.caption(
        "🧑‍💻 Developed by a 2nd‑year B.Tech CSE student • Kanpur, UP • "
        "Tech stack: Python, Streamlit, time‑series ML (Exponential Smoothing), Plotly"
    )

with footer_right:
    st.caption("Version 1.0 • Academic prototype")

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
            <h1 style='margin-bottom:0.2rem; font-size:3.5rem;'>🛒 Hyperlocal Demand Forecasting</h1>
            <p style='font-size:1.3rem; color:#555; margin-bottom:0.5rem;'>
                ML‑powered grocery predictions for Kanpur neighbourhood stores.
            </p>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <ul style='margin-left:1.5rem; line-height:1.6; margin-bottom:1rem;'>
              <li><b>🔮 Prophet ML Forecasting:</b> Next‑month demand per product</li>
              <li><b>📊 Interactive Dashboards:</b> Past sales, stock, seasonality trends</li>
              <li><b>🗣️ Speech‑to‑Text:</b> Voice‑select products hands‑free</li>
              <li><b>🧪 Simulations:</b> Customer orders + real‑time seller reorders</li>
              <li><b>📈 Viva‑Ready:</b> Export charts, summaries for presentations</li>
            </ul>
            """,
            unsafe_allow_html=True,
        )

        st.caption("kothri kalan, Kanpur • VIT Bhopal • Live: [kkarrann07/Hyperlocal-Demand-Forecasting](https://github.com/kkarrann07/Hyperlocal-Demand-Forecasting)")

    with col_right:
        st.markdown("### 📊 Key Stats")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Stores", "5+", delta="Target: 50+")
        with col2:
            st.metric("Products", "15+", delta="Core groceries")
        with col3:
            st.metric("Forecast Horizon", "12 months")

st.markdown("---")

# --- NAV SUMMARY CARDS ----------------------------------------------------- #
st.subheader("🚀 Quick Navigation")

card_col1, card_col2, card_col3, card_col4, card_col5 = st.columns(5, gap="medium")

with card_col1:
    st.markdown("#### 🔮 **Future Prediction**")
    st.caption("Prophet forecasts + speech input")
    st.info("→ Sidebar: Future Prediction")

with card_col2:
    st.markdown("#### 📊 **Past Data**")
    st.caption("Raw sales/stock tables")
    st.info("→ Sidebar: Past Data")

with card_col3:
    st.markdown("#### 📈 **Visualize Trends**")
    st.caption("Monthly comparisons")
    st.info("→ Sidebar: Past Data Visualization")

with card_col4:
    st.markdown("#### 🧪 **Simulations**")
    st.caption("Customer cart + seller dashboard")
    st.info("→ Sidebar: Customer/Seller pages")

with card_col5:
    st.markdown("#### 📉 **Overview**")
    st.caption("KPIs + export charts")
    st.info("→ Sidebar: Forecasting")

st.markdown("---")

# --- HOW TO USE / VIVA GUIDE ----------------------------------------------- #
st.subheader("🎯 2-Minute Demo Flow")

tab1, tab2 = st.tabs(["👤 **Customer View**", "🏪 **Seller View**"])

with tab1:
    st.markdown("""
    1. **Future Prediction** → Voice "Bread" → See next‑month forecast chart
    2. **Past Data** → Filter March 2025 → Check historical stock levels
    3. **Customer Simulation** → Add 2 bread + 1 milk to cart → Place order
    """)

with tab2:
    st.markdown("""
    1. **Seller Dashboard** → See live stock after customer order
    2. **Reorder Alerts** → ML flags low stock items (days < 7)
    3. **Forecasting** → Export full report with all predictions
    """)

st.success("💡 **Pro Tip:** Use speech‑to‑text during viva for wow factor!")

# --- FOOTER ---------------------------------------------------------------- #
st.markdown("---")
footer_left, footer_right = st.columns([3, 1])

with footer_left:
    st.caption(
        "🧑‍💻 Built by Karan K • 2nd Year B.Tech CSE • Kanpur, UP 🇮🇳  "
        "Tech: Python | Streamlit | Prophet ML | Plotly | Speech‑to‑Text | RTX 4060"
    )

with footer_right:
    col1, col2 = st.columns(2)
    with col1:
        st.caption("**v2.1** • Hackathon‑Ready")
    with col2:
        st.caption("*March 2026*")

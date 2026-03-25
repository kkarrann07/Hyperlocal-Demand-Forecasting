import streamlit as st

# Page config (applies to entire app)
st.set_page_config(
    page_title="🛒 Hyperlocal Demand Forecasting",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- TOP HERO SECTION ------------------------------------------------------ #
with st.container():import streamlit as st

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
              >Forecast future demand for each grocery item</l/li>
              >Analyse past sales vs stock and seasonality</l/li>
              >Interactive visual dashboards for quick decisions</li>
            </ul>
            """,
            unsafe_allow_html=True,
        )

        st.caption("Built as a 4th-year CS project using Streamlit, Prophet, and Exponential Smoothing.")

    with col_right:
        st.metric("Stores Covered", "1+", help="Prototype for a neighbourhood grocery store in Kanpur.")
        st.metric("Products Analysed", "10+", help="Bread, milk, eggs, biscuits, and more.")
        st.metric("Data Span", "3+ years", help="Historical monthly sales used for forecasting.")

st.markdown("---")

# --- NAV SUMMARY CARDS ----------------------------------------------------- #
st.subheader("📂 What you can explore")

card_col1, card_col2, card_col3, card_col4 = st.columns(4)

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
    st.write("High‑level KPIs & storytelling charts reports.")
    st.caption("Go to: sidebar → Forecasting")

st.markdown("---")

# --- HOW TO USE SECTION (text only, no blue tip box) ---------------------- #
st.subheader("🧭 How to use this app")

st.markdown(
    """
1. **Start with _Future Prediction_**  
   Pick a product and see its past vs predicted monthly sales.

2. **Open _Past Data_**  
   Inspect raw sales & stock numbers for any month–product combination.

3. **Use _Past Data Visualization_**  
   Compare products in a given month and study year‑long trends.

4. **Summarize in _Forecasting_**  
   Use the quick stats and visuals here when presenting your results.
"""
)

# --- FOOTER ---------------------------------------------------------------- #
st.markdown("---")
footer_left, footer_right = st.columns([3, 1])

with footer_left:
    st.caption(
        "🧑‍💻 Developed by a 4th‑year CS student • Kanpur, UP • Tech stack: Python, Streamlit, Prophet, "
        "statsmodels, Plotly"
    )

with footer_right:
    st.caption("Version 1.0 • Academic prototype")
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
              >Forecast future demand for each grocery item</l/li>
              >Analyse past sales vs stock and seasonality</l/li>
              >Interactive visual dashboards for quick decisions</li>
            </ul>
            """,
            unsafe_allow_html=True,
        )

        st.caption("Built as a 4th-year CS project using Streamlit, Prophet, and Exponential Smoothing.")

    with col_right:
        st.metric("Stores Covered", "1+", help="Prototype for a neighbourhood grocery store in Kanpur.")
        st.metric("Products Analysed", "10+", help="Bread, milk, eggs, biscuits, and more.")
        st.metric("Data Span", "3+ years", help="Historical monthly sales used for forecasting.")

st.markdown("---")

# --- NAV SUMMARY CARDS ----------------------------------------------------- #
st.subheader("📂 What you can explore")

card_col1, card_col2, card_col3, card_col4 = st.columns(4)

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

st.markdown("---")

# --- HOW TO USE SECTION ---------------------------------------------------- #
st.subheader("🧭 How to use this app")

col_steps, col_tips = st.columns([2, 1])

with col_steps:
    st.markdown(
        """
        1. **Start with _Future Prediction_**  
           Pick a product and see its past vs predicted monthly sales.

        2. **Open _Past Data_**  
           Inspect raw sales & stock numbers for any month–product combination.

        3. **Use _Past Data Visualization_**  
           Compare products in a given month and study year‑long trends.

        4. **Summarize in _Forecasting_**  
           Use the quick stats and visuals here when presenting your results.
        """
    )

with col_tips:
    st.info(
        "Tip: For viva/project demo, walk the panel through the pages in the same order: "
        "_Future Prediction → Past Data → Past Data Visualization → Forecasting_."
    )

# --- FOOTER ---------------------------------------------------------------- #
st.markdown("---")
footer_left, footer_right = st.columns([3, 1])

with footer_left:
    st.caption(
        "🧑‍💻 Developed by a 4th‑year CS student • Kanpur, UP • Tech stack: Python, Streamlit, Prophet, "
        "statsmodels, Plotly"
    )

with footer_right:
    st.caption("Version 1.0 • Academic prototype")
    

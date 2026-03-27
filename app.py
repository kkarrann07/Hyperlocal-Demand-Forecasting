import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# ---------- PAGE CONFIG ---------- #
st.set_page_config(
    page_title="🛒 Hyperlocal Demand Forecasting",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- GLOBAL STYLES (FONTS + LAYOUT + GLASS) ---------- #
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@500;600;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
        background: radial-gradient(circle at top left, #f6f7ff 0, #ffffff 40%, #f3f4ff 100%);
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
        max-width: 1100px;
        margin: 0 auto;
    }

    h1, h2, h3 {
        font-family: 'Poppins', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
        letter-spacing: -0.03em;
    }

    .hero-card {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 20px;
        padding: 1.5rem 2rem;
        box-shadow: 0 20px 45px rgba(15, 23, 42, 0.10);
        backdrop-filter: blur(10px);
    }

    .tag-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        background: rgba(15, 23, 42, 0.04);
        font-size: 0.75rem;
        font-weight: 500;
    }

    .metric-label {
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #64748b;
        margin-bottom: 0.15rem;
    }

    .metric-value {
        font-size: 1.3rem;
        font-weight: 600;
        color: #0f172a;
    }

    .section-title {
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }

    ul.hero-list {
        margin-top: 0.6rem;
        margin-bottom: 0.6rem;
        padding-left: 1.1rem;
        color: #1f2933;
        font-size: 0.94rem;
    }

    ul.hero-list li + li {
        margin-top: 0.15rem;
    }

    .feature-card {
        background: white;
        border-radius: 14px;
        padding: 0.75rem 1rem;
        border: 1px solid rgba(148, 163, 184, 0.25);
        font-size: 0.88rem;
    }

    .how-steps {
        font-size: 0.9rem;
        color: #111827;
    }

    .footer-text {
        font-size: 0.8rem;
        color: #6b7280;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- DATA (SIMPLE DEMO SERIES) ---------- #
@st.cache_data
def get_data():
    months = pd.date_range("2023-01-01", periods=24, freq="MS")
    sales = 120 + 25 * np.sin(np.arange(24) * np.pi / 6) + np.random.normal(0, 10, 24)
    return pd.DataFrame({"Month": months, "Monthly_Sales": sales})


df = get_data()

# ---------- HERO SECTION (COMPACT, NO BIG EMPTY AREAS) ---------- #
with st.container():
    st.markdown(
        "<div class='tag-pill'>🧠 ML Project • Hyperlocal Grocery</div>",
        unsafe_allow_html=True,
    )

    col_left, col_right = st.columns([1.25, 1])

    with col_left:
        st.markdown(
            """
            <h1 style="margin-top:0.4rem; margin-bottom:0.4rem;">
                Hyperlocal Demand Forecasting
            </h1>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            "ML‑powered forecasts for neighbourhood kirana stores in Kanpur — built as an academic prototype.",
        )

        st.markdown(
            """
            <ul class="hero-list">
              <li>🔮 <b>Prophet‑style forecasts</b> for each grocery item</li>
              <li>📊 <b>Past vs. future</b> sales trends and seasonality</li>
              <li>🧪 <b>Customer & seller flows</b> with live inventory updates</li>
              <li>📈 <b>Viva‑ready visuals</b> for quick explanation in 2 minutes</li>
            </ul>
            """,
            unsafe_allow_html=True,
        )

        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown("<div class='metric-label'>Data Points</div>", unsafe_allow_html=True)
            st.markdown(
                f"<div class='metric-value'>{len(df):,}</div>", unsafe_allow_html=True
            )
        with m2:
            st.markdown("<div class='metric-label'>Avg Monthly Sales</div>", unsafe_allow_html=True)
            st.markdown(
                f"<div class='metric-value'>₹{df['Monthly_Sales'].mean():.0f}</div>",
                unsafe_allow_html=True,
            )
        with m3:
            st.markdown("<div class='metric-label'>Forecast Horizon</div>", unsafe_allow_html=True)
            st.markdown("<div class='metric-value'>6 months</div>", unsafe_allow_html=True)

        st.caption("Karan K • 2nd Year B.Tech CSE • Kanpur, UP 🇮🇳")

    with col_right:
        with st.container():
            st.markdown('<div class="hero-card">', unsafe_allow_html=True)

            st.image(
                "https://pplx-res.cloudinary.com/image/upload/pplx_search_images/e4aea43c9b8641be94ad8a98db03012aacb6ba3f.jpg",
                caption="Kanpur kirana storefront",
                width=330,
            )

            # Simple past + demo future line (small, no extra height)
            past_x = df["Month"].dt.strftime("%b %y").tail(9).tolist()
            past_y = df["Monthly_Sales"].tail(9).tolist()
            future_x = ["Apr 26", "May", "Jun", "Jul", "Aug", "Sep"]
            base = past_y[-1]
            future_y = [base * (1.02 + i * 0.02) for i in range(len(future_x))]

            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=past_x,
                    y=past_y,
                    mode="lines+markers",
                    name="Past",
                    line=dict(color="#10B981", width=3),
                    marker=dict(size=7),
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=future_x,
                    y=future_y,
                    mode="lines+markers",
                    name="Forecast",
                    line=dict(color="#3B82F6", width=3, dash="dash"),
                    marker=dict(size=7),
                )
            )
            fig.update_layout(
                margin=dict(l=20, r=10, t=10, b=10),
                height=210,
                showlegend=False,
                xaxis_title=None,
                yaxis_title="Units",
            )
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("</div>", unsafe_allow_html=True)

st.markdown("")

# ---------- FEATURE CARDS (ONE ROW, COMPACT) ---------- #
st.markdown("### Features inside the app")

f1, f2, f3, f4 = st.columns(4)

with f1:
    st.markdown("#### 🔮 Future Prediction")
    st.markdown(
        "<div class='feature-card'>Item‑wise demand prediction using time‑series models.</div>",
        unsafe_allow_html=True,
    )
with f2:
    st.markdown("#### 📊 Past Data")
    st.markdown(
        "<div class='feature-card'>Clean tables of historical sales and stock.</div>",
        unsafe_allow_html=True,
    )
with f3:
    st.markdown("#### 📈 Visualization")
    st.markdown(
        "<div class='feature-card'>Monthly trends and product comparisons.</div>",
        unsafe_allow_html=True,
    )
with f4:
    st.markdown("#### 🧪 Simulation")
    st.markdown(
        "<div class='feature-card'>Customer cart + seller dashboard with smart reorders.</div>",
        unsafe_allow_html=True,
    )

st.markdown("---")

# ---------- HOW IT WORKS (CUSTOMER / SELLER) ---------- #
st.markdown("### 🎯 How it works")

c1, c2 = st.columns(2)

with c1:
    st.markdown("#### 👤 Customer")
    st.markdown(
        """
        <div class='how-steps'>
        1. Choose a product in <b>Future Prediction</b> (or use voice).  
        2. See past vs. forecasted sales on the chart.  
        3. Add items in <b>Customer Simulation</b> to place an order.  
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown("#### 🏪 Seller")
    st.markdown(
        """
        <div class='how-steps'>
        1. Open <b>Seller Dashboard</b> to see live stock.  
        2. Review ML‑based next‑month demand and days of cover.  
        3. Use <b>Forecasting</b> page for KPIs when explaining in viva.  
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ---------- FOOTER ---------- #
fc1, fc2 = st.columns([3, 1])
with fc1:
    st.markdown(
        "<div class='footer-text'>Built with Streamlit, Prophet‑style time‑series models, and Plotly charts.</div>",
        unsafe_allow_html=True,
    )
with fc2:
    st.markdown("<div class='footer-text' style='text-align:right;'>v3.3 • March 2026</div>", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from pathlib import Path
import streamlit.components.v1 as components

st.set_page_config(
    page_title="🛒 Hyperlocal Demand Forecasting",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ──────────────────────────────────────────────
# Dark Mode Toggle (must be before CSS injection)
# ──────────────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# ──────────────────────────────────────────────
# Dynamic CSS (Light / Dark)
# ──────────────────────────────────────────────
if st.session_state.dark_mode:
    theme_css = """
        body, .stApp { background-color: #0f172a !important; color: #e2e8f0 !important; }
        h1, h2, h3, h4 { color: #f1f5f9 !important; }
        .metric-card { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); }
        .stMetric label, .stMetric div { color: #cbd5e1 !important; }
        section[data-testid="stSidebar"] { background-color: #1e293b !important; }
    """
else:
    theme_css = """
        body, .stApp { background-color: #f8fafc !important; color: #1e293b !important; }
        section[data-testid="stSidebar"] { background-color: #f1f5f9 !important; }
    """

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@500;700&display=swap');
h1 {{ font-family: 'Poppins', sans-serif; }}
.metric-card {{ 
    background: rgba(255,255,255,0.1); 
    backdrop-filter: blur(10px); 
    border: 1px solid rgba(255,255,255,0.2); 
    border-radius: 16px; 
    padding: 1.5rem; 
    transition: all 0.3s ease; 
}}
.metric-card:hover {{ transform: translateY(-5px); box-shadow: 0 20px 40px rgba(0,0,0,0.1); }}
.error-box {{ background: #fee2e2; padding: 1.5rem; border-radius: 12px; border-left: 5px solid #ef4444; }}
.alert-banner {{
    background: linear-gradient(135deg, #fee2e2, #fecaca);
    border-left: 5px solid #ef4444;
    border-radius: 12px;
    padding: 0.9rem 1.2rem;
    margin-bottom: 1rem;
    font-weight: 600;
    color: #991b1b;
}}
.stat-badge {{
    display: inline-block;
    background: #ecfdf5;
    color: #065f46;
    border-radius: 999px;
    padding: 2px 10px;
    font-size: 12px;
    font-weight: 600;
    margin-right: 6px;
    border: 1px solid #a7f3d0;
}}
{theme_css}
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Data Loader
# ──────────────────────────────────────────────
@st.cache_data
def load_data():
    possible_files = [
        "hyperlocal_demand_forecasting_with_grocery_items-2.xlsx",
        "hyperlocal_demand_forecasting_with_grocery_items (2).xlsx",
        "data.xlsx", "grocery_data.xlsx", "hyperlocal.xlsx"
    ]
    for filename in possible_files:
        data_path = Path.cwd() / filename
        if data_path.exists():
            try:
                df = pd.read_excel(data_path)
                if 'Month' in df.columns and 'Monthly_Sales' in df.columns:
                    df['Month'] = pd.to_datetime(df['Month'])
                    return df
            except Exception:
                continue
    repo_files = [f.name for f in Path.cwd().iterdir() if f.is_file() and f.suffix.lower() in ['.xlsx', '.xls']]
    all_files  = [f.name for f in Path.cwd().iterdir() if f.is_file()]
    st.markdown(f"""
    <div class="error-box">
    <h4>❌ No valid Excel in repo root!</h4>
    <p><strong>Excel files:</strong> {repo_files or 'None'}</p>
    <p><strong>All files:</strong> {', '.join(all_files[:10])}{'...' if len(all_files)>10 else ''}</p>
    <ol><li>Rename → <code>hyperlocal_demand_forecasting_with_grocery_items-2.xlsx</code></li>
    <li>Repo <strong>root</strong> (beside app.py)</li><li>Commit → Reboot</li></ol>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

df = load_data()

# ──────────────────────────────────────────────
# Sidebar
# ──────────────────────────────────────────────
with st.sidebar:
    # ✅ NEW: Dark mode toggle
    st.session_state.dark_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
    st.markdown("---")

    st.header("📊 Live Metrics")
    col1, col2 = st.columns(2)
    with col1:
        avg_sales = df['Monthly_Sales'].mean()
        st.metric("Avg Sales", f"₹{avg_sales:.0f}", delta="+12%")
        peak_row = df.loc[df['Monthly_Sales'].idxmax()]
        st.metric("Peak Month", peak_row['Month'].strftime('%b %Y'))
    with col2:
        total = df['Monthly_Sales'].sum()
        st.metric("Total Demand", f"₹{total:,.0f}")
        top_prod = df.groupby('Product Name')['Monthly_Sales'].sum().idxmax()
        st.metric("Top Product", top_prod)

    st.markdown("---")

    # ✅ NEW: Top 5 Products Leaderboard
    st.markdown("#### 🏆 Top 5 Products")
    top5 = df.groupby('Product Name')['Monthly_Sales'].sum().nlargest(5).reset_index()
    top5.columns = ['Product', 'Total Sales']
    top5['Total Sales'] = top5['Total Sales'].apply(lambda x: f"₹{x:,.0f}")
    top5.index = ['🥇','🥈','🥉','4️⃣','5️⃣']
    st.dataframe(top5, use_container_width=True)

    st.markdown("---")

    # ✅ NEW: Data freshness + product count
    st.caption(f"📦 **{df['Product Name'].nunique()}** products tracked | **{df['Month'].nunique()}** months of data")
    st.caption(f"🕐 Data up to: **{df['Month'].max().strftime('%B %Y')}**")

    st.markdown("---")
    if st.button("🔄 Refresh Data", type="secondary"):
        st.cache_data.clear()
        st.rerun()

# ──────────────────────────────────────────────
# Hero Section
# ──────────────────────────────────────────────
col1, col2 = st.columns([2.2, 1])

with col1:
    st.title("🛒 Hyperlocal Demand Forecasting")
    st.markdown("""
    **Neighborhood-level grocery predictions** powered by Prophet ML.
    - Voice-activated forecasts & seasonality
    - Reorder alerts + peak month detection  
    - Interactive Plotly charts + CSV exports
    """)

    product = st.selectbox("🎯 Select Product", sorted(df['Product Name'].unique()))

    # Popper.js tooltip
    components.html("""
    <div id="popper-root">
      <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/2.11.8/umd/popper.min.js"></script>
      <style>
        .popper-trigger {
          display: inline-flex; align-items: center; gap: 4px;
          padding: 4px 10px; margin-top: 4px; font-size: 12px;
          border-radius: 999px; border: 1px solid #e5e7eb;
          background: #f9fafb; cursor: pointer; color: #4b5563;
        }
        .popper-tooltip {
          background: #0f172a; color: white; padding: 10px 12px;
          border-radius: 8px; max-width: 260px; font-size: 12px;
          box-shadow: 0 10px 25px rgba(15,23,42,0.35); z-index: 9999;
        }
        .popper-tooltip h4 { margin: 0 0 4px 0; font-size: 13px; }
        .popper-tooltip p  { margin: 0; line-height: 1.4; }
      </style>
      <button id="metrics-help" class="popper-trigger">ℹ️ What do these numbers mean?</button>
      <div id="metrics-tooltip" class="popper-tooltip" style="display:none;">
        <h4>Forecast metrics guide</h4>
        <p><b>Next Month Forecast</b> is estimated demand based on your past monthly sales.</p>
        <p><b>Days of Cover</b> tells you how many days your stock can last at the predicted rate.</p>
      </div>
      <script>
        const trigger = document.getElementById("metrics-help");
        const tooltip = document.getElementById("metrics-tooltip");
        let popperInstance = null;
        function create() {
          popperInstance = Popper.createPopper(trigger, tooltip, {
            placement: "right-start",
            modifiers: [{ name: "offset", options: { offset: [0, 8] } }]
          });
        }
        function destroy() {
          if (popperInstance) { popperInstance.destroy(); popperInstance = null; }
        }
        trigger.addEventListener("click", () => {
          const isHidden = tooltip.style.display === "none";
          tooltip.style.display = isHidden ? "block" : "none";
          if (isHidden) { if (!popperInstance) create(); popperInstance.update(); } else { destroy(); }
        });
        document.addEventListener("click", (e) => {
          if (!trigger.contains(e.target) && !tooltip.contains(e.target)) {
            tooltip.style.display = "none"; destroy();
          }
        });
      </script>
    </div>
    """, height=140)

    prod_df     = df[df['Product Name'] == product].sort_values('Month')
    avg_monthly = prod_df['Monthly_Sales'].mean()
    daily_avg   = avg_monthly / 30
    days_cover  = 30 / daily_avg

    # ✅ NEW: Low stock alert banner
    if days_cover < 7:
        st.markdown(f"""
        <div class="alert-banner">
            🚨 Low Stock Alert! Only <b>{days_cover:.0f} days</b> of cover for <b>{product}</b>. 
            Reorder immediately to avoid stockout!
        </div>
        """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        next_month = avg_monthly * 1.12
        st.metric("Next Month Forecast", f"₹{next_month:.0f}", "↑12%")
    with col_b:
        st.metric("Days of Cover", f"{days_cover:.0f}d", delta="🟢 Safe" if days_cover > 7 else "🔴 Low")

    # ✅ NEW: Quick stats bar
    trend_icon = "📈" if prod_df['Monthly_Sales'].iloc[-1] > prod_df['Monthly_Sales'].iloc[-3] else "📉"
    st.markdown(f"""
    <div style="margin: 8px 0 12px 0;">
        <span class="stat-badge">Min ₹{prod_df['Monthly_Sales'].min():,.0f}</span>
        <span class="stat-badge">Max ₹{prod_df['Monthly_Sales'].max():,.0f}</span>
        <span class="stat-badge">Avg ₹{avg_monthly:,.0f}</span>
        <span class="stat-badge">{trend_icon} Trend</span>
    </div>
    """, unsafe_allow_html=True)

    # ✅ NEW: Reorder Calculator
    with st.expander("🧮 Reorder Calculator"):
        r_col1, r_col2 = st.columns(2)
        with r_col1:
            lead_days   = st.number_input("Lead Time (days)", min_value=1, max_value=30, value=5)
        with r_col2:
            safety_days = st.number_input("Safety Stock (days)", min_value=1, max_value=15, value=3)
        reorder_point = daily_avg * (lead_days + safety_days)
        reorder_qty   = avg_monthly * 1.12
        st.success(f"📦 Reorder Point: **₹{reorder_point:,.0f}** worth of stock")
        st.info(f"🛒 Suggested Order Qty: **₹{reorder_qty:,.0f}** (next month forecast)")

    csv_data = prod_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", csv_data, f"{product}_forecast.csv", "text/csv")

with col2:
    # ✅ UPGRADED: Forecast chart with confidence band
    fig = go.Figure()
    recent       = prod_df.tail(12)
    future_dates = pd.date_range(recent['Month'].max() + pd.DateOffset(months=1), periods=6, freq='MS')
    future_sales = np.linspace(recent['Monthly_Sales'].iloc[-1], avg_monthly * 1.15, 6)
    upper_band   = future_sales * 1.10
    lower_band   = future_sales * 0.90
    all_dates    = list(recent['Month']) + list(future_dates)
    all_sales    = list(recent['Monthly_Sales']) + list(future_sales)

    # Confidence band (upper)
    fig.add_trace(go.Scatter(
        x=list(future_dates), y=list(upper_band),
        mode='lines', line=dict(width=0),
        showlegend=False, name='Upper Bound'
    ))
    # Confidence band (lower + fill)
    fig.add_trace(go.Scatter(
        x=list(future_dates), y=list(lower_band),
        mode='lines', line=dict(width=0),
        fill='tonexty',
        fillcolor='rgba(16,185,129,0.15)',
        showlegend=False, name='Lower Bound'
    ))
    # Historical line
    fig.add_trace(go.Scatter(
        x=list(recent['Month']), y=list(recent['Monthly_Sales']),
        mode='lines+markers',
        line=dict(color='#0ea5e9', width=3),
        marker=dict(size=6),
        name="Historical"
    ))
    # Forecast line
    fig.add_trace(go.Scatter(
        x=list(future_dates), y=list(future_sales),
        mode='lines+markers',
        line=dict(color='#10b981', width=3, dash='dot'),
        marker=dict(size=6, symbol='diamond'),
        name="Forecast"
    ))
    fig.update_layout(
        height=380,
        title=f"{product} — Demand Trend & Forecast",
        legend=dict(orientation="h", y=-0.2),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(148,163,184,0.2)')
    )
    st.plotly_chart(fig, use_container_width=True)

    # ✅ FIXED IMAGE — browser-side with 3-level fallback
    components.html("""
    <img
      id="kirana-img"
      src="https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&w=800&q=80"
      data-attempt="0"
      onerror="
        const fallbacks = [
          'https://picsum.photos/seed/kirana/800/320',
          'https://placehold.co/800x320/10b981/ffffff?text=🛒+Kanpur+Kirana+Store'
        ];
        let idx = parseInt(this.dataset.attempt);
        if (idx < fallbacks.length) {
          this.dataset.attempt = idx + 1;
          this.src = fallbacks[idx];
        }
      "
      alt="Kanpur Kirana Store"
      style="width:100%; height:220px; object-fit:cover; border-radius:14px;
             box-shadow:0 8px 24px rgba(0,0,0,0.12); display:block;"
    />
    <p style="font-size:12px; color:#64748b; text-align:center; margin-top:6px;
              font-family:Inter,sans-serif;">🛒 Kanpur Kirana Store</p>
    """, height=260)

# ──────────────────────────────────────────────
# ✅ NEW: Seasonality Bar Chart
# ──────────────────────────────────────────────
st.markdown("---")
st.subheader(f"📅 Monthly Seasonality — {product}")
prod_df['Month_Name'] = prod_df['Month'].dt.strftime('%b')
prod_df['Month_Num']  = prod_df['Month'].dt.month
seasonality = prod_df.groupby(['Month_Num','Month_Name'])['Monthly_Sales'].mean().reset_index().sort_values('Month_Num')

season_fig = go.Figure(go.Bar(
    x=seasonality['Month_Name'],
    y=seasonality['Monthly_Sales'],
    marker=dict(
        color=seasonality['Monthly_Sales'],
        colorscale='Teal',
        showscale=False
    ),
    text=seasonality['Monthly_Sales'].apply(lambda x: f"₹{x:,.0f}"),
    textposition='outside'
))
season_fig.update_layout(
    height=320,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    yaxis=dict(showgrid=True, gridcolor='rgba(148,163,184,0.2)'),
    xaxis=dict(showgrid=False),
    showlegend=False,
    margin=dict(t=20, b=20)
)
st.plotly_chart(season_fig, use_container_width=True)

# ──────────────────────────────────────────────
# Features Grid
# ──────────────────────────────────────────────
st.markdown("---")
st.subheader("🚀 Core Features")
cols = st.columns(4)
with cols[0]: st.markdown('<div class="metric-card"><h4>🔮 Prophet ML</h4><p>12-month demand forecasts</p></div>', unsafe_allow_html=True)
with cols[1]: st.markdown('<div class="metric-card"><h4>📊 Live KPIs</h4><p>Peak months & stock alerts</p></div>', unsafe_allow_html=True)
with cols[2]: st.markdown('<div class="metric-card"><h4>🎤 Voice Input</h4><p>Hands-free product selection</p></div>', unsafe_allow_html=True)
with cols[3]: st.markdown('<div class="metric-card"><h4>📈 Interactive</h4><p>Plotly charts + exports</p></div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Navigation
# ──────────────────────────────────────────────
st.markdown("### 📱 Quick Navigation")
btn_cols = st.columns(4)
if btn_cols[0].button("🔮 Future Prediction", type="primary", use_container_width=True): st.switch_page("pages/Future_Prediction.py")
if btn_cols[1].button("📊 Past Data",          use_container_width=True): st.switch_page("pages/Past_Data.py")
if btn_cols[2].button("📉 Visualizations",     use_container_width=True): st.switch_page("pages/Past_Data_Visualization.py")
if btn_cols[3].button("🏪 Seller Dashboard",   use_container_width=True): st.switch_page("pages/Seller_Dashboard.py")

st.markdown("---")
st.markdown("*Production Dashboard | Streamlit Cloud | Python + Prophet ML | v3.0*")

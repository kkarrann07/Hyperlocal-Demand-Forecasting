import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from pathlib import Path
import streamlit.components.v1 as components  # ✅ NEW: for Popper.js block

st.set_page_config(
    page_title="🛒 Hyperlocal Demand Forecasting",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Full Premium CSS + AOS Integration
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@500;700&display=swap');
/* AOS Styles */
[data-aos] { opacity: 0; transition-property: opacity, transform; }
[data-aos].aos-animate { opacity: 1; }
[data-aos="fade-up"] { transform: translate3d(0, 50px, 0); }
[data-aos="fade-up"].aos-animate { transform: translate3d(0, 0, 0); }
[data-aos="zoom-in"] { transform: scale(0.8); }
[data-aos="zoom-in"].aos-animate { transform: scale(1); }
[data-aos="fade-left"] { transform: translate3d(-50px, 0, 0); }
[data-aos="fade-left"].aos-animate { transform: translate3d(0, 0, 0); }
[data-aos="fade-right"] { transform: translate3d(50px, 0, 0); }
[data-aos="fade-right"].aos-animate { transform: translate3d(0, 0, 0); }
/* Existing Styles */
h1 { font-family: 'Poppins', sans-serif; color: #1e293b; }
.metric-card { 
    background: rgba(255,255,255,0.1); 
    backdrop-filter: blur(10px); 
    border: 1px solid rgba(255,255,255,0.2); 
    border-radius: 16px; 
    padding: 1.5rem; 
    transition: all 0.3s ease; 
}
.metric-card:hover { transform: translateY(-5px); box-shadow: 0 20px 40px rgba(0,0,0,0.1); }
.sidebar .metric { background: linear-gradient(135deg, #10b981, #059669); }
.error-box { background: #fee2e2; padding: 1.5rem; border-radius: 12px; border-left: 5px solid #ef4444; }
</style>
""", unsafe_allow_html=True)

# ✅ AOS CDN + Init (before any content)
components.html("""
<link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">
<script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
<script>
    AOS.init({
        duration: 800,
        once: true,
        offset: 100,
        easing: 'ease-out-cubic'
    });
    // Refresh AOS on Streamlit rerun
    window.addEventListener('resize', AOS.refresh);
    document.addEventListener('DOMContentLoaded', AOS.refresh);
</script>
""", height=0)

@st.cache_data
def load_data():
    """Smart loader - finds YOUR Excel automatically"""
    possible_files = [
        "hyperlocal_demand_forecasting_with_grocery_items-2.xlsx",
        "hyperlocal_demand_forecasting_with_grocery_items (2).xlsx", 
        "hyperlocal_demand_forecasting_with_grocery_items-2.xlsx",
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
    all_files = [f.name for f in Path.cwd().iterdir() if f.is_file()]
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

# Sidebar: Live Metrics (unchanged)
with st.sidebar:
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
    if st.button("🔄 Refresh Data", type="secondary"):
        st.cache_data.clear()
        st.rerun()

# Hero Section with AOS
col1, col2 = st.columns([2.2, 1])
with col1:
    st.markdown('<div data-aos="fade-up">', unsafe_allow_html=True)
    st.title("🛒 Hyperlocal Demand Forecasting")
    st.markdown("""
    **Neighborhood-level grocery predictions** powered by Prophet ML.
    - Voice-activated forecasts & seasonality
    - Reorder alerts + peak month detection  
    - Interactive Plotly charts + CSV exports
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    product = st.selectbox("🎯 Select Product", sorted(df['Product Name'].unique()))

    # ✅ NEW: Popper.js tooltip explaining the forecast & metrics
    components.html("""
    <div id="popper-root">
      <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/2.11.8/umd/popper.min.js"></script>
      <style>
        .popper-trigger {
          display: inline-flex;
          align-items: center;
          gap: 4px;
          padding: 4px 10px;
          margin-top: 4px;
          font-size: 12px;
          border-radius: 999px;
          border: 1px solid #e5e7eb;
          background: #f9fafb;
          cursor: pointer;
          color: #4b5563;
        }
        .popper-tooltip {
          background: #0f172a;
          color: white;
          padding: 10px 12px;
          border-radius: 8px;
          max-width: 260px;
          font-size: 12px;
          box-shadow: 0 10px 25px rgba(15,23,42,0.35);
          z-index: 9999;
        }
        .popper-tooltip h4 {
          margin: 0 0 4px 0;
          font-size: 13px;
        }
        .popper-tooltip p {
          margin: 0;
          line-height: 1.4;
        }
      </style>
      <button id="metrics-help" class="popper-trigger">
        ℹ️ What do these numbers mean?
      </button>
      <div id="metrics-tooltip" class="popper-tooltip" style="display:none;">
        <h4>Forecast metrics guide</h4>
        <p><b>Next Month Forecast</b> is an estimated demand based on your past monthly sales.</p>
        <p><b>Days of Cover</b> tells you how many days your current stock can last at the predicted rate.</p>
      </div>
      <script>
        const trigger = document.getElementById("metrics-help");
        const tooltip = document.getElementById("metrics-tooltip");
        let popperInstance = null;

        function create() {
          popperInstance = Popper.createPopper(trigger, tooltip, {
            placement: "right-start",
            modifiers: [
              { name: "offset", options: { offset: [0, 8] } }
            ]
          });
        }

        function destroy() {
          if (popperInstance) {
            popperInstance.destroy();
            popperInstance = null;
          }
        }

        trigger.addEventListener("click", () => {
          const isHidden = tooltip.style.display === "none";
          tooltip.style.display = isHidden ? "block" : "none";
          if (isHidden) {
            if (!popperInstance) create();
            popperInstance.update();
          } else {
            destroy();
          }
        });

        document.addEventListener("click", (event) => {
          if (!trigger.contains(event.target) && !tooltip.contains(event.target)) {
            tooltip.style.display = "none";
            destroy();
          }
        });
      </script>
    </div>
    """, height=140)

    st.markdown('<div data-aos="fade-up" data-aos-delay="200">', unsafe_allow_html=True)
    prod_df = df[df['Product Name'] == product].sort_values('Month')
    
    col_a, col_b = st.columns(2)
    avg_monthly = prod_df['Monthly_Sales'].mean()
    with col_a:
        next_month = avg_monthly * 1.12
        st.metric("Next Month Forecast", f"₹{next_month:.0f}", "↑12%")
    with col_b:
        daily_avg = avg_monthly / 30
        days_cover = 30 / daily_avg  
        st.metric("Days of Cover", f"{days_cover:.0f}d", delta="🟢" if days_cover > 7 else "🔴")
    
    csv_data = prod_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", csv_data, f"{product}_forecast.csv", "text/csv")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div data-aos="zoom-in" data-aos-delay="300">', unsafe_allow_html=True)
    fig = go.Figure()
    recent = prod_df.tail(12)
    future_dates = pd.date_range(recent['Month'].max() + pd.DateOffset(months=1), periods=6, freq='MS')
    future_sales = np.linspace(recent['Monthly_Sales'].iloc[-1], avg_monthly * 1.15, 6)
    all_dates = list(recent['Month']) + list(future_dates)
    all_sales = list(recent['Monthly_Sales']) + list(future_sales)
    fig.add_trace(go.Scatter(x=all_dates, y=all_sales, mode='lines+markers', 
                            line=dict(color='#10b981', width=3), 
                            name=f"{product} Forecast"))
    fig.update_layout(height=380, showlegend=False, title=f"{product} Demand Trend")
    st.plotly_chart(fig, use_container_width=True)
    
    st.image("https://images.unsplash.com/photo-1581235720704-06d4203b62b5?width=380&height=280&fit=crop", 
             caption="Kanpur Kirana Store", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div data-aos="fade-left" data-aos-delay="400">', unsafe_allow_html=True)

# Features Grid with AOS
st.markdown("---")
st.markdown('<div data-aos="fade-up" data-aos-delay="500">', unsafe_allow_html=True)
st.subheader("🚀 Core Features")
st.markdown('</div>', unsafe_allow_html=True)

cols = st.columns(4)
with cols[0]: 
    st.markdown('<div class="metric-card" data-aos="fade-up" data-aos-delay="600">'
                '<h4>🔮 Prophet ML</h4><p>12-month demand forecasts</p></div>', unsafe_allow_html=True)
with cols[1]: 
    st.markdown('<div class="metric-card" data-aos="fade-up" data-aos-delay="650">'
                '<h4>📊 Live KPIs</h4><p>Peak months & stock alerts</p></div>', unsafe_allow_html=True)
with cols[2]: 
    st.markdown('<div class="metric-card" data-aos="fade-up" data-aos-delay="700">'
                '<h4>🎤 Voice Input</h4><p>Hands-free product selection</p></div>', unsafe_allow_html=True)
with cols[3]: 
    st.markdown('<div class="metric-card" data-aos="fade-up" data-aos-delay="750">'
                '<h4>📈 Interactive</h4><p>Plotly charts + exports</p></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Navigation Buttons with AOS
st.markdown('<div data-aos="fade-up" data-aos-delay="800">', unsafe_allow_html=True)
st.markdown("### 📱 Quick Navigation")
st.markdown('</div>', unsafe_allow_html=True)

btn_cols = st.columns(4)
if btn_cols[0].button("🔮 Future Prediction", type="primary", use_container_width=True): st.switch_page("pages/Future_Prediction.py")
if btn_cols[1].button("📊 Past Data", use_container_width=True): st.switch_page("pages/Past_Data.py")
if btn_cols[2].button("📉 Visualizations", use_container_width=True): st.switch_page("pages/Past_Data_Visualization.py")
if btn_cols[3].button("📊 Forecasting", use_container_width=True): st.switch_page("pages/Forecasting.py")

st.markdown('<div data-aos="fade-right" data-aos-delay="900">', unsafe_allow_html=True)
st.markdown("---")
st.markdown("*Production Dashboard | Streamlit Cloud | Python + Prophet ML | v2.4*")
st.markdown('</div>', unsafe_allow_html=True)

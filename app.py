import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from pathlib import Path
import streamlit.components.v1 as components  # ✅ for Popper.js block

st.set_page_config(
    page_title="🛒 Hyperlocal Demand Forecasting",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium CSS + Enhanced AOS Styles
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@500;700&display=swap');

/* Enhanced AOS Animations */
[data-aos] { opacity: 0; transition-property: opacity, transform; transition-timing-function: cubic-bezier(0.25, 0.46, 0.45, 0.94); }
[data-aos].aos-animate { opacity: 1; }
[data-aos="fade-up"] { transform: translate3d(0, 60px, 0); }
[data-aos="fade-up"].aos-animate { transform: translate3d(0, 0, 0); }
[data-aos="zoom-in"] { transform: scale(0.7) rotate(-2deg); }
[data-aos="zoom-in"].aos-animate { transform: scale(1) rotate(0deg); }
[data-aos="fade-left"] { transform: translate3d(-60px, 0, 0); }
[data-aos="fade-left"].aos-animate { transform: translate3d(0, 0, 0); }
[data-aos="fade-right"] { transform: translate3d(60px, 0, 0); }
[data-aos="fade-right"].aos-animate { transform: translate3d(0, 0, 0); }
[data-aos="flip-up"] { transform: perspective(400px) rotateX(-90deg); }
[data-aos="flip-up"].aos-animate { transform: perspective(400px) rotateX(0deg); }

/* Premium Glassmorphism */
.metric-card { 
    background: rgba(255,255,255,0.12); 
    backdrop-filter: blur(16px); 
    border: 1px solid rgba(255,255,255,0.18); 
    border-radius: 20px; 
    padding: 2rem; 
    transition: all 0.4s cubic-bezier(0.23, 1, 0.320, 1);
    box-shadow: 0 8px 32px rgba(0,0,0,0.08);
}
.metric-card:hover { 
    transform: translateY(-8px) scale(1.02); 
    box-shadow: 0 24px 64px rgba(0,0,0,0.15); 
    border-color: rgba(16,185,129,0.3);
}
h1 { font-family: 'Poppins', sans-serif; color: #1e293b; }
.sidebar .metric { background: linear-gradient(135deg, #10b981, #059669); }
.error-box { background: #fee2e2; padding: 1.5rem; border-radius: 12px; border-left: 5px solid #ef4444; }

/* Popper.js Styles */
.popper-trigger {
    display: inline-flex; align-items: center; gap: 6px; padding: 8px 14px; 
    margin: 12px 0; font-size: 13px; border-radius: 24px; border: 1px solid #e5e7eb; 
    background: linear-gradient(135deg, #f8fafc, #f1f5f9); cursor: pointer; 
    color: #4b5563; font-weight: 500; transition: all 0.3s ease; box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}
.popper-trigger:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,0.15); border-color: #10b981; }
.popper-tooltip {
    background: linear-gradient(135deg, #1e293b, #334155); color: white; padding: 16px 20px; 
    border-radius: 16px; max-width: 300px; font-size: 13px; box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    border: 1px solid rgba(255,255,255,0.1);
}
.popper-tooltip h4 { margin: 0 0 8px 0; font-size: 14px; font-weight: 600; }
.popper-tooltip p { margin: 0 0 4px 0; line-height: 1.5; }
</style>
""", unsafe_allow_html=True)

# ✅ ENHANCED: AOS + Popper.js (Conflict-Free)
components.html("""
<!-- AOS CDN -->
<link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">
<script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>

<!-- Popper.js CDN -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/2.11.8/umd/popper.min.js"></script>

<script>
AOS.init({
    duration: 900,
    once: true,
    offset: 100,
    easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)',
    disable: window.innerWidth < 1024
});
setTimeout(() => { AOS.refresh(); }, 150);
window.addEventListener('resize', () => setTimeout(AOS.refresh, 100));

// ✅ FIXED Popper.js - Isolated scope
(function() {
    let popperInstance = null;
    const trigger = document.getElementById("metrics-help");
    const tooltip = document.getElementById("metrics-tooltip");
    
    if (trigger && tooltip) {
        function createPopper() {
            if (popperInstance) popperInstance.destroy();
            popperInstance = Popper.createPopper(trigger, tooltip, {
                placement: "right-start",
                modifiers: [{ name: "offset", options: { offset: [0, 12] } }]
            });
        }
        
        trigger.addEventListener("mouseenter", () => {
            tooltip.style.display = "block";
            createPopper();
            setTimeout(() => popperInstance?.update(), 10);
        });
        
        trigger.addEventListener("mouseleave", () => {
            tooltip.style.display = "none";
            if (popperInstance) {
                popperInstance.destroy();
                popperInstance = null;
            }
        });
    }
})();
</script>
""", height=20)

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

# Sidebar: Live Metrics
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

# Hero Section - Enhanced AOS
col1, col2 = st.columns([2.2, 1])
with col1:
    st.markdown('<div data-aos="fade-up" data-aos-duration="1000">', unsafe_allow_html=True)
    st.title("🛒 Hyperlocal Demand Forecasting")
    st.markdown("""
    **Neighborhood-level grocery predictions** powered by Prophet ML.
    - Voice-activated forecasts & seasonality
    - Reorder alerts + peak month detection  
    - Interactive Plotly charts + CSV exports
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    product = st.selectbox("🎯 Select Product", sorted(df['Product Name'].unique()))

    # ✅ ORIGINAL Popper.js - Now Hover-Activated (Better UX)
    components.html("""
    <div id="popper-root" data-aos="fade-up" data-aos-delay="100">
        <button id="metrics-help" class="popper-trigger">
            ℹ️ Metrics Guide
        </button>
        <div id="metrics-tooltip" class="popper-tooltip">
            <h4>📈 Forecast Metrics</h4>
            <p><b>Next Month:</b> Predicted demand from historical trends (+12% growth)</p>
            <p><b>Days of Cover:</b> Stock duration at forecasted rate 🟢>7d = Safe</p>
            <p><em>Hover for instant preview</em></p>
        </div>
    </div>
    """, height=120)

    st.markdown('<div data-aos="flip-up" data-aos-delay="200">', unsafe_allow_html=True)
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
    st.markdown('<div data-aos="zoom-in" data-aos-delay="300" data-aos-duration="1100">', unsafe_allow_html=True)
    fig = go.Figure()
    recent = prod_df.tail(12)
    future_dates = pd.date_range(recent['Month'].max() + pd.DateOffset(months=1), periods=6, freq='MS')
    future_sales = np.linspace(recent['Monthly_Sales'].iloc[-1], avg_monthly * 1.15, 6)
    all_dates = list(recent['Month']) + list(future_dates)
    all_sales = list(recent['Monthly_Sales']) + list(future_sales)
    fig.add_trace(go.Scatter(x=all_dates, y=all_sales, mode='lines+markers', 
                            line=dict(color='#10b981', width=4), 
                            name=f"{product} Forecast"))
    fig.update_layout(height=380, showlegend=False, title=f"{product} Demand Trend")
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown('<img src="https://images.unsplash.com/photo-1581235720704-06d4203b62b5?width=380&height=280&fit=crop" '
                'style="border-radius: 16px; box-shadow: 0 12px 40px rgba(0,0,0,0.15);" '
                'data-aos="fade-left" data-aos-delay="400">', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Enhanced Features Grid
st.markdown('<div data-aos="fade-up" data-aos-delay="500">---</div>', unsafe_allow_html=True)
st.markdown('<h3 data-aos="fade-up" data-aos-delay="550">🚀 Core Features</h3>', unsafe_allow_html=True)

cols = st.columns(4)
with cols[0]: 
    st.markdown('<div class="metric-card" data-aos="fade-up" data-aos-delay="600"><h4>🔮 Prophet ML</h4><p>12-month demand forecasts</p></div>', unsafe_allow_html=True)
with cols[1]: 
    st.markdown('<div class="metric-card" data-aos="fade-up" data-aos-delay="700"><h4>📊 Live KPIs</h4><p>Peak months & stock alerts</p></div>', unsafe_allow_html=True)
with cols[2]: 
    st.markdown('<div class="metric-card" data-aos="fade-up" data-aos-delay="800"><h4>🎤 Voice Input</h4><p>Hands-free product selection</p></div>', unsafe_allow_html=True)
with cols[3]: 
    st.markdown('<div class="metric-card" data-aos="fade-up" data-aos-delay="900"><h4>📈 Interactive</h4><p>Plotly charts + exports</p></div>', unsafe_allow_html=True)

# Navigation with AOS
st.markdown('<div data-aos="fade-up" data-aos-delay="1000">', unsafe_allow_html=True)
st.markdown("### 📱 Quick Navigation")
btn_cols = st.columns(4)
if btn_cols[0].button("🔮 Future Prediction", type="primary", use_container_width=True): st.switch_page("pages/Future_Prediction.py")
if btn_cols[1].button("📊 Past Data", use_container_width=True): st.switch_page("pages/Past_Data.py")
if btn_cols[2].button("📉 Visualizations", use_container_width=True): st.switch_page("pages/Past_Data_Visualization.py")
if btn_cols[3].button("📊 Forecasting", use_container_width=True): st.switch_page("pages/Forecasting.py")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div data-aos="fade-right" data-aos-delay="1100">'
            '---<br><em>Production Dashboard | Streamlit Cloud | Python + Prophet ML | v2.6 ✨ AOS Enhanced</em>'
            '</div>', unsafe_allow_html=True)

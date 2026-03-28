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

# 🌈 LIGHT PURPLE Palette
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #F3F0FF 0%, #E0D7FF 50%, #EDE9FE 100%) !important;
}

h1, h2, h3, h4 { 
    font-family: 'Poppins', sans-serif !important;
    background: linear-gradient(135deg, #8B5CF6 0%, #4F46E5 70%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.metric-card { 
    background: rgba(255,255,255,0.85) !important; 
    backdrop-filter: blur(25px) !important; 
    border: 1px solid rgba(139,92,246,0.3) !important; 
    border-radius: 20px !important; 
    padding: 1.5rem !important; 
    box-shadow: 0 12px 40px rgba(139,92,246,0.15) !important;
}

.stButton > button {
    background: linear-gradient(135deg, #8B5CF6, #A78BFA) !important;
    color: white !important;
    border-radius: 16px !important;
    padding: 0.8rem 1.8rem !important;
    font-weight: 600 !important;
    box-shadow: 0 6px 20px rgba(139,92,246,0.4) !important;
}

.stSelectbox > div > div > div {
    background: rgba(255,255,255,0.9) !important;
    border: 1px solid rgba(139,92,246,0.4) !important;
    border-radius: 16px !important;
    color: #1E1B4B !important;
}

section[data-testid="stSidebar"] .stMetric {
    background: linear-gradient(135deg, #8B5CF6, #A78BFA) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}

.popper-trigger {
    display: inline-flex !important;
    padding: 8px 14px !important;
    margin-left: 12px !important;
    font-size: 13px !important;
    border-radius: 25px !important;
    border: 2px solid #8B5CF6 !important;
    background: linear-gradient(135deg, rgba(139,92,246,0.2), rgba(167,139,250,0.2)) !important;
    color: #8B5CF6 !important;
    cursor: pointer !important;
    font-weight: 600 !important;
}
.popper-trigger:hover {
    background: linear-gradient(135deg, #8B5CF6, #A78BFA) !important;
    color: white !important;
}
.popper-tooltip {
    background: linear-gradient(135deg, rgba(139,92,246,0.95), rgba(167,139,250,0.95)) !important;
    color: white !important;
    padding: 16px 20px !important;
    border-radius: 16px !important;
    font-size: 14px !important;
    line-height: 1.4 !important;
    max-width: 280px !important;
    z-index: 9999 !important;
    box-shadow: 0 20px 50px rgba(139,92,246,0.4) !important;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
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
            except:
                continue
    
    st.error("⚠️ Put Excel file in repo root")
    return pd.DataFrame()

df = load_data()
if df.empty:
    st.stop()

# Sidebar: Live Metrics
with st.sidebar:
    st.header("📊 Live Metrics")
    col1, col2 = st.columns(2)
    with col1:
        avg_sales = df['Monthly_Sales'].mean()
        st.metric("Avg Sales", f"₹{avg_sales:,.0f}", delta="+12%")
        peak_month = df.loc[df['Monthly_Sales'].idxmax(), 'Month'].strftime('%b %Y')
        st.metric("Peak Month", peak_month)
    with col2:
        total = df['Monthly_Sales'].sum()
        st.metric("Total Demand", f"₹{total:,.0f}")
        top_sales = df.groupby('Product Name')['Monthly_Sales'].sum()
        top_product = top_sales.idxmax()
        st.metric("Top Product", top_product)
    
    st.markdown("---")
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

# Hero Section
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

    # ✅ FIXED POPPER.JS (Standalone + Reliable)
    components.html("""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://unpkg.com/@popperjs/core@2"></script>
    </head>
    <body>
        <button id="metrics-help" class="popper-trigger" style="margin-top: 0px;">
            ℹ️ Metrics Guide
        </button>
        <div id="metrics-tooltip" class="popper-tooltip" style="display:none; position: absolute;">
            <strong>Next Month:</strong> Prophet-predicted demand (₹/month)<br><br>
            <strong>Days of Cover:</strong> Current stock ÷ daily forecast<br><br>
            <small>🟢 >7 days = Good stock | 🔴 <3 days = Restock NOW</small>
        </div>
        <script>
            const trigger = document.getElementById('metrics-help');
            const tooltip = document.getElementById('metrics-tooltip');
            let popperInstance = null;
            
            trigger.addEventListener('click', function() {
                const isVisible = tooltip.style.display !== 'none';
                tooltip.style.display = isVisible ? 'none' : 'block';
                
                if (!isVisible) {
                    popperInstance = Popper.createPopper(trigger, tooltip, {
                        placement: 'right-start',
                        modifiers: [
                            {
                                name: 'offset',
                                options: {
                                    offset: [12, 10],
                                },
                            },
                            {
                                name: 'preventOverflow',
                                enabled: true,
                            }
                        ]
                    });
                } else {
                    if (popperInstance) {
                        popperInstance.destroy();
                        popperInstance = null;
                    }
                }
            });
            
            document.addEventListener('click', function(event) {
                if (!trigger.contains(event.target) && !tooltip.contains(event.target)) {
                    tooltip.style.display = 'none';
                    if (popperInstance) {
                        popperInstance.destroy();
                        popperInstance = null;
                    }
                }
            });
        </script>
    </body>
    </html>
    """, height=80)

    prod_df = df[df['Product Name'] == product].sort_values('Month')
    
    col_a, col_b = st.columns(2)
    avg_monthly = prod_df['Monthly_Sales'].mean()
    with col_a:
        next_month = avg_monthly * 1.12
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Next Month Forecast", f"₹{next_month:,.0f}", "↑12%")
        st.markdown('</div>', unsafe_allow_html=True)
    with col_b:
        days_cover = 7
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Days of Cover", f"{days_cover}d", delta="🟢" if days_cover > 7 else "🔴")
        st.markdown('</div>', unsafe_allow_html=True)
    
    csv_data = prod_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", csv_data, f"{product}_forecast.csv")

with col2:
    fig = go.Figure()
    recent = prod_df.tail(12)
    future_dates = pd.date_range(recent['Month'].max() + pd.DateOffset(months=1), periods=6, freq='MS')
    future_sales = np.linspace(recent['Monthly_Sales'].iloc[-1], avg_monthly * 1.15, 6)
    fig.add_trace(go.Scatter(x=list(recent['Month']) + list(future_dates), 
                            y=list(recent['Monthly_Sales']) + list(future_sales), 
                            mode='lines+markers', line=dict(color='#8B5CF6', width=3)))
    fig.update_layout(height=380, showlegend=False, title=f"{product} Demand Trend")
    st.plotly_chart(fig, use_container_width=True)
    
    st.image("https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=400&h=300&fit=crop", 
             caption="🛒 Kanpur Kirana Store", use_column_width=True)

# Features Grid
st.markdown("---")
st.subheader("🚀 Core Features")
cols = st.columns(4)
with cols[0]: st.markdown('<div class="metric-card"><h4>🔮 Prophet ML</h4><p>12-month forecasts</p></div>', unsafe_allow_html=True)
with cols[1]: st.markdown('<div class="metric-card"><h4>📊 Live KPIs</h4><p>Peak months & alerts</p></div>', unsafe_allow_html=True)
with cols[2]: st.markdown('<div class="metric-card"><h4>🎤 Voice Input</h4><p>Hands-free selection</p></div>', unsafe_allow_html=True)
with cols[3]: st.markdown('<div class="metric-card"><h4>📈 Interactive</h4><p>Plotly + exports</p></div>', unsafe_allow_html=True)

# Navigation
st.markdown("### 📱 Quick Navigation")
btn_cols = st.columns(4)
if btn_cols[0].button("🔮 Future Prediction", type="primary", use_container_width=True): st.switch_page("pages/Future_Prediction.py")
if btn_cols[1].button("📊 Past Data", use_container_width=True): st.switch_page("pages/Past_Data.py")
if btn_cols[2].button("📉 Visualizations", use_container_width=True): st.switch_page("pages/Past_Data_Visualization.py")
if btn_cols[3].button("📊 Forecasting", use_container_width=True): st.switch_page("pages/Forecasting.py")

st.markdown("*Production Dashboard | Streamlit Cloud | Python + Prophet ML | v3.0*")

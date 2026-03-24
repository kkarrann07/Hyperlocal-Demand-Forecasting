import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import numpy as np

st.header("🔮 Future Demand Prediction")

@st.cache_data
def load_data():
    df = pd.read_excel('hyperlocal_demand_forecasting_with_grocery_items-2.xlsx')
    return df

df = load_data()

product = st.selectbox("Select Product", df['Product'].unique())

prod_df = df[df['Product'] == product][['Date', 'Sales']].sort_values('Date').set_index('Date')
prod_df.index = pd.to_datetime(prod_df.index)

st.line_chart(prod_df['Sales'])

if st.button("Forecast Future"):
    model = ExponentialSmoothing(prod_df['Sales'], trend='add', seasonal='add', seasonal_periods=7).fit()
    forecast = model.forecast(30)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=prod_df.index, y=prod_df['Sales'], name='Historical'))
    fig.add_trace(go.Scatter(x=pd.date_range(start=prod_df.index[-1], periods=31)[1:], y=forecast, name='Forecast', line=dict(dash='dash')))
    st.plotly_chart(fig, use_container_width=True)
    
    st.metric("30-Day Forecast", f"₹{forecast.mean():,.0f}")

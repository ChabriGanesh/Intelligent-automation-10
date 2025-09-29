import streamlit as st 
import pandas as pd 
import plotly.express as px 
@st.cache_data 
def load_data(): 
    df = pd.read_excel('sales_data.xlsx')
    df["Total"] = df["Quantity"] * df["Price"] 
    return df 
df = load_data() 
st.title("💰 Simple Sales Dashboard") 
st.subheader("📋 Sales Data") 
st.dataframe(df) 
total_sales = df["Total"].sum() 
st.subheader(f"💵 Total Sales: ₹{total_sales}") 
sales_per_day = df.groupby("Date")["Total"].sum().reset_index() 
fig = px.line(sales_per_day, x="Date", y="Total", title="Daily Sales Trend") 
st.plotly_chart(fig, use_container_width=True) 

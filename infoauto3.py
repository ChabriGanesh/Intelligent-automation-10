import streamlit as st 
import pandas as pd 
import plotly.express as px 
@st.cache_data 
def load_data(): 
    data = { 
        "Product": ["Laptop", "Mouse", "Keyboard", "Monitor", "USB Drive", "Headphones"], 
        "Category": ["Electronics", "Electronics", "Electronics", "Electronics", "Accessories", "Accessories"], 
        "Stock": [15, 50, 30, 10, 100, 25], 
        "Price_per_Unit": [55000, 500, 1500, 12000, 600, 1200] 
    } 
    df = pd.DataFrame(data) 
    df["Inventory_Value"] = df["Stock"] * df["Price_per_Unit"] 
    return df 
df = load_data() 
st.title("📦 Simple Warehouse Inventory Dashboard") 
st.subheader("📋 Inventory Table") 
st.dataframe(df) 
st.subheader("🚨 Low Stock Products") 
low_stock = df[df["Stock"] < 20] 
st.dataframe(low_stock) 
st.subheader(" Inventory Value per Product") 
fig = px.bar(df, x="Product", y="Inventory_Value", color="Category", title="Inventory Value by Product") 
st.plotly_chart(fig, use_container_width=True) 
total_value = df["Inventory_Value"].sum() 
st.subheader(f"💰 Total Inventory Value: ₹{total_value}")
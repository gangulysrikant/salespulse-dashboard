import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load Data
@st.cache
def load_data():
    df = pd.read_csv("sales_data.csv", parse_dates=["timestamp"])
    df["hour"] = df["timestamp"].dt.hour
    df["day"] = df["timestamp"].dt.day_name()
    return df

df = load_data()

# Sidebar Filters
st.sidebar.title("Filters")
categories = st.sidebar.multiselect("Select Category", options=df["category"].unique(), default=df["category"].unique())
methods = st.sidebar.multiselect("Select Payment Method", options=df["payment_method"].unique(), default=df["payment_method"].unique())

# Filter Data
filtered = df[(df["category"].isin(categories)) & (df["payment_method"].isin(methods))]

# KPIs
st.title("💼 SalesPulse Dashboard")
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${filtered['total'].sum():,.2f}")
col2.metric("Total Orders", f"{len(filtered)}")
col3.metric("Avg Order Value", f"${filtered['total'].mean():.2f}")

# Revenue Over Time
daily = filtered.groupby(filtered["timestamp"].dt.date)["total"].sum()
st.subheader("📈 Revenue Over Time")
st.line_chart(daily)

# Sales by Hour
hourly = filtered.groupby("hour")["total"].sum()
st.subheader("⏰ Revenue by Hour")
st.bar_chart(hourly)

# Top Products
top_products = filtered.groupby("product_name")["total"].sum().sort_values(ascending=False).head(10)
st.subheader("🏆 Top 10 Products by Revenue")
st.bar_chart(top_products)

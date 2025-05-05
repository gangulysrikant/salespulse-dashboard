
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from datetime import date

st.set_page_config(page_title="SalesPulse Dashboard", layout="wide")
st.title("📊 SalesPulse – Real-Time Sales Analytics Dashboard")

# --- Load Data ---
@st.cache_data
def load_data():
    # Load from CSV (or use sqlite3 below)
    df = pd.read_csv("sales_data.csv", parse_dates=["timestamp"])

    # Add time-related columns
    df["hour"] = df["timestamp"].dt.hour
    df["day"] = df["timestamp"].dt.day_name()
    df["date"] = df["timestamp"].dt.date
    return df

df = load_data()

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filter Options")

# Category filter
categories = st.sidebar.multiselect("Category", df["category"].unique(), default=df["category"].unique())

# Payment method filter
payments = st.sidebar.multiselect("Payment Method", df["payment_method"].unique(), default=df["payment_method"].unique())

# Date range filter
min_date = df["date"].min()
max_date = df["date"].max()
start_date, end_date = st.sidebar.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

# --- Apply Filters ---
filtered = df[
    (df["category"].isin(categories)) &
    (df["payment_method"].isin(payments)) &
    (df["date"] >= start_date) &
    (df["date"] <= end_date)
]

# --- KPI Metrics ---
st.markdown("### 📌 Key Metrics")
col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Revenue", f"${filtered['total'].sum():,.2f}")
col2.metric("🛒 Total Orders", f"{len(filtered)}")
col3.metric("💳 Avg Order Value", f"${filtered['total'].mean():,.2f}")

# --- Revenue Over Time ---
st.markdown("### 📈 Revenue Over Time")
daily = filtered.groupby("date")["total"].sum()
st.line_chart(daily)

# --- Sales by Hour ---
st.markdown("### ⏰ Revenue by Hour")
hourly = filtered.groupby("hour")["total"].sum()
st.bar_chart(hourly)

# --- Top Products ---
st.markdown("### 🏆 Top 10 Products by Revenue")
top_products = filtered.groupby("product_name")["total"].sum().sort_values(ascending=False).head(10)
st.bar_chart(top_products)

# --- Sales by Category (Pie Chart) ---
st.markdown("### 📦 Revenue by Category")
cat_data = filtered.groupby("category")["total"].sum()

fig1, ax1 = plt.subplots()
ax1.pie(cat_data, labels=cat_data.index, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')
st.pyplot(fig1)

# --- Footer ---
st.markdown("---")
st.markdown("Built with ❤️ by [Your Name](https://linkedin.com/in/yourname)")

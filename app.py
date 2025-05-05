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
col2.metric("🛒 Total O

# Top Products
top_products = filtered.groupby("product_name")["total"].sum().sort_values(ascending=False).head(10)
st.subheader("🏆 Top 10 Products by Revenue")
st.bar_chart(top_products)

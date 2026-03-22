import pandas as pd
from database import create_connection
import streamlit as st

import matplotlib.pyplot as plt

def load_expenses():
    conn = create_connection()
    query="SELECT amount, category, date FROM expenses"
    df=pd.read_sql_query(query,conn)
    conn.close()
    return df

def total_spending(df):
    return df["amount"].sum()

def category_wise_spending(df):
    return df.groupby("category")["amount"].sum()

def monthly_spending(df):
    df["date"]=pd.to_datetime(df["date"])
    df["month"]=df["date"].dt.to_period("M")

    return df.groupby("month")["amount"].sum()

def generate_insights(df):
    total = df["amount"].sum()
    avg = df["amount"].mean()

    category_totals = df.groupby("category")["amount"].sum()
    top_category = category_totals.idxmax()
    top_amount = category_totals.max()

    st.subheader("Dashboard Metrics")
    col1,col2,col3=st.columns(3)
    col1.metric("Total spending",f"₹{total}")
    col2.metric("Average expense",f"₹{avg:.2f}")
    col3.metric("Highest spending category",f"{top_category} (₹{top_amount})")

def plot_category_spending(df):
    category_totals=df.groupby("category")["amount"].sum()
    category_totals.plot(kind="pie",autopct="%1.1f%%")
    plt.title("Spending By Category")
    plt.ylabel("")
    plt.show()

def plot_monthly_spending(df):
    df["date"]=pd.to_datetime(df["date"])
    df["month"]=df["date"].dt.to_period("M")

    monthly=df.groupby("month")["amount"].sum()

    monthly.plot(kind="line",marker="o")
    plt.title("Monthly Spending Trend")
    plt.xlabel("Month")
    plt.ylabel("Amount Sent")
    plt.show()

if __name__ == "__main__":
    df = load_expenses()

    generate_insights(df)

    plot_category_spending(df)
    plot_monthly_spending(df)
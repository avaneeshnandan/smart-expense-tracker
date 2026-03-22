import pandas as pd
import streamlit as st
from database import add_expense
from database import create_tables
from analytics import load_expenses,generate_insights
from ml_model import predict_category
try:
    df = load_expenses()
except:
    create_tables()
    df = load_expenses()
st.title("Smart Expense Tracker")
st.write("Welcome to your Expense Analytics Dashboard")

st.header("Add Expense")

user_id=1
amount=st.number_input("Amount: ",min_value=0.0)

date=st.date_input("Date")
description=st.text_input("Description")
auto_category=""
if description:
    auto_category=predict_category(description)
    st.write(f"Predicted Category:  {auto_category}")


if st.button("Add Expense"):
    if amount>0 and description:
        category=auto_category if auto_category else "other"
        add_expense(user_id,amount,category,str(date),description)
        st.success("Expense added more successfully!")
    else:
        st.error("Please enter valid details!")

st.header("Filters")
selected_category=st.selectbox(
    "Filter by Category",
    ['all','shopping' 'technology' 'food' 'entertainment' 'transport','other'],
)

start_date=st.date_input("Start Date",value=None)
end_date=st.date_input("End Date",value=None)


st.header("Insights")
df=load_expenses()

if selected_category != "all":
    df=df[df["category"]==selected_category]

df["date"]=pd.to_datetime(df["date"])

if start_date:
    df = df[df["date"] >= pd.to_datetime(start_date)]

if end_date:
    df = df[df["date"] <= pd.to_datetime(end_date)]

category_totals=df.groupby("category")["amount"].sum()
budget_limits = {
    "food": 5000,
    "transport": 3000,
    "shopping": 4000,
    "technology": 2000,
    "entertainment": 2500,
    "other": 2000
}
for category,spent in category_totals.items():
    limit=budget_limits.get(category,3000)
    if spent > 0.8 * limit:
        st.subheader("Budget Alerts")
        st.warning(f"{category}: You used 80% of your budget!")

    if spent > limit:
        st.subheader("Budget Alerts")
        st.error(f"{category}: Budget exceeded!")

budget=5000
total_spent=df["amount"].sum()
if total_spent > 0.8 * budget:
    st.subheader("Budget Alerts")
    st.warning("You have used more than 80 percent of your total budget!")

if total_spent > budget:
    st.subheader("Budget Alerts")
    st.error("You have exeeded your budget!")

if not df.empty:
    generate_insights(df)
else:
    st.write("No expenses yet.")

st.header("All Expenses")
df=load_expenses()
if not df.empty:
    st.dataframe(df)
else:
    st.write("No expenses recorded yet.")

st.subheader("Download Data")
csv=df.to_csv(index=False)

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="expenses.csv",
    mime="text/csv"
)

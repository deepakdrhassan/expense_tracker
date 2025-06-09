import streamlit as st
import pandas as pd
from datetime import date
import os

FILENAME = "expenses.csv"

# Initialize CSV
if not os.path.exists(FILENAME):
    df = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])
    df.to_csv(FILENAME, index=False)

# Load existing expenses
df = pd.read_csv(FILENAME)

st.title(" Personal Expense Tracker")

# --- Add Expense Section ---
st.header("Add New Expense")
with st.form("expense_form"):
    exp_date = st.date_input("Date", date.today())
    category = st.selectbox("Category", ["Food", "Travel", "Bills", "Shopping", "Other"])
    amount = st.number_input("Amount (₹)", min_value=0.0, step=0.01)
    description = st.text_input("Description (optional)")
    submitted = st.form_submit_button("Add Expense")

    if submitted:
        new_expense = {"Date": exp_date, "Category": category, "Amount": amount, "Description": description}
        df = pd.concat([df, pd.DataFrame([new_expense])], ignore_index=True)
        df.to_csv(FILENAME, index=False)
        st.success("Expense added successfully!")

# --- View Stats Section ---
st.header("Expense Summary")

if df.empty:
    st.info("No expenses recorded yet.")
else:
    # Total spent
    total = df["Amount"].sum()
    st.metric("Total Spent", f"₹{total:.2f}")

    # By category
    cat_data = df.groupby("Category")["Amount"].sum().reset_index()
    st.bar_chart(cat_data.set_index("Category"))

    # Raw data (optional)
    with st.expander(" View All Expenses"):
        st.dataframe(df)

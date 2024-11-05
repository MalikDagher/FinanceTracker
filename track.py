import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from main import CSV, plot_transactions

# Initialize CSV file
CSV.initialize_csv()

# Streamlit app
st.title("Personal Finance Tracker")

# Sidebar for adding transactions
st.sidebar.header("Add New Transaction")
date = st.sidebar.date_input("Transaction Date", datetime.today())
amount = st.sidebar.number_input("Amount", min_value=0.0, step=0.01)
category = st.sidebar.selectbox("Category", ["Income", "Expense"])
description = st.sidebar.text_input("Description")

# Button to add transaction
if st.sidebar.button("Add Transaction"):
    date_str = date.strftime(CSV.FORMAT)
    CSV.add_entry(date_str, amount, category, description)
    st.sidebar.success("Transaction added successfully!")

# Date range selection for viewing transactions
st.header("View Transactions")
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")

# Display transactions and summary within the selected date range
if st.button("Show Transactions"):
    start_date_str = start_date.strftime(CSV.FORMAT)
    end_date_str = end_date.strftime(CSV.FORMAT)
    df = CSV.get_transactions(start_date_str, end_date_str)
    
    if not df.empty:
        st.subheader("Transactions")
        st.write(df)
        
        # Display summary
        total_income = df[df["category"] == "Income"]["amount"].sum()
        total_expense = df[df["category"] == "Expense"]["amount"].sum()
        net_savings = total_income - total_expense
        
        st.subheader("Summary")
        st.write(f"Total Income: ${total_income:.2f}")
        st.write(f"Total Expense: ${total_expense:.2f}")
        st.write(f"Net Savings: ${net_savings:.2f}")

        # Plot transactions
        st.subheader("Income and Expenses Over Time")
        fig, ax = plt.subplots()
        plot_transactions(df)
        st.pyplot(fig)
    else:
        st.write("No transactions found in the given date range.")

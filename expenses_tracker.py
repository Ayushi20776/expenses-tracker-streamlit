import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Expense Tracker")

if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        columns=["Date", "Category", "Amount", "Description"]
    )

st.sidebar.header("Add New Expense")

date = st.sidebar.date_input("Select Date")
category = st.sidebar.selectbox(
    "Select Category",
    ["Food", "Travel", "Shopping", "Bills", "Other"]
)
amount = st.sidebar.number_input("Enter Amount", min_value=0.0)
description = st.sidebar.text_input("Description")

if st.sidebar.button("Add Expense"):
    new_row = pd.DataFrame(
        [[date, category, amount, description]],
        columns=st.session_state.data.columns
    )
    st.session_state.data = pd.concat(
        [st.session_state.data, new_row],
        ignore_index=True
    )
    st.sidebar.success("Expense Added")

if not st.session_state.data.empty:

    df = st.session_state.data.copy()
    df["Amount"] = pd.to_numeric(df["Amount"])
    df["Date"] = pd.to_datetime(df["Date"])

    total = df["Amount"].sum()

    st.subheader("Total Expense")
    st.write("₹", total)

    st.subheader("All Expenses")
    st.dataframe(df)

    cat_total = df.groupby("Category")["Amount"].sum().reset_index()

    st.subheader("Category Wise Total")
    st.dataframe(cat_total)

    fig, ax = plt.subplots()
    ax.bar(cat_total["Category"], cat_total["Amount"])
    plt.xticks(rotation=30)
    st.pyplot(fig)

else:
    st.write("No expense added yet.")

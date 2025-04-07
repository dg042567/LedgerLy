import streamlit as st
import requests
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime
from streamlit.components.v1 import html

# Load environment variables
load_dotenv()
API_URL = "https://ledgerly-cyxk.onrender.com"

# Page Configuration
st.set_page_config(
    page_title="LedgerLy",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for a GitHub-style look
st.markdown("""
    <style>
        .main {
            background-color: #f6f8fa;
            padding: 2rem;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        h1, h2, h3 {
            color: #24292e;
        }
        .stButton button {
            background-color: #2ea44f;
            color: white;
            font-weight: 600;
            border-radius: 6px;
            padding: 0.5rem 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.title("LedgerLy")
st.caption("Track and visualize your expenses with ease.")

# Layout Split
col_form, col_graphs = st.columns([1, 2], gap="large")

# -------- Expense Entry Form --------
with col_form:
    st.subheader("Add New Expense")
    with st.form("entry_form", clear_on_submit=True):
        title = st.text_input("Expense Title")
        amount = st.number_input("Amount ", min_value=0.01, step=0.01)
        category = st.selectbox("Category", ["Food", "Transport", "Bills", "Shopping","Clothes", "Other"])
        submitted = st.form_submit_button("Add Expense")

        if submitted:
            if not title:
                st.warning("Please enter a title for the expense.")
            else:
                data = {"title": title, "amount": amount, "category": category}
                response = requests.post(f"{API_URL}/add", json=data)
                if response.status_code == 201:
                    st.success("Expense successfully added.")
                else:
                    st.error("Failed to add expense. Please try again.")

# -------- Expense Data & Graphs --------
with col_graphs:
    st.subheader("Expense Dashboard")
    res = requests.get(f"{API_URL}/transactions")

    if res.status_code == 200 and res.json():
        df = pd.DataFrame(res.json())
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values(by="date", ascending=False)

        tab1, tab2 = st.tabs(["Overview Table", "Visualizations"])

        with tab1:
            st.dataframe(df, use_container_width=True)

        with tab2:
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### Expenses by Category")
                category_chart = df.groupby("category")["amount"].sum().sort_values(ascending=False)
                st.bar_chart(category_chart)

            with col2:
                st.markdown("#### Spending Trend Over Time")
                trend = df.groupby(df["date"].dt.date)["amount"].sum()
                st.line_chart(trend)
    else:
        st.info("No expenses to show yet. Add your first expense above.")

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="AI Business Dashboard", layout="wide")

st.title("📊 AI Business Dashboard")

file = st.file_uploader("Upload CSV file", type=["csv"])

if file:
    df = pd.read_csv(file)

    st.subheader("Preview Data")
    st.dataframe(df)

    # SAFE CHECKS
    required_cols = ["Sales", "Profit", "Category"]

    if all(col in df.columns for col in required_cols):

        col1, col2 = st.columns(2)
        col1.metric("Total Sales", df["Sales"].sum())
        col2.metric("Total Profit", df["Profit"].sum())

        st.subheader("Sales by Category")
        fig1 = px.bar(df, x="Category", y="Sales", color="Category")
        st.plotly_chart(fig1)

    else:
        st.error("CSV missing required columns: Sales, Profit, Category")

    # OPTIONAL REGION FILTER
    if "Region" in df.columns:
        region = st.selectbox("Filter by Region", df["Region"].unique())
        df = df[df["Region"] == region]

    # SAFE DATE HANDLING
    if "Date" in df.columns:
        try:
            df["Date"] = pd.to_datetime(df["Date"])
            trend = df.groupby("Date")["Sales"].sum().reset_index()

            st.subheader("Sales Trend")
            fig2 = px.line(trend, x="Date", y="Sales")
            st.plotly_chart(fig2)
        except:
            st.warning("Date column format issue")

    # AI INSIGHTS
    if st.button("Generate Insights"):
        st.subheader("AI Insights")

        if "Category" in df.columns:
            st.write("Top Category:", df.groupby("Category")["Sales"].sum().idxmax())

        if "Region" in df.columns:
            st.write("Top Region:", df.groupby("Region")["Sales"].sum().idxmax())

else:
    st.info("Please upload a CSV file to start analysis")
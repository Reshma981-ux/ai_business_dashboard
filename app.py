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

    # KPIs
    col1, col2 = st.columns(2)
    col1.metric("Total Sales", df["Sales"].sum())
    col2.metric("Total Profit", df["Profit"].sum())

    # Filters
    if "Region" in df.columns:
        region = st.selectbox("Select Region", df["Region"].unique())
        df = df[df["Region"] == region]

    # Charts
    st.subheader("Sales by Category")
    fig1 = px.bar(df, x="Category", y="Sales", color="Category")
    st.plotly_chart(fig1)

    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])
        trend = df.groupby("Date")["Sales"].sum().reset_index()

        st.subheader("Sales Trend")
        fig2 = px.line(trend, x="Date", y="Sales")
        st.plotly_chart(fig2)

    # AI Insight (simple)
    if st.button("Generate Insights"):
        st.subheader("AI Insights")

        st.write("Top Category:", df.groupby("Category")["Sales"].sum().idxmax())

        if "Region" in df.columns:
            st.write("Top Region:", df.groupby("Region")["Sales"].sum().idxmax())
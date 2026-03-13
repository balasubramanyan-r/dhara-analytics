import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import plotly.express as px

st.set_page_config(page_title="Dhara Analytics", layout="wide")

st.title("🏢 DHARA Marketing Dashboard")

# Google Sheets connection
@st.cache_data
def load_data():

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    import json

    creds_dict = st.secrets["gcp_service_account"]

    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        creds_dict, scope
    )

    client = gspread.authorize(creds)

    sheet = client.open("RealEstate_Marketing_Data")

    campaign_sheet = sheet.worksheet("Campaign_Data")
    visit_sheet = sheet.worksheet("Site_Visits")
    booking_sheet = sheet.worksheet("Bookings")
    campaign_df = pd.DataFrame(campaign_sheet.get_all_records())
    visit_df = pd.DataFrame(visit_sheet.get_all_records())
    booking_df = pd.DataFrame(booking_sheet.get_all_records())

    return campaign_df, visit_df, booking_df


df, visit_df, booking_df = load_data()

# Project filter
project = st.selectbox(
    "Select Project",
    ["All"] + list(df["Project"].unique())
)

if project != "All":
    df = df[df["Project"] == project]
    
# KPI calculations
total_spend = df["Spend"].sum()
total_leads = df["Leads"].sum()
total_visits = len(visit_df)
total_bookings = len(booking_df)

total_revenue = booking_df["Value"].sum() if "Value" in booking_df.columns else 0

cpl = total_spend / total_leads if total_leads > 0 else 0
roas = total_revenue / total_spend if total_spend > 0 else 0

# KPI Display
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

col1.metric("Ad Spend", f"₹{total_spend}")
col2.metric("Leads", total_leads)
col3.metric("Site Visits", total_visits)
col4.metric("Bookings", total_bookings)
col5.metric("Revenue", f"₹{total_revenue}")
col6.metric("CPL", f"₹{round(cpl,2)}")
col7.metric("ROAS", round(roas,2))

st.divider()

# Campaign performance chart
st.subheader("Lead → Visit → Booking Funnel")

funnel_data = pd.DataFrame({
    "Stage": ["Leads", "Site Visits", "Bookings"],
    "Count": [total_leads, total_visits, total_bookings]
})

fig = px.funnel(funnel_data, x="Count", y="Stage")

st.plotly_chart(fig, width='stretch')

st.subheader("Campaign Performance")

campaign_chart = px.bar(
    df,
    x="Campaign",
    y="Leads",
    color="Platform",
    title="Leads by Campaign"
)

st.plotly_chart(campaign_chart, width='stretch')

st.subheader("Spend vs Leads")

fig2 = px.scatter(
    df,
    x="Spend",
    y="Leads",
    color="Platform",
    size="Leads",
    hover_data=["Campaign"]
)

st.plotly_chart(fig2, width='stretch')

# Data table
st.subheader("Campaign Data")


st.dataframe(df)



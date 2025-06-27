import streamlit as st
from config import PAGE_TITLE, PAGE_LAYOUT, LOG_TABLES
from data_loader import get_summary_data, get_active_snowflake_session
from ui import render_header, render_cards, render_log_details
from visuals import show_status_distribution, show_time_series

# Config
st.set_page_config(page_title=PAGE_TITLE, layout=PAGE_LAYOUT)

# Header
render_header()

# Session
session = get_active_snowflake_session()

# Load data
summary_data = get_summary_data(session, LOG_TABLES)

# Card selection
selected_source = render_cards(summary_data)

# Log details
df = summary_data[selected_source]
render_log_details(df, selected_source)

# Visuals
if not df.empty:
    if 'status' in df.columns:
        show_status_distribution(df)
    if 'timestamp' in df.columns:
        show_time_series(df)

st.caption("Modern observability powered by Streamlit & Snowflake")

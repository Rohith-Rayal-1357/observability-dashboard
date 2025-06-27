import streamlit as st
import pandas as pd

def show_status_distribution(df):
    st.subheader("Status Distribution")
    counts = df['status'].value_counts()
    st.plotly_chart({
        "data": [{
            "labels": counts.index.tolist(),
            "values": counts.values.tolist(),
            "type": "pie"
        }],
        "layout": {"margin": {"l": 0, "r": 0, "b": 0, "t": 0}}
    })

def show_time_series(df):
    st.subheader("Logs Over Time")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    daily = df.groupby(df['timestamp'].dt.date).size()
    st.area_chart(daily)

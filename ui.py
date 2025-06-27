import streamlit as st

def render_header():
    st.markdown("""
        <div style='text-align: center; padding: 0.5rem 0; background: linear-gradient(90deg,#e3f2fd,#f5f7fa); border-radius: 18px;'>
            <h1 style='color: #1a237e; margin-bottom: 0;'>Observability Dashboard</h1>
            <p style='color: #616161; font-size:1.1rem; margin-top: 0;'>
                Unified monitoring for Prefect, dbt, Snowflake, and Power BI logs
            </p>
        </div>
    """, unsafe_allow_html=True)

def render_cards(summary_data: dict):
    st.subheader("System Overview")
    cols = st.columns(len(summary_data))
    selected = st.session_state.get("selected_source", list(summary_data.keys())[0])

    card_style = """
        background: #f5f7fa;
        border-radius: 16px;
        padding: 18px;
        box-shadow: 0 2px 8px #e3e3e3;
        text-align:center;
        transition: 0.2s all;
        cursor: pointer;
    """

    for i, (label, df) in enumerate(summary_data.items()):
        total = len(df)
        status_col = 'status' if 'status' in df.columns else None
        success = df[status_col].str.lower().eq('success').sum() if status_col else 0
        fail = df[status_col].str.lower().eq('fail').sum() if status_col else 0
        color = "#43a047" if success >= fail else "#e53935" if fail > 0 else "#757575"
        icon = "✅" if success >= fail else "❌" if fail > 0 else "ℹ️"
        highlight = "border: 3px solid #1976d2;" if selected == label else ""

        if cols[i].button(f"{icon} {label}\n\n{total} logs", key=label):
            selected = label
            st.session_state["selected_source"] = label

        cols[i].markdown(f"""
            <div style="{card_style}{highlight}">
                <span style='font-size: 1.2rem; color: #3949ab;'>{label}</span><br>
                <span style='font-size: 2.5rem; font-weight: 700; color: {color};'>{icon} {total}</span><br>
                <span style='font-size: 1rem; color: #757575;'>Total Logs</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    return selected

def render_log_details(df, label):
    st.markdown(f"<h2 style='color:#1976d2;'>{label} Logs</h2>", unsafe_allow_html=True)

    if df.empty:
        st.info("No logs available for this source.")
        return

    if 'status' in df.columns and (df['status'].str.lower() == 'fail').any():
        st.error(f"⚠️ {df['status'].str.lower().eq('fail').sum()} failures detected in {label} logs!")

    with st.expander("Show detailed logs table"):
        st.dataframe(df, use_container_width=True, hide_index=True)

    st.subheader("Inspect a Log Entry")
    if 'id' in df.columns:
        log_id = st.selectbox("Select Log ID", df['id'].astype(str).unique())
        log_details = df[df['id'].astype(str) == log_id]
    else:
        idx = st.number_input("Select row number", min_value=0, max_value=len(df)-1, value=0)
        log_details = df.iloc[[idx]]

    st.json(log_details.to_dict(orient='records')[0])

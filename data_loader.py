import pandas as pd
from snowflake.snowpark.context import get_active_session

def get_active_snowflake_session():
    return get_active_session()

def get_summary_data(session, log_tables: dict):
    summary = {}
    for label, table in log_tables.items():
        try:
            df = session.sql(f"SELECT * FROM OBSERVABILITY.{table} ORDER BY 1 DESC LIMIT 500").to_pandas()
            summary[label] = df
        except Exception:
            summary[label] = pd.DataFrame()
    return summary

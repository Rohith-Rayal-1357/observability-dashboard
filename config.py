PAGE_TITLE = "Observability Dashboard"
PAGE_LAYOUT = "wide"

LOG_TABLES = {
    "Prefect": "prefect_logs",
    "File Ingestion": "file_ingestion_logs",
    "dbt Run": "dbt_run_result",
    "dbt Manifest": "dbt_manifest",
    "Snowflake Query": "snowflake_query_logs",
    "Snowflake Task": "snowflake_task_logs",
    "Power BI": "powerbi_refresh_logs"
}

resource "snowflake_account_role" "airflow_role" {
  name = "AIRFLOW_ROLE"
  comment = "Role for Airflow ingestion"
}

resource "snowflake_account_role" "dbt_role" {
  name = "DBT_ROLE"
  comment = "Role for dbt transformations"
}

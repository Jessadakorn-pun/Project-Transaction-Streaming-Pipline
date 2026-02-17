resource "snowflake_account_role" "airflow_role" {
  name = "AIRFLOW_ROLE"
  comment = "Role for Airflow ingestion"
}

resource "snowflake_account_role" "dbt_role" {
  name = "DBT_ROLE"
  comment = "Role for dbt transformations"
}

resource "snowflake_grant_account_role" "grant_airflow_role_to_user" {
  role_name = snowflake_account_role.airflow_role.name
  user_name = snowflake_user.airflow_user.name
}

resource "snowflake_grant_account_role" "grant_dbt_role_to_user" {
  role_name = snowflake_account_role.dbt_role.name
  user_name = snowflake_user.dbt_user.name
}
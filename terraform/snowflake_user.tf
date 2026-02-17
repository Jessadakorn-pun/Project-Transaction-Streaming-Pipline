resource "snowflake_user" "airflow_user" {
  name                 = "AIRFLOW_USER"
  password             = var.airflow_user_password
  default_role         = snowflake_account_role.airflow_role.name
  must_change_password = false
  comment              = "Service account for Airflow"
}

resource "snowflake_user" "dbt_user" {
  name                 = "DBT_USER"
  password             = var.dbt_user_password
  default_role         = snowflake_account_role.dbt_role.name
  must_change_password = false
  comment              = "Service account for dbt transformations"
}
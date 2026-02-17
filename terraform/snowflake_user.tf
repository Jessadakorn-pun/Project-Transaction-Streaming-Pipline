resource "snowflake_user" "airflow_user" {
  name                 = "AIRFLOW_USER"
  password             = var.airflow_user_password
  default_role         = snowflake_account_role.airflow_role.name
  must_change_password = false
  comment              = "Service account for Airflow"
}
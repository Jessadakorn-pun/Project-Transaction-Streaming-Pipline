resource "snowflake_grant_privileges_to_account_role" "airflow_raw_schema" {
  account_role_name = snowflake_account_role.airflow_role.name
  privileges        = ["ALL"]

  on_schema {
    schema_name = "${snowflake_database.banking.name}.${snowflake_schema.raw.name}"
  }
}

resource "snowflake_grant_privileges_to_account_role" "dbt_analytic_schema" {
  account_role_name = snowflake_account_role.dbt_role.name
  privileges        = ["ALL"]

  on_schema {
    schema_name = "${snowflake_database.banking.name}.${snowflake_schema.analytic.name}"
  }
}

resource "snowflake_grant_privileges_to_account_role" "dbt_mart_schema" {
  account_role_name = snowflake_account_role.dbt_role.name
  privileges        = ["ALL"]

  on_schema {
    schema_name = "${snowflake_database.banking.name}.${snowflake_schema.mart.name}"
  }
}

resource "snowflake_grant_privileges_to_account_role" "airflow_wh_usage" {
  account_role_name = snowflake_account_role.airflow_role.name
  privileges        = ["USAGE"]

  on_account_object {
    object_type = "WAREHOUSE"
    object_name = snowflake_warehouse.transforming.name
  }
}

resource "snowflake_grant_privileges_to_account_role" "dbt_wh_usage" {
  account_role_name = snowflake_account_role.dbt_role.name
  privileges        = ["USAGE"]

  on_account_object {
    object_type = "WAREHOUSE"
    object_name = snowflake_warehouse.transforming.name
  }
}

resource "snowflake_grant_privileges_to_account_role" "dbt_database_usage" {
  account_role_name = snowflake_account_role.dbt_role.name
  privileges        = ["USAGE"]

  on_account_object {
    object_type = "DATABASE"
    object_name = snowflake_database.banking.name
  }
}

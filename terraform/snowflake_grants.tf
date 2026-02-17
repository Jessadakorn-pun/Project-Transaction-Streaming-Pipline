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

resource "snowflake_grant_privileges_to_account_role" "airflow_database_usage" {
  account_role_name = snowflake_account_role.airflow_role.name
  privileges        = ["USAGE"]

  on_account_object {
    object_type = "DATABASE"
    object_name = snowflake_database.banking.name
  }
}

resource "snowflake_grant_privileges_to_account_role" "airflow_raw_schema_usage" {
  account_role_name = snowflake_account_role.airflow_role.name
  privileges        = ["USAGE"]

  on_schema {
    schema_name = "${snowflake_database.banking.name}.${snowflake_schema.raw.name}"
  }
}

resource "snowflake_grant_privileges_to_account_role" "airflow_stage_rw" {
  account_role_name = snowflake_account_role.airflow_role.name
  privileges        = ["READ", "WRITE"]

  on_schema_object {
    object_type = "STAGE"
    object_name = "${snowflake_database.banking.name}.${snowflake_schema.raw.name}.${snowflake_stage.airflow_stage.name}"
  }
}


resource "snowflake_grant_privileges_to_account_role" "airflow_raw_tables" {
  for_each = snowflake_table.raw_tables

  account_role_name = snowflake_account_role.airflow_role.name
  privileges        = ["INSERT", "SELECT"]

  on_schema_object {
    object_type = "TABLE"
    object_name = "${snowflake_database.banking.name}.${snowflake_schema.raw.name}.${each.key}"
  }
}

resource "snowflake_grant_privileges_to_account_role" "dbt_raw_all_tables_select" {
  account_role_name = snowflake_account_role.dbt_role.name
  privileges        = ["SELECT"]

  on_schema_object {
    all {
      object_type_plural = "TABLES"
      in_schema          = "${snowflake_database.banking.name}.${snowflake_schema.raw.name}"
    }
  }
}

resource "snowflake_grant_privileges_to_account_role" "dbt_raw_future_tables_select" {
  account_role_name = snowflake_account_role.dbt_role.name
  privileges        = ["SELECT"]

  on_schema_object {
    future {
      object_type_plural = "TABLES"
      in_schema          = "${snowflake_database.banking.name}.${snowflake_schema.raw.name}"
    }
  }
}

resource "snowflake_grant_privileges_to_account_role" "airflow_raw_create_table" {
  account_role_name = snowflake_account_role.airflow_role.name
  privileges        = ["CREATE TABLE"]

  on_schema {
    schema_name = "${snowflake_database.banking.name}.${snowflake_schema.raw.name}"
  }
}

resource "snowflake_grant_privileges_to_account_role" "airflow_raw_schema_create_stage" {
  account_role_name = snowflake_account_role.airflow_role.name
  privileges        = ["CREATE STAGE"]

  on_schema {
    schema_name = "${snowflake_database.banking.name}.${snowflake_schema.raw.name}"
  }
}

resource "snowflake_grant_privileges_to_account_role" "dbt_raw_schema_usage" {
  account_role_name = snowflake_account_role.dbt_role.name
  privileges        = ["USAGE"]

  on_schema {
    schema_name = "${snowflake_database.banking.name}.${snowflake_schema.raw.name}"
  }
}



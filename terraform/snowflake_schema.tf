resource "snowflake_schema" "raw" {
    database = snowflake_database.banking.name
    name = "RAW"
    comment = "Raw ingestion layer"
}

resource "snowflake_schema" "analytic" {
    database = snowflake_database.banking.name
    name = "ANALYTIC"
    comment = "Cleaned and conformed layer"
}

resource "snowflake_schema" "mart" {
    database = snowflake_database.banking.name
    name = "MART"
    comment = "Business data marts"
}

resource "snowflake_stage" "airflow_stage" {
  name     = "AIRFLOW_STAGE"
  database = snowflake_database.banking.name
  schema   = snowflake_schema.raw.name
  comment  = "Stage for Airflow raw ingestion"
}
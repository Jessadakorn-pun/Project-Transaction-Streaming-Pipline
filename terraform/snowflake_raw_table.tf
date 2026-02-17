resource "snowflake_table" "raw_tables" {
  for_each = toset(local.raw_tables)

  database = snowflake_database.banking.name
  schema   = snowflake_schema.raw.name
  name     = each.key

  column {
    name = "RAW_DATA"
    type = "VARIANT"
  }

  column {
    name = "METADATA_FILENAME"
    type = "STRING"
  }

  column {
    name = "LOADED_AT"
    type = "TIMESTAMP_NTZ"
    default {
      expression = "CURRENT_TIMESTAMP()"
    }
  }
}
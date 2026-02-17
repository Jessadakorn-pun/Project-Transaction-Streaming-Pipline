output "database" {
    value = snowflake_database.banking.name
}

output "warehouse" {
    value =  snowflake_warehouse.transforming.name
}
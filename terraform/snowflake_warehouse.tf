resource "snowflake_warehouse" "transforming" {
    name = "BANKING_WH"
    warehouse_size = var.warehouse_size
    auto_suspend = 60
    auto_resume = true
    comment = "Warehouse for Airflow service and DBT"
}
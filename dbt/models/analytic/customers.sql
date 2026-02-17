{{ config(materialized='table') }}

select 
    raw_data:id::int as customer_id
    , raw_data:first_name::string as first_name
    , raw_data:last_name::string as last_name
    , raw_data:email::string as email
    , raw_data:created_at::timestamp as created_at
    , loaded_at

from {{ source('raw', 'customers') }}

qualify row_number() over ( partition by raw_data:id order by loaded_at desc) = 1
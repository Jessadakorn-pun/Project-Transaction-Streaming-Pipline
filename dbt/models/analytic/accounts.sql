{{ config(materialized = 'table') }}

select 
    raw_data:id::int as account_id
    , raw_data:customer_id::int as customer_id
    , raw_data:account_type::string as account_type
    , raw_data:balance::number(18, 2) as balance
    , raw_data:currency::string as currency
    , raw_data:created_at::timestamp as created_at

from {{ source('raw', 'accounts') }}

qualify row_number() over (partition by raw_data:id order by loaded_at desc) = 1
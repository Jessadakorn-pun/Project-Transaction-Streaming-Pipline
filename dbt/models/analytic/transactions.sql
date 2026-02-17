{{ config(materialized = 'table') }}

select 
    raw_data:id::int as transaction_id
    , raw_data:account_id::int as account_id
    , raw_data:txn_type::string as txn_type
    , raw_data:amount::number(18, 2) as amount
    , raw_data:status::string as status
    , raw_data:created_at::timestamp as created_at

from {{ source('raw', 'transactions') }}

qualify row_number() over (partition by raw_data:id order by loaded_at desc) = 1
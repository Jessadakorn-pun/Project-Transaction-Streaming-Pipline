{{ config(materialized = 'view') }}

select 
    c.customer_id
    , c.first_name
    , c.last_name
    , c.email
    , count(distinct a.account_id) as total_account
    , sum(a.balance) as total_balance
    , min(c.created_at) as customer_since

from {{ ref('customers') }} c
left join {{ ref('accounts') }} a
    on c.customer_id = a.customer_id
group by 1,2,3,4
{{ config(materialized = 'view') }}

select
    c.customer_id
    , c.first_name
    , c.last_name
    , count(t.transaction_id) as total_txn
    , sum(t.amount) as total_txn_amount
    , avg(t.amount) as avg_txn_amount
    , min(t.created_at) as first_txn_date
    , max(t.created_at) as last_txn_date


from {{ ref('transactions') }} t
join {{ ref('accounts') }} a
    on t.account_id = a.account_id
join {{ ref('customers')}} c
    on a.customer_id = c.customer_id
where 1=1
    and t.status = 'COMPLETE'
group by 1,2,3
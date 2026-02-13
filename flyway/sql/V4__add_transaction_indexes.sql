CREATE INDEX IF NOT EXISTS idx_transactions_account_created on transactions(account_id, created_at)
;
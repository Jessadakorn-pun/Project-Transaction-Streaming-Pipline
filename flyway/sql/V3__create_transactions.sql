CREATE TABLE IF NOT EXISTS transactions (
    id BIGSERIAL PRIMARY KEY
    , account_id INT NOT NULL
    , txn_type VARCHAR(50) NOT NULL
    , amount NUMERIC (18, 2) NOT NULL CHECK (amount > 0)
    , related_account_id INT NULL
    , status VARCHAR(20) NOT NULL DEFAULT 'COMPLETE'
    , created_at TIMESTAMP WITH TIME ZONE DEFAULT now()

    , CONSTRAINT fk_transactions_account FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE
) 
;
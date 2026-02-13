CREATE TABLE IF NOT EXISTS accounts (
    id BIGSERIAL PRIMARY KEY
    , customer_id INT NOT NULL
    , account_type VARCHAR(50) NOT NULL
    , balance NUMERIC(18, 2) NOT NULL DEFAULT 0 CHECK (balance >= 0)
    , currency CHAR(3) NOT NULL DEFAULT 'USD'
    , created_at TIMESTAMP WITH TIME ZONE DEFAULT now()

    , CONSTRAINT fk_accounts_customer FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
)
;
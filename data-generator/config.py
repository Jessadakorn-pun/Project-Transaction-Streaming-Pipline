from decimal import Decimal

CONFIG ={
    # data generator config
    "NUM_CUSTOMERS": 10,
    "ACCOUNTS_PER_CUSTOMER": 2,
    "NUM_TRANSACTIONS": 50,
    "MAX_TXN_AMOUNT": 1000.00,
    "CURRENCY": "USD",

    # Non-zero initial balances
    "INITIAL_BALANCE_MIN": Decimal("10.00"),
    "INITIAL_BALANCE_MAX": Decimal("1000.00"),

    # Loop config
    "DEFAULT_LOOP": True,
    "SLEEP_SECONDS": 2
}
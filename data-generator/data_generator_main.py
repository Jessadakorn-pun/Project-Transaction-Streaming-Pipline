import os
import sys
import time
import psycopg2
from faker import Faker
import random
import argparse
from typing import List
from decimal import Decimal, ROUND_DOWN
from db_utils import get_connection
from config import CONFIG

def random_money(min_val: Decimal, max_val: Decimal) -> Decimal:
    val = Decimal(str(random.uniform(float(min_val), float(max_val))))
    return val.quantize(Decimal("0.01"), rounding=ROUND_DOWN)

def generate_customer(num_customer: int, faker: Faker, conn)-> list[int]:

    customers_ids = list()
    
    query = """
        
        INSERT INTO customers (first_name, last_name, email) VALUES (%s, %s, %s) RETURNING id
        
    """
    try:
        with conn.cursor() as cur:
            for _ in range(num_customer):
                first_name = faker.first_name()
                last_name = faker.last_name()
                email = faker.unique.email()
        
                cur.execute(query, (first_name, last_name, email))
                customers_ids.append(cur.fetchone()[0])
                
    except Exception as err:
        conn.rollback()
        raise RuntimeError(f"!! Customer Data Inserted Fail: {err} \n")
        
    print("     Process Insert Customers: < Complete > \n")
    return customers_ids
     
    
                   
def generate_account(customer_ids:list[int], faker: Faker, account_per_customer: int, initial_min_balance: float, initial_max_balance: float, currency: str, conn) -> list:
    
    account_ids = list()
    query = """
    
    INSERT INTO accounts (customer_id, account_type, balance, currency) VALUES (%s, %s, %s, %s) RETURNING id
    
    """
    try:
        with conn.cursor() as cur:
            for customer_id in customer_ids:
                for _ in range(account_per_customer):
                    account_type = random.choice(["SAVINGS", "CHECKING"])
                    initial_balance = random_money(initial_min_balance, initial_max_balance)
                    
                    cur.execute(query, (customer_id, account_type, initial_balance, currency))
                    account_ids.append(cur.fetchone()[0])
          
    except Exception as err:
        conn.rollback()
        raise RuntimeError(f"!! Account Data Inserted Fail: {err} \n")
        
    print("     Process Insert Accounts: < Complete > \n")
    return account_ids

def generate_transaction(account_ids: list[int], number_transactions: int, max_transaction_amount: float, conn)-> None:
    
    query = """
        INSERT INTO transactions (account_id, txn_type, amount, related_account_id, status) VALUES (%s, %s, %s, %s, 'COMPLETED')
    """
    
    transaction_types = ["DEPOSIT", "WITHDRAWAL", "TRANSFER"]
    
    try:
        with conn.cursor() as cur:
            for _ in range(number_transactions):
                account_id = random.choice(account_ids)
                transaction_type = random.choice(transaction_types)
                amount = round(random.uniform(1, max_transaction_amount), 2)
                related_account = None
                if transaction_type == "TRANSFER" and len(account_ids) > 1:
                    related_account = random.choice(list(set(account_ids) - {account_id}))
                    
                cur.execute(query, (account_id, transaction_type, amount, related_account))

    except Exception as err:
        conn.rollback()
        raise RuntimeError(f"!! Account Data Inserted Fail: {err} \n")

    print("     Process Insert Transaction: < Complete >\n")

def main():

    # CLI override (run once mode)
    parser = argparse.ArgumentParser(description="Run fake data generator")
    parser.add_argument("--once", action="store_true", help="Run a single iteration and exit")
    args = parser.parse_args()
    LOOP = not args.once and CONFIG["DEFAULT_LOOP"]
    
    faker = Faker()
    conn = get_connection()
    conn.autocommit = False
    
    try:
        
        interation = 0
        print("\n ==================== Start Streaming Data ==================== \n")
        
        while True:
            
            interation += 1
            
            print(f"------ Start Interation: {interation} ------ \n")
            
            customer_ids = generate_customer(CONFIG["NUM_CUSTOMERS"], faker, conn)
            account_ids = generate_account(customer_ids, faker, CONFIG["ACCOUNTS_PER_CUSTOMER"], CONFIG["INITIAL_BALANCE_MIN"], CONFIG["INITIAL_BALANCE_MAX"], CONFIG["CURRENCY"], conn)
            generate_transaction(account_ids, CONFIG["NUM_TRANSACTIONS"], CONFIG["MAX_TXN_AMOUNT"], conn)
            
            conn.commit()
            print(f"---- Generated {len(customer_ids)} customer, {len(account_ids)} accounts, {CONFIG["NUM_TRANSACTIONS"]} transactions ----")
            print(f"------ End Interation: {interation} ------ \n")
            
            if not LOOP:
                break
            
            time.sleep(CONFIG["SLEEP_SECONDS"])
            
    except KeyboardInterrupt:
        print("\n ==================== < Interrupted by user, Exiting Script > ==================== \n")
    except Exception as e:
        print(f"!! ERROR OCCURRED: {e} \n")

        
    finally:
        conn.close()
        sys.exit(0)    
        

if __name__ == "__main__":
    main()

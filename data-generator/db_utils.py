import psycopg2
import os

def get_connection() -> psycopg2.extensions.connection:
    
    connection = psycopg2.connect(
        host = os.getenv("POSTGRES_HOST"),
        port = os.getenv("POSTGRES_PORT", 5432),
        dbname = os.getenv("POSTGRES_DB"),
        user = os.getenv("POSTGRES_USER"),
        password = os.getenv("POSTGRES_PASSWORD")
    )
    
    return connection

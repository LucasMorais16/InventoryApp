import psycopg

DB_CONFIG = {
    "host": "localhost",
    "dbname": "inventory_db",
    "user": "postgres",
    "password": "123"
}

def connect():
    """Conecta ao banco de dados PostgreSQL usando psycopg."""
    return psycopg.connect(**DB_CONFIG)

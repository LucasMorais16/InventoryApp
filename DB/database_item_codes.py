# database_item_codes.py
from .databaseConnect import connect

def create_item_codes_table():
    """Cria a tabela de códigos dos itens, se não existir."""
    query = """
    CREATE TABLE IF NOT EXISTS item_codes (
        id SERIAL PRIMARY KEY,
        code VARCHAR(5) UNIQUE NOT NULL,
        name VARCHAR(100) NOT NULL
    );
    """
    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
        conn.commit()

def populate_item_codes_data():
    """
    Popula a tabela com pelo menos 15 itens.  
    Exemplo: código 68790 e nome 'mouse' e outros itens à sua escolha.
    """
    item_codes = [
        ("68790", "mouse"),
        ("12345", "keyboard"),
        ("23456", "monitor"),
        ("34567", "printer"),
        ("45678", "usb cable"),
        ("56789", "laptop"),
        ("67890", "webcam"),
        ("78901", "headphones"),
        ("89012", "microphone"),
        ("90123", "speakers"),
        ("11223", "charger"),
        ("22334", "desk lamp"),
        ("33445", "router"),
        ("44556", "external HDD"),
        ("55667", "SSD drive")
    ]
    with connect() as conn:
        with conn.cursor() as cursor:
            for code, name in item_codes:
                cursor.execute(
                    "INSERT INTO item_codes (code, name) VALUES (%s, %s) ON CONFLICT (code) DO NOTHING;",
                    (code, name)
                )
        conn.commit()

def get_item_codes():
    """Retorna a lista de códigos dos itens disponíveis."""
    query = "SELECT code, name FROM item_codes ORDER BY code;"
    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()

from .databaseConnect import connect

def create_departments_table():
    """Cria a tabela de departamentos, se não existir."""
    query = """
    CREATE TABLE IF NOT EXISTS departments (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) UNIQUE NOT NULL
    );
    """
    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)

def populate_departments_data():
    """Popula a tabela de departamentos com os dados padrão."""
    departments = [
    "I.T",
    "H.R",
    "Finance",
    "Procurement",
    "Marketing",
    "Sales",
    "Legal",
    "Operations",
    "Customer Support",
    "Research & Development"
    ]
    with connect() as conn:
        with conn.cursor() as cursor:
            for dept in departments:
                cursor.execute("INSERT INTO departments (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;", (dept,))
        conn.commit()

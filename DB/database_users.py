from .databaseConnect import connect

def create_user_tables():
    query = '''
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        continent VARCHAR(255) NOT NULL,
        location VARCHAR(100) NOT NULL,
        department VARCHAR(100) NOT NULL,
        email_verified BOOLEAN NOT NULL DEFAULT FALSE
    );
    '''
    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)

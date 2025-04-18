from .databaseConnect import connect

def create_tokens_table():
    query = '''
    CREATE TABLE IF NOT EXISTS tokens (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
        token VARCHAR(255) NOT NULL,
        type VARCHAR(50) NOT NULL,
        expires_at TIMESTAMP NOT NULL
    );
    '''
    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
        conn.commit()
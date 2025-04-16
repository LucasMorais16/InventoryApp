from .databaseConnect import connect

def create_stockroom_table():
    query = """
    CREATE TABLE IF NOT EXISTS stockroom (
        id SERIAL PRIMARY KEY,
        item_code VARCHAR(5) NOT NULL,
        item_name VARCHAR(100) NOT NULL,
        user_name VARCHAR(100) NOT NULL,
        location VARCHAR(100) NOT NULL,
        department VARCHAR(100) NOT NULL,
        created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        removed_date TIMESTAMP
    );
    """
    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query)
        conn.commit()

def get_stockroom_items(location, department, filters=None):
    """
    Retorna os itens do estoque filtrados pela localidade e departamento,
    além de filtros opcionais.
    
    filters pode incluir:
      - 'item_code' (str)
      - 'item_name' (str)
      - 'user_name' (str)
      - 'created_date' (str)
      - 'removed' (bool) -> indica se filtra itens removidos ou não
    """
    base_query = """
    SELECT id, item_code, item_name, user_name, created_date, removed_date
    FROM stockroom
    WHERE location = %s AND department = %s
    """
    params = [location, department]

    # Adiciona filtros convencionais
    if filters:
        if filters.get('item_code'):
            base_query += " AND item_code::text LIKE %s"
            params.append('%' + filters['item_code'] + '%')
        if filters.get('item_name'):
            base_query += " AND item_name ILIKE %s"
            params.append('%' + filters['item_name'] + '%')
        if filters.get('user_name'):
            base_query += " AND user_name ILIKE %s"
            params.append('%' + filters['user_name'] + '%')
        if filters.get('created_date'):
            base_query += " AND created_date::text LIKE %s"
            params.append('%' + filters['created_date'] + '%')

        # Filtro para removido ou não
        if 'removed' in filters:
            if filters['removed']:  # Exibir itens removidos
                base_query += " AND removed_date IS NOT NULL"
            else:                   # Exibir itens não removidos
                base_query += " AND removed_date IS NULL"

    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute(base_query, tuple(params))
            return cursor.fetchall()

def add_stockroom_item(item_code, item_name, user_name, location, department):
    query = """
    INSERT INTO stockroom (item_code, item_name, user_name, location, department)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id;
    """
    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (item_code, item_name, user_name, location, department))
            item_id = cursor.fetchone()[0]
        conn.commit()
    return item_id

def remove_stockroom_item(item_id):
    query = """
    UPDATE stockroom
    SET removed_date = CURRENT_TIMESTAMP
    WHERE id = %s
    """
    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (item_id,))
        conn.commit()

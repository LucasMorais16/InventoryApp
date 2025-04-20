from .databaseConnect import connect

def create_checklist_templates_tables():
    query_templates = """
    CREATE TABLE IF NOT EXISTS checklist_templates (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        created_by INTEGER NOT NULL,
        created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """
    query_items = """
    CREATE TABLE IF NOT EXISTS checklist_template_items (
        id SERIAL PRIMARY KEY,
        template_id INTEGER REFERENCES checklist_templates(id) ON DELETE CASCADE,
        item_text TEXT NOT NULL,
        position INTEGER NOT NULL
    );
    """
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query_templates)
            cur.execute(query_items)
        conn.commit()

def get_all_templates():
    query = "SELECT id, title FROM checklist_templates ORDER BY created_date DESC;"
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()

def add_new_template(title, items, user_id):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO checklist_templates (title, created_by) VALUES (%s, %s) RETURNING id;",
                (title, user_id)
            )
            tpl_id = cur.fetchone()[0]
            for idx, item in enumerate(items, start=1):
                cur.execute(
                    "INSERT INTO checklist_template_items (template_id, item_text, position) VALUES (%s, %s, %s);",
                    (tpl_id, item, idx)
                )
        conn.commit()
    return tpl_id

def get_template_by_id(template_id):
    tpl_query = "SELECT title FROM checklist_templates WHERE id = %s;"
    items_query = "SELECT item_text FROM checklist_template_items WHERE template_id = %s ORDER BY position;"
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(tpl_query, (template_id,))
            row = cur.fetchone()
            if not row:
                return None
            title = row[0]
            cur.execute(items_query, (template_id,))
            items = [r[0] for r in cur.fetchall()]
    return {"title": title, "items": items}
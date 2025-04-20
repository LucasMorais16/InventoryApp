from .databaseConnect import connect

def create_checklists_tables():
    query_main = """
    CREATE TABLE IF NOT EXISTS checklists (
        id SERIAL PRIMARY KEY,
        template_id INTEGER REFERENCES checklist_templates(id) ON DELETE CASCADE,
        created_by VARCHAR(100) NOT NULL,
        equipment VARCHAR(255),
        recipient VARCHAR(255),
        created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    """
    query_results = """
    CREATE TABLE IF NOT EXISTS checklist_results (
        id SERIAL PRIMARY KEY,
        checklist_id INTEGER REFERENCES checklists(id) ON DELETE CASCADE,
        item_text TEXT NOT NULL,
        checked BOOLEAN NOT NULL
    );
    """
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query_main)
            cur.execute(query_results)
        conn.commit()

def get_checklists_for_template(template_id):
    query = "SELECT id, equipment, recipient, created_by, created_date FROM checklists WHERE template_id = %s ORDER BY created_date DESC;"
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (template_id,))
            return cur.fetchall()

def add_new_checklist(template_id, user_name, equipment, recipient, results):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO checklists (template_id, created_by, equipment, recipient) VALUES (%s, %s, %s, %s) RETURNING id;",
                (template_id, user_name, equipment, recipient)
            )
            chk_id = cur.fetchone()[0]
            for item_text, checked in results.items():
                cur.execute(
                    "INSERT INTO checklist_results (checklist_id, item_text, checked) VALUES (%s, %s, %s);",
                    (chk_id, item_text, checked)
                )
        conn.commit()
    return chk_id

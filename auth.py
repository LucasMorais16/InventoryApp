from DB.databaseConnect import connect
import psycopg
import bcrypt
import secrets
from datetime import datetime, timedelta
from DB.database_tokens import create_tokens_table  # já executado via databaseInit
from mail_utils import send_email


def hash_password(password):
    """Cria um hash para a senha usando bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password, hashed_password):
    """Verifica se a senha corresponde ao hash armazenado."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def send_password_reset(email: str) -> bool:
    # Busca usuário
    q = "SELECT id,name FROM users WHERE email=%s"
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(q, (email,))
            row = cur.fetchone()
    if not row:
        return False
    user_id, name = row
    token = _create_token(user_id, "password_reset")
    link = f"http://localhost:5000/reset_password?token={token}"
    subj = "Redefina sua senha"
    body = f"Hello {name},\nClick on the link to create a new password:\n{link}\n\nLink valid for 1 hour"
    send_email(subj, body, email)
    return True

def reset_password(token: str, new_password: str) -> bool:
    user_id = _consume_token(token, "password_reset")
    if not user_id:
        return False
    hashed = hash_password(new_password)
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE users SET password=%s WHERE id=%s", (hashed, user_id))
        conn.commit()
    return True

def validate_registration_fields(name, email, password, continent, location, department):
    """Valida os campos de registro."""
    placeholders = {
        "name": (name, "Type your name", "Name field is required."),
        "email": (email, "Type your email", "Email field is required."),
        "password": (password, "Type your password", "Password field is required."),
        "continent": (continent, "Select your Global Location", "Continent field is required."),
        "location": (location, "Select your Local Location", "Location field is required."),
        "department": (department, "Select your Department", "Department field is required.")
    }

    all_invalid = all(value == placeholder or not value for value, placeholder, _ in placeholders.values())
    if all_invalid:
        return False, "All fields are required"

    for _, (value, placeholder, error_message) in placeholders.items():
        if value == placeholder or not value:
            return False, error_message

    return True, ""

def login_user(email, password):
    """Autentica um usuário com base no email e na senha."""
    query = "SELECT * FROM users WHERE email = %s"
    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (email,))
            user = cursor.fetchone()            
            if user and verify_password(password, user[3]):
                if user[7] is False:
                    return False
                return user
            else:
                return None
    

def register_user(name, email, password, continent, location, department):
    hashed = hash_password(password)
    insert = "INSERT INTO users (name,email,password,continent,location,department) VALUES (%s,%s,%s,%s,%s,%s) RETURNING id"
    with connect() as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(insert, (name,email,hashed,continent,location,department))
                user_id = cur.fetchone()[0]
                conn.commit()
            except psycopg.errors.UniqueViolation:
                return "error", "Email already registered."

    # Gera e envia token de VERIFICAÇÃO
    token = _create_token(user_id, "email_verification")
    link  = f"http://localhost:5000/verify_email?token={token}"
    subject = "Confirm your e-mail"
    body = f"Hello {name},\nClick on the link to activate your account\n{link}\n\nThis link will be valid for 1 hour"
    send_email(subject, body, email)
    return "success", "Registration Sucessful! Please, verify your e-mail."

def verify_email(token: str) -> bool:
    user_id = _consume_token(token, "email_verification")
    if not user_id:
        return False
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE users SET email_verified = TRUE WHERE id = %s", (user_id,))
        conn.commit()
    return True
       

def _create_token(user_id: int, token_type: str) -> str:
    token = secrets.token_urlsafe(32)
    expires = datetime.utcnow() + timedelta(hours=1)
    query = "INSERT INTO tokens (user_id, token, type, expires_at) VALUES (%s, %s, %s, %s)"
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (user_id, token, token_type, expires))
            conn.commit()
    return token

def _consume_token(token: str, expected_type: str) -> int | None:
    """
    Retorna user_id se token válido, ou None. Remove token após uso.
    """
    select_q = "SELECT user_id FROM tokens WHERE token=%s AND type=%s AND expires_at > NOW()"
    delete_q = "DELETE FROM tokens WHERE token=%s"
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(select_q, (token, expected_type))
            row = cur.fetchone()
            if not row:
                return None
            user_id = row[0]
            cur.execute(delete_q, (token,))
        conn.commit()
    return user_id
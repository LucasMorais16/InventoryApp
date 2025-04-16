from DB.databaseConnect import connect
import psycopg
import bcrypt

def hash_password(password):
    """Cria um hash para a senha usando bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password, hashed_password):
    """Verifica se a senha corresponde ao hash armazenado."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def validate_registration_fields(name, email, password, continent, location, department):
    """Valida os campos de registro."""
    placeholders = {
        "name": "Type your name",
        "email": "Type your email",
        "password": "Type your password",
        "continent": "Select your Global Location",
        "location": "Select your Local Location",
        "department": "Select your Department"
    }

    if (name == placeholders["name"] or not name) and (email == placeholders["email"] or not email) and (password == placeholders["password"] or not password) and (continent == placeholders["continent"] or not continent) and (location == placeholders["location"] or not location) and (department == placeholders["department"] or not department):
        return False, "All fields are required"

    if name == placeholders["name"] or not name:
        return False, "Name field is required."
    if email == placeholders["email"] or not email:
        return False, "Email field is required."
    if password == placeholders["password"] or not password:
        return False, "Password field is required."
    if continent == placeholders["continent"] or not continent:
        return False, "Continent field is required."
    if location == placeholders["location"] or not location:
        return False, "Location field is required."
    if department == placeholders["department"] or not department:
        return False, "Department field is required."

    return True, ""

def register_user(name, email, password, continent, location, department):
    """Registra um novo usuário no banco de dados."""
    query = """
    INSERT INTO users (name, email, password, continent, location, department)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    hashed_password = hash_password(password)
    with connect() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute(query, (name, email, hashed_password, continent, location, department))
                conn.commit()
                return "success", "User successfully registered!"
            except psycopg.errors.UniqueViolation:
                return "error", "Email is already in use."

def login_user(email, password):
    """Autentica um usuário com base no email e na senha."""
    query = "SELECT * FROM users WHERE email = %s"
    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            if user and verify_password(password, user[3]):
                return user
            else:
                return None

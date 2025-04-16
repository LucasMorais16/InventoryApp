from .databaseConnect import connect

def create_location_tables():
    """Cria as tabelas para continentes e localidades."""
    create_continents_query = """
    CREATE TABLE IF NOT EXISTS continents (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) UNIQUE NOT NULL
    );
    """
    
    create_locations_query = """
    CREATE TABLE IF NOT EXISTS locations (
        id SERIAL PRIMARY KEY,
        city_name VARCHAR(100) NOT NULL,
        continent_id INTEGER NOT NULL,
        FOREIGN KEY (continent_id) REFERENCES continents(id) ON DELETE CASCADE
    );
    """

    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute(create_continents_query)
            cursor.execute(create_locations_query)

def populate_location_data():
    """Insere dados de continentes e localidades no banco de dados, garantindo que não haja duplicação."""
    continents = ["South America", "North America", "Asia", "Europe", "Oceania"]

    locations = {
        "South America": [
            "São Paulo", "Buenos Aires", "Rio de Janeiro", "Santiago",
            "Lima", "Bogotá", "Montevideo", "Quito", "Caracas", "Ponta Grossa"
        ],
        "North America": [
            "New York", "Los Angeles", "Chicago", "Houston",
            "Toronto", "Vancouver", "Montreal", "San Francisco", "Miami", "Dallas"
        ],
        "Asia": [
            "Tokyo", "Beijing", "Seoul", "Shanghai",
            "Mumbai", "Bangkok", "Singapore", "Kuala Lumpur", "Jakarta", "Delhi"
        ],
        "Europe": [
            "London", "Paris", "Berlin", "Madrid",
            "Rome", "Amsterdam", "Vienna", "Prague", "Moscow", "Copenhagen"
        ],
        "Oceania": [
            "Sydney", "Melbourne", "Brisbane", "Auckland",
            "Wellington", "Perth", "Adelaide", "Canberra", "Hobart", "Christchurch"
        ]
    }

    with connect() as conn:
        with conn.cursor() as cursor:
            # Insere os continentes
            continent_ids = {}
            for continent in continents:
                cursor.execute("INSERT INTO continents (name) VALUES (%s) ON CONFLICT (name) DO NOTHING RETURNING id;", (continent,))
                result = cursor.fetchone()
                if result:
                    continent_ids[continent] = result[0]
                else:
                    cursor.execute("SELECT id FROM continents WHERE name = %s;", (continent,))
                    continent_ids[continent] = cursor.fetchone()[0]

            # Insere localidades, evitando duplicações
            for continent, cities in locations.items():
                for city in cities:
                    cursor.execute("SELECT 1 FROM locations WHERE city_name = %s AND continent_id = %s;", (city, continent_ids[continent]))
                    if not cursor.fetchone():
                        cursor.execute("INSERT INTO locations (city_name, continent_id) VALUES (%s, %s);", (city, continent_ids[continent]))
        conn.commit()

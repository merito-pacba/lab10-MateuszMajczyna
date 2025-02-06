import pyodbc
import random

# Database connection settings (modify as needed)
DATABASE_CONFIG = {
    "server": "server-1563302063.database.windows.net",
    "database": "MediaDatabaseMateusz",
    "username": "MateuszMajczyna2000There",
    "password": "WhooptyDoo2000!!!",
    "driver": "{ODBC Driver 18 for SQL Server}",
}

# Media types
MEDIA_TYPES = ["games", "movies", "books", "tv_shows", "anime"]

# Status options
STATUSES = ["wishlist", "playing", "finished", "abandoned"]

# Sample names for each media type
SAMPLE_NAMES = {
    "games": ["Zelda", "Elden Ring", "Halo", "Minecraft", "Cyberpunk"],
    "movies": ["Inception", "Interstellar", "Avengers", "The Matrix", "Titanic"],
    "books": ["1984", "Dune", "Harry Potter", "Lord of the Rings", "The Hobbit"],
    "tv_shows": ["Breaking Bad", "Stranger Things", "The Office", "Game of Thrones", "Friends"],
    "anime": ["Naruto", "Attack on Titan", "One Piece", "Death Note", "Demon Slayer"]
}

def get_db_connection():
    """Establish a connection to the Azure SQL database."""
    conn_string = f"DRIVER={DATABASE_CONFIG['driver']};SERVER={DATABASE_CONFIG['server']};DATABASE={DATABASE_CONFIG['database']};UID={DATABASE_CONFIG['username']};PWD={DATABASE_CONFIG['password']}"
    return pyodbc.connect(conn_string)

def insert_sample_data():
    """Insert 20 random entries for each media type."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        for media_type in MEDIA_TYPES:
            for _ in range(20):
                name = random.choice(SAMPLE_NAMES[media_type]) + f" {random.randint(1, 100)}"
                status = random.choice(STATUSES)
                score = random.randint(0, 10)

                cursor.execute(
                    "INSERT INTO media (name, type, status, score) VALUES (?, ?, ?, ?)",
                    (name, media_type, status, score)
                )

        conn.commit()
        print("✅ 20 entries added for each media type!")
    
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        conn.close()

# Run the function to add sample data
insert_sample_data()

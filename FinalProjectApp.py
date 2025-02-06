from flask import Flask, render_template, request, redirect, url_for
import pyodbc

# Define connection variables
server = "server-1563302063.database.windows.net"
database = "MediaDatabaseMateusz"
username = "MateuszMajczyna2000There"
password = "WhooptyDoo2000!!!"
driver = "{ODBC Driver 18 for SQL Server}"

# Create connection string
conn_string = f"""
DRIVER={driver};
SERVER={server};
DATABASE={database};
UID={username};
PWD={password};
Encrypt=yes;
TrustServerCertificate=no;
Connection Timeout=30;
"""

try:
    # Establish connection
    conn = pyodbc.connect(conn_string)
    cursor = conn.cursor()
    
    cursor.execute("SELECT @@VERSION")
    row = cursor.fetchone()
    
    print(f"Connected successfully! SQL Server version: {row[0]}")
except Exception as e:
    print(f"Error connecting to database: {e}")

create_table_query = """
IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Media')
BEGIN
    CREATE TABLE Media (
        id INT IDENTITY(1,1) PRIMARY KEY,
        name NVARCHAR(255) NOT NULL,
        type NVARCHAR(100) NOT NULL,
        status NVARCHAR(50) NOT NULL,
        score FLOAT
    )
END
"""

cursor.execute(create_table_query)
conn.commit()
print("Table 'Media' created (if not exists).")


insert_query = "INSERT INTO Media (name, type, status, score) VALUES (?, ?, ?, ?)"

# Sample media data
media_data = [
    ("Inception", "Movie", "Watched", 9.0),
    ("Breaking Bad", "Movie", "Completed", 10.0),
    ("Attack on Titan", "Movie", "Ongoing", 8.5),
    ("Cyberpunk 2077", "Game", "Completed", 9.2)
]

# Insert multiple rows
# cursor.executemany(insert_query, media_data)
# conn.commit()
# print("Inserted sample media data successfully!")

cursor.execute("SELECT * FROM Media")
rows = cursor.fetchall()

print("\n📌 Media Entries in Database:")
for row in rows:
    print(f"ID: {row.id}, Name: {row.name}, Type: {row.type}, Status: {row.status}, Score: {row.score}")

cursor.close()
conn.close()
print("Connection closed.")


def get_media_by_type(media_type):
    # Create connection string
    conn_string = f"""
    DRIVER={driver};
    SERVER={server};
    DATABASE={database};
    UID={username};
    PWD={password};
    Encrypt=yes;
    TrustServerCertificate=no;
    Connection Timeout=30;
    """

    try:
        # Connect to the database
        conn = pyodbc.connect(conn_string)
        cursor = conn.cursor()

        # SQL query to select media by type
        query = "SELECT * FROM Media WHERE type = ?"
        
        # Execute query with parameter
        cursor.execute(query, (media_type,))
        
        # Fetch results
        rows = cursor.fetchall()

        # Print results
        if rows:
            print(f"\n📌 Media of type '{media_type}':")
            for row in rows:
                print(f"ID: {row.id}, Name: {row.name}, Status: {row.status}, Score: {row.score}")
        else:
            print(f"\nNo media found for type '{media_type}'.")

        # Close connection
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")


get_media_by_type("Book")  # Fetch all movies from the database


app = Flask(__name__)

# Database connection function
def get_db_connection():
    server = "server-1563302063.database.windows.net"
    database = "MediaDatabaseMateusz"
    username = "MateuszMajczyna2000There"
    password = "WhooptyDoo2000!!!"
    driver = "{ODBC Driver 18 for SQL Server}"

    conn_string = f"""
    DRIVER={driver};
    SERVER={server};
    DATABASE={database};
    UID={username};
    PWD={password};
    Encrypt=yes;
    TrustServerCertificate=no;
    Connection Timeout=30;
    """
    return pyodbc.connect(conn_string)

# @app.route("/")
# def hello_world():
#     return render_template("MainPage.html")

# @app.route("/games")
# def gamesTemplate():
#     return render_template("GamesPage.html")

# @app.route("/movies")
# def moviesTemplate():
#     return render_template("MoviesPage.html")

# @app.route("/books")
# def booksTemplate():
#     return render_template("BooksPage.html")

# @app.route("/music")
# def musicTemplate():
#     return render_template("MusicPage.html")

# Route to display media of a given type
@app.route('/media/<media_type>', methods=['GET'])
def display_media(media_type):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get filter and sort options from request parameters
        status_filter = request.args.get('status', default=None)
        sort_by = request.args.get('sort', default='name')  # Default sorting by name
        order = request.args.get('order', default='asc')  # Default ascending order

        # Build SQL query
        query = "SELECT id, name, status, score FROM Media WHERE type = ?"
        params = [media_type]

        if status_filter and status_filter != "all":
            query += " AND status = ?"
            params.append(status_filter)

        # Sorting options
        valid_sort_columns = ["name", "score", "status"]
        if sort_by in valid_sort_columns:
            query += f" ORDER BY {sort_by} {order.upper()}"

        cursor.execute(query, params)
        media_entries = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template(
            "media.html",
            media_entries=media_entries,
            media_type=media_type,
            status_filter=status_filter,
            sort_by=sort_by,
            order=order
        )

    except Exception as e:
        return f"Error: {e}"

    
# Route to display media type selection form (this will be the default page)
@app.route('/', methods=['GET', 'POST'])
def select_media_type():
    if request.method == 'POST':
        media_type = request.form['media_type']
        return redirect(url_for('display_media', media_type=media_type))
    return render_template('select_media_type.html')

# Route to display form for adding a new media entry
@app.route('/add_media/<media_type>', methods=['GET', 'POST'])
def add_media(media_type):
    if request.method == 'POST':
        name = request.form['name']
        status = request.form['status']
        score = request.form['score']

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Insert the new media entry into the database
            query = "INSERT INTO Media (name, type, status, score) VALUES (?, ?, ?, ?)"
            cursor.execute(query, (name, media_type, status, score))
            conn.commit()

            cursor.close()
            conn.close()

            return redirect(url_for('display_media', media_type=media_type))  # Redirect back to the media list page
        except Exception as e:
            return f"Error: {e}"

    return render_template('add_media.html', media_type=media_type)

# Route to edit a media entry
@app.route('/edit_media/<int:id>', methods=['GET', 'POST'])
def edit_media(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch the media entry by its ID
        query = "SELECT id, name, status, score, type FROM Media WHERE id = ?"
        cursor.execute(query, (id,))
        media_entry = cursor.fetchone()

        if not media_entry:
            return f"Error: Media entry with ID {id} not found."

        if request.method == 'POST':
            name = request.form['name']
            status = request.form['status']
            score = request.form['score']

            # Update the media entry in the database
            update_query = "UPDATE Media SET name = ?, status = ?, score = ? WHERE id = ?"
            cursor.execute(update_query, (name, status, score, id))
            conn.commit()

            cursor.close()
            conn.close()

            return redirect(url_for('display_media', media_type=media_entry[4]))  # Redirect back to the media list page

        cursor.close()
        conn.close()

        return render_template('edit_media.html', media_entry=media_entry)

    except Exception as e:
        return f"Error: {e}"

# Route to delete a media entry
@app.route('/delete_media/<int:id>', methods=['POST'])
def delete_media(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch the media type before deleting to redirect correctly
        cursor.execute("SELECT type FROM Media WHERE id = ?", (id,))
        media_entry = cursor.fetchone()

        if not media_entry:
            return "Error: Media entry not found."

        media_type = media_entry[0]

        # Delete the media entry
        delete_query = "DELETE FROM Media WHERE id = ?"
        cursor.execute(delete_query, (id,))
        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for('display_media', media_type=media_type))  # Redirect to the list page
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    app.run(debug=True)
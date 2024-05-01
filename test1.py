#this function for snake game
import psycopg2

# Database connection parameters
DB_NAME = "database_name"
DB_USER = "database_user"
DB_PASSWORD = "database_password"
DB_HOST = "database_host"
DB_PORT = "database_port"

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Function to register a new user
def register_user(username):
    try:
        cursor.execute("INSERT INTO user (username) VALUES (%s) RETURNING id", (username,))
        user_id = cursor.fetchone()[0]
        conn.commit()
        print("User registered successfully with ID:", user_id)
        return user_id
    except psycopg2.IntegrityError:
        conn.rollback()
        print("Username already exists. Please choose another username.")
        return None

# Function to fetch user information
def get_user_info(username):
    cursor.execute("SELECT id FROM user WHERE username = %s", (username,))
    row = cursor.fetchone()
    if row:
        return row[0]
    else:
        return None

# Function to save game state and score
def save_game_state(user_id, score, level):
    try:
        cursor.execute("INSERT INTO user_score (user_id, score, level) VALUES (%s, %s, %s)", (user_id, score, level))
        conn.commit()
        print("Game state saved successfully")
    except psycopg2.Error as e:
        conn.rollback()
        print("Error:", e)

# Function to retrieve user scores
def get_user_scores(user_id):
    cursor.execute("SELECT score, level FROM user_score WHERE user_id = %s ORDER BY level", (user_id,))
    rows = cursor.fetchall()
    if rows:
        print("User scores:")
        for row in rows:
            print("Level:", row[1], "- Score:", row[0])
    else:
        print("No scores found for the user")

# Close the cursor and connection
cursor.close()
conn.close()

import csv

with open("names.csv", mode="w") as csvfile:
    fieldnames = ["first_name", "last_name"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({"first_name": "weight", "last_name": "height"})
    writer.writerow({"first_name": "weight", "last_name": "height"})
    writer.writerow({"first_name": "weight", "last_name": "height"})
    writer.writerow({"first_name": "weight", "last_name": "height"})
    writer.writerow({"first_name": "weight", "last_name": "height"})
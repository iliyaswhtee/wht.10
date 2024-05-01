import psycopg2
import csv
from psycopg2 import sql

# Database connection parameters
DB_NAME = "database_name"
DB_USER = "database_user"
DB_PASSWORD = "database_password"
DB_HOST = "database_host"
DB_PORT = "5432"

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

# Function to create PhoneBook table
def create_phonebook_table():
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            phone VARCHAR(15) NOT NULL
        )
    '''
    cursor.execute(create_table_query)
    conn.commit()
    print("PhoneBook table created successfully")

# Function to insert data from a CSV file
def insert_from_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            username, phone = row
            insert_query = sql.SQL("INSERT INTO phonebook (username, phone) VALUES (%s, %s)")
            cursor.execute(insert_query, (username, phone))
    conn.commit()
    print("Data inserted from CSV successfully")

# Function to insert data from console
def insert_from_console():
    username = input("Enter username: ")
    phone = input("Enter phone number: ")
    insert_query = sql.SQL("INSERT INTO phonebook (username, phone) VALUES (%s, %s)")
    cursor.execute(insert_query, (username, phone))
    conn.commit()
    print("Data inserted from console successfully")

# Function to update data in the table
def update_data(username, new_phone):
    update_query = sql.SQL("UPDATE phonebook SET phone = %s WHERE username = %s")
    cursor.execute(update_query, (new_phone, username))
    conn.commit()
    print("Data updated successfully")

# Function to query data from the table with filters
def query_data():
    query = "SELECT * FROM phonebook"
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)

# Function to delete data from the table by username or phone
def delete_data(criteria, value):
    delete_query = sql.SQL("DELETE FROM phonebook WHERE {} = %s").format(sql.Identifier(criteria))
    cursor.execute(delete_query, (value,))
    conn.commit()
    print("Data deleted successfully")

if __name__ == "__main__":
    create_phonebook_table()

    # Insert data from CSV file
    insert_from_csv("phonebook_data.csv")

    # Insert data from console
    insert_from_console()

    # Update data
    update_data("username_to_update", "new_phone_number")

    # Query data
    query_data()

    # Delete data
    delete_data("username", "username_to_delete")

# Close the cursor and connection
cursor.close()
conn.close()


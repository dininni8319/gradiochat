import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv()

db = os.getenv("DATABASE_NAME")
username = os.getenv("DATABASE_USER")
password = os.getenv("DATABASE_PASSWORD")
host = os.getenv("DATABASE_HOST")
port = os.getenv("DATABASE_PORT")

# Function to create a new connection
def get_connection():
    try:
        connection = psycopg2.connect(
            database=db,
            user=username,
            password=password,
            host=host,
            port=port
        )
        print("Connection created successfully")
        return connection
    except Exception as e:
        print(f"Error getting connection: {e}")

# Function to close the connection
def close_connection(connection):
    if connection:
        connection.close()
        print("Connection closed")

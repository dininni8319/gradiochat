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
# Function to check if a token is valid for a specific user
def is_token_valid(user_id, token):
    connection = None
    try:
        connection = get_connection()
        if connection is None:
            return False

        cursor = connection.cursor()
        
        # Define the query to check if the token exists for the specified user
        query = sql.SQL("SELECT COUNT(*) FROM user_usertoken WHERE token = %s AND user_id = %s")
        
        # Execute the query
        cursor.execute(query, (token, user_id))
        
        # Fetch the result
        result = cursor.fetchone()
        
        # Check if token exists for the user
        if result[0] > 0:
            print("Token is valid")
            return True
        else:
            print("Token is invalid")
            return False
        
    except Exception as e:
        print(f"Error checking token: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        close_connection(connection)

# Function to close the connection
def close_connection(connection):
    if connection:
        connection.close()
        print("Connection closed")

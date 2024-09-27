import os
import MySQLdb
from dotenv import load_dotenv

load_dotenv()

# Fetching database connection parameters from environment variables
db_name = os.getenv("DATABASE_NAME")
username = os.getenv("DATABASE_USER")
password = os.getenv("DATABASE_PASSWORD")
host = os.getenv("DATABASE_HOST")
port = os.getenv("DATABASE_PORT")  # MySQL typically defaults to port 3306

# Function to create a new connection
def get_connection():
    try:
        connection = MySQLdb.connect(
            host=host, 
            user=username, 
            passwd=password, 
            db=db_name,
            port=int(port) if port else 3306  # Use the specified port or default to 3306
        )
        print("Database connection successful!")
        return connection
    except MySQLdb.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Function to check if a token is valid for a specific user
def is_token_valid(user_id, token):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        if connection is None:
            return False

        cursor = connection.cursor()
        
        # Define the query to check if the token exists for the specified user
        query = "SELECT COUNT(*) FROM user_usertoken WHERE token = %s AND user_id = %s"
        
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

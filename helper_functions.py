import re
from datetime import datetime

instructions = ""
# Path to store assistant ID
assistant_id_file = 'assistant_id.txt'

# Function to check if the assistant already exists and return its ID
def get_value_from_file(target_key, filename = "assistant_id.txt"):
    try:
        # Open and read the file
        with open(filename, 'r') as file:
            for line in file:
                # Strip any extra whitespace and split the line by '='
                key, value = line.strip().split('=', 1)
                # Check if the key matches the target_key
                if key == target_key:
                    return value
        return None  # Key not found
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Function to save the assistant ID to a file
def save_assistant_id(file_path, assistant_id):
    data = read_data_from_file()
    with open(file_path, 'w') as file:
        file.write(assistant_id)

def read_data_from_file(filename = "data.txt"):
    """
    Reads key-value pairs from a file and returns them as a dictionary.

    :param filename: The name of the file to read from.
    :return: A dictionary containing the key-value pairs.
    """
    data = {}
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                key, value = line.strip().split('=')
                data[key] = value
    except FileNotFoundError:
        print(f"File {filename} not found.")
    except ValueError:
        print(f"Invalid format in {filename}. Each line should be key=value.")
    
    return data


def process_data(data):
    """
    Process the raw data to clean responses, format dates, and return structured results.
    
    Args:
        data (list): A list of strings where each string contains a query, date, and response.
    
    Returns:
        list: A list of lists where each sublist contains the query, formatted date, and cleaned response.
    """
    processed_data = []
    
    def clean_response(response):
        # Remove unwanted special characters from the response
        return re.sub(r'[{"(,\\)}]', '', response).strip()

    def format_date(date_str):
        # If date_str is already a datetime object, format it directly
        if isinstance(date_str, datetime):
            return date_str.strftime("%d.%m.%Y")
        else:
            # If it's a string, convert to datetime and then format
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            return date_obj.strftime("%d.%m.%Y")

    # Iterate through the data and process each record
    
    # Iterate through the data and process each record
    for record in data:
        # Unpack the tuple into query, date, and response
        query, date_str, response = record

        # Clean the response and format the date
        cleaned_response = clean_response(response)
        formatted_date = format_date(date_str)

        # Append the processed result to the list
        processed_data.append([query, formatted_date, cleaned_response])

    return processed_data



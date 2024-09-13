import os

# Function to check if the assistant already exists and return its ID
def get_existing_assistant_id(file_path):
  if os.path.exists(file_path):
    with open(file_path, 'r') as file:
        assistant_id = file.read().strip()
        return assistant_id
  return None
# Function to save the assistant ID to a file
def save_assistant_id(file_path, assistant_id):
    with open(file_path, 'w') as file:
        file.write(assistant_id)


import os

instructions = "Devi rispondere solo in Italiano. Se ti scrivo in altre lingue digli che non puoi scrivere in altre lingue. Inoltre devi rispondere a domande che sono relative alla finanza. Tipo borsa, azioni e politica aziendale. Se qualcuno ti chiede come ti chiami gli rispondi che mi chiamo Gaia. Non rispondere a domande che non sono relative all'argomento."
# Path to store assistant ID
assistant_id_file = 'assistant_id.txt'

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


import os
import time
from openai import OpenAI
from dotenv import load_dotenv
from helper_functions import get_value_from_file, read_data_from_file, instructions, assistant_id_file

load_dotenv() # Load env file

# OpenAI API initialization
api_key = os.getenv("OPENAI")  # Ensure your API key is set correctly
client = OpenAI(api_key=api_key)

# Function to initialize the assistant (create or retrieve existing)
def initialize_assistant():
    user_data = read_data_from_file()
    existing_assistant_id = get_value_from_file(user_data["assistant"])
    print("🚀 ~ existing_assistant_id:", existing_assistant_id)

    if existing_assistant_id:
        # Retrieve existing assistant
        return client.beta.assistants.retrieve(existing_assistant_id)
    else:
        # Create a new assistant if one doesn't exist
        assistant = client.beta.assistants.create(
            instructions=instructions,
            name="Gaja",
            tools=[{"type": "file_search"}],
            model="gpt-4o-mini",
        )
        # Save the new assistant ID for future use
        # save_assistant_id(assistant_id_file, assistant.id)
        return assistant

# Function to create a new thread and send the user's query and the file content
def create_thread_send_file_and_query(assistant, query, file_path):
    try:
        # Create a new conversation thread
        thread = client.beta.threads.create()
        print("🚀 ~ thread:", thread)
      
        # Step 1: Upload a File with an "assistants" purpose
        my_file = client.files.create(
            file=open(file_path, "rb"),
            purpose='assistants'
        )

        print(f"This is the file object: {my_file} \n")

        # Add file content to the thread
        my_thread_message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=query or "Quale è il contenuto del file!",
            attachments=[{
                "file_id": my_file.id,
                "tools": [{"type": "code_interpreter"}]
            }]
        )

        print(f"This is my thread object: {my_thread_message} \n")

    
        # Run the assistant on the thread
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
            instructions=instructions,
        )

        print(f"This is the run object: {run} \n")

        return thread, run

    except Exception as e:
        return [("Error", f"An error occurred: {e}")]

# Function to create a new thread and send the user's query
def create_thread_and_send_query(assistant, query):
    try:
        # Create a new conversation thread
        thread = client.beta.threads.create()
       
        # Add user query to the thread
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=query
        )

        # Run the assistant on the thread
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
            instructions=instructions,
        )

        return thread, run

    except Exception as e:
        return [("Error", f"An error occurred: {e}")]


# Function to retrieve and format the assistant's response
def retrieve_and_format_messages(thread, run):
    try:
        while True:
            time.sleep(1)
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            # If the run is complete, retrieve the messages
            if run_status.status == 'completed':
                messages = client.beta.threads.messages.list(
                    thread_id=thread.id,
                    run_id=run.id
                )
                formatted_messages = []
                user_message = None
                # Process and format the conversation messages
                for msg in messages.data:
                    role = msg.role
                    content = msg.content[0].text.value
                    if role == "user":
                        user_message = content
                    elif role == "assistant":
                        assistant_response = content
                        formatted_messages.append((user_message, assistant_response))
                return formatted_messages

            elif run_status.status == 'failed':
                return [("Error", "The assistant encountered an error.")]

    except Exception as e:
        return [("Error", f"An error occurred: {e}")]

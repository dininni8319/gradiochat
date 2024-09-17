from openai import OpenAI
from dotenv import load_dotenv
from requests_made import check_and_update_requests
from helper_functions import get_existing_assistant_id, save_assistant_id, instructions, assistant_id_file
import os
import time

# Load environment variables
load_dotenv()

# OpenAI API initialization
api_key = os.getenv("OPENAI")  # Ensure your API key is set correctly
client = OpenAI(api_key=api_key)

# Function to initialize the assistant (create or retrieve existing)
def initialize_assistant():
    existing_assistant_id = get_existing_assistant_id(assistant_id_file)

    if existing_assistant_id:
        # Retrieve existing assistant
        return client.beta.assistants.retrieve(existing_assistant_id)
    else:
        # Create a new assistant if one doesn't exist
        assistant = client.beta.assistants.create(
            instructions=instructions,
            name="Gaja",
            # tools=[{"type": "code_interpreter"}],
            model="gpt-4o",
        )
        # Save the new assistant ID for future use
        save_assistant_id(assistant_id_file, assistant.id)
        # print("🚀 ~ Assistant ID saved:", assistant.id)
        return assistant

# Function to create a new thread and send the user's query
def create_thread_and_send_query(assistant, query):
    try:
        # Create a new conversation thread
        thread = client.beta.threads.create()
     
        # if user_id:
        #     check_and_update_requests(user_id)
        # Add user message to the thread
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
            max_completion_tokens=150
        )

        return thread, run

    except Exception as e:
        return [("Error", f"An error occurred: {e}")]

# Function to retrieve and format the assistant's response
def retrieve_and_format_messages(thread, run):
    try:
        while True:
            time.sleep(5)
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

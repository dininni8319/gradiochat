
from openai import OpenAI
import gradio as gr
from dotenv import load_dotenv
import os
import time
from assistent import get_existing_assistant_id, save_assistant_id

# Load environment variables
load_dotenv()

api_key = os.getenv("OPENAI")  # Ensure your API key is set correctly
client = OpenAI(api_key=api_key)

# Path to the file where the assistant ID will be stored
assistant_id_file = 'assistant_id.txt'

# Check if the assistant already exists
existing_assistant_id = get_existing_assistant_id(assistant_id_file)

if existing_assistant_id:
    # If the assistant exists, retrieve it
    assistant = client.beta.assistants.retrieve(existing_assistant_id)
else:
    # If the assistant does not exist, create it
    assistant = client.beta.assistants.create(
        instructions="Ciao sono Gaja. Come posso aiutarti?",
        name="Gaja",
        tools=[{"type": "code_interpreter"}],
        model="gpt-4o",
    )
    # Save the new assistant ID for future reference
    save_assistant_id(assistant_id_file, assistant.id)

# Function to handle the Gradio interface interaction
def handle_query(query):
    try:
        # Create a new thread
        thread = client.beta.threads.create()
        
        # Add a message to the thread
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=query
        )
        
        # Run the assistant
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
            instructions="Please introduce yourself to the user."
        )
        
        while True:
            # Check the run status
            time.sleep(5)
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            print("🚀 ~ run_status:", run_status)
            user_message = None
            if run_status.status == 'completed':
                # Retrieve and format messages from the thread
                messages = client.beta.threads.messages.list(
                    thread_id=thread.id
                ) 
                formatted_messages = []
                for msg in messages.data:
                    role = msg.role
                    content = msg.content[0].text.value
                    # Format messages to tuples of (user_message, assistant_response)
                    if role == "user":
                        user_message = content
                    elif role == "assistant":
                        assistant_response = content
                        formatted_messages.append((user_message, assistant_response))
                
                return formatted_messages

            elif run_status.status == 'failed':
                return [("Error", "The assistant encountered an error.")]
            else:
                continue
    
    except Exception as e:
        return [("Error", f"An error occurred: {e}")]


with gr.Blocks(fill_height=True) as demo:
    gr.Markdown("""<h1><center>Assistente Virtuale</center></h1>""") 
    chatbot = gr.Chatbot(
        elem_id="chatbot",
        bubble_full_width=False,
        scale=1
    )  # Gradio chatbot
    
    chat_input = gr.Textbox(
        interactive=True,
        placeholder="Inserisci un messaggio o carica un file...",
        show_label=False
    )
    
    # Submit button for the handle_query function
    chat_input.submit(handle_query, [chat_input], chatbot)

# Launch the Gradio demo
demo.launch(share=True)

import multiprocessing
import gradio as gr
from openai_assistent import initialize_assistant, create_thread_and_send_query, create_thread_send_file_and_query, retrieve_and_format_messages
from flask_app import run_flask
from helper_functions import read_data_from_file, process_data
from requests_made import check_and_update_requests, add_chat_conversation, get_chat_conversations

def display_past_conversations(user_id):
    conversations = process_data(get_chat_conversations(user_id))
    if not conversations:
        return []
    # Convert to a format suitable for gr.Dataframe (list of dicts or tuples)
    return conversations

# Function to process the uploaded file and send content to OpenAI
def handle_file_upload_and_query(file, query, history):
    if not file:
        return history + [[None, "No file uploaded!"]]
    try:
        # Send the file content to the assistant
        assistant = initialize_assistant()
        thread, run = create_thread_send_file_and_query(assistant, query,file.name)
        formatted_messages = retrieve_and_format_messages(thread, run)

        # Append messages to the chat history
        for user_msg, assistant_response in formatted_messages:
            history.append([user_msg, assistant_response])
        
        return history
    except Exception as e:
        return history + [("Error", f"An error occurred: {e} ")]


# Main function to handle the user query
def handle_assistant_query(query, history):
    # Read data from a plain text file
    data = read_data_from_file()

    if not query:
        return history + [[None, "Input non valido!"]]

    if not data['user_id'] or not data['token']:
        return history + [[None, "User ID or Token is missing"]]

    # Check if the user is over the request limit
    if not check_and_update_requests(data['user_id']):
        return history + [[None, "Mi dispiace ma hai raggiunto il numero massimo di richieste per questo periodo"]]
    
    try:
        # Initialize the assistant
        assistant = initialize_assistant()

        # Create a thread and send the user's query
        thread, run = create_thread_and_send_query(assistant, query)

        # Retrieve and format the messages from the assistant
        formatted_messages = retrieve_and_format_messages(thread, run)
        
        # Saving the conversation in the DB
        add_chat_conversation(data['user_id'], query, formatted_messages)
        
        # Append the new messages to the history
        for user_msg, assistant_response in formatted_messages:
            history.append([user_msg, assistant_response])

        return history # Return updated history to update the chat

    except Exception as e:
        return history + [[None, f"An error occurred: {e}"]]

# Global data variable
data = None

def update_interface():
    global data
    if data:
        assistant_name = data["assistant"].capitalize()
        return (f"<h1><center style='color: orange;'> Assistente Virtuale</center></h1>",
                [[None, f"Ciao sono il tuo assistente virtuale. Come posso aiutarti?"]])
    return ("<h1><center>Assistente Virtuale</center></h1>", [[None, "Ciao! Come posso aiutarti?"]])

# Gradio interface setup
def create_gradio_interface():
    with gr.Blocks(fill_height=True, theme=gr.themes.Monochrome()) as demo:
        global data
        data = read_data_from_file()
        # Markdown for assistant name
        assistant_markdown = gr.Markdown(update_interface()[0])

        # Chatbot and user input elements
        chatbot = gr.Chatbot(value=update_interface()[1], elem_id="Gaja", bubble_full_width=False, scale=1)

        user_input = gr.Textbox(
            interactive=True,
            placeholder="Inserisci un messaggio...",
            show_label=False
        )

        # Add a Dataframe component to list all past conversations
        if data and data['user_id']:
            conversations = display_past_conversations(data['user_id'])
        else:
            conversations = []
        with gr.Row():
             # Buttons for handling inputs
            query_submit = gr.Button("Send Query")
            file_submit = gr.Button("Upload and Query")
    
        # File upload input for CSV/Excel files
        file_upload = gr.File(label="Upload CSV or Excel", file_types=["csv", "xlsx"])

        # Bind buttons to functions
        query_submit.click(handle_assistant_query, [user_input, chatbot], chatbot)
        file_submit.click(handle_file_upload_and_query, [file_upload, user_input, chatbot], chatbot)
        
        conversations_df = gr.Dataframe(
            headers=["Richiesta", "Data", "Risposta"],
            type="pandas",  # Use "pandas" if you want DataFrame-like output
            value=conversations
        )

    return demo

# Function to run Gradio
def run_gradio():
    demo = create_gradio_interface()
    demo.launch(share=False, server_port=7860)

if __name__ == "__main__":
    # Start Flask in a separate process
    flask_process = multiprocessing.Process(target=run_flask)
    flask_process.start()

    # Run Gradio for the chat interface
    run_gradio()

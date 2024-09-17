import multiprocessing
import gradio as gr
from openai_assistent import  initialize_assistant, create_thread_and_send_query, retrieve_and_format_messages
from flask_app import run_flask
from helper_functions import read_data_from_file
from requests_made import check_and_update_requests

# Main function to handle the user query
def handle_query(query):
    # Read data from a plain text file
    data = read_data_from_file()
   
    if not query:
        return [("Error", "Input non valido!")]
    
    if not data['user_id']or not data['token']:
        return [("Error", "User ID or Token is missing")]

    # checks if you are over the limit
    if not check_and_update_requests(data['user_id']):
        return [("Error", "Mi dispiace ma hai raggiunto il numbero massimo di richieste per questo periodo")]

    # Initialize the assistant
    assistant = initialize_assistant()

    # Create a thread and send the user's query
    thread, run = create_thread_and_send_query(assistant, query)
    # Retrieve and format the messages from the assistant
    return retrieve_and_format_messages(thread, run)

# Gradio interface setup
def create_gradio_interface():
    with gr.Blocks(fill_height=True) as demo:
        gr.Markdown("<h1><center> Gaja. Assistente Virtuale</center></h1>")

        # Chatbot and user input elements
        chatbot = gr.Chatbot(
            value=[[None, "Ciao sono Gaja. Il tuo assistente virtuale. Come posso aiutarti?"]],
            elem_id="Gaja",
            bubble_full_width=False,
            scale=1
        )

        chat_input = gr.Textbox(
            interactive=True,
            placeholder="Inserisci un messaggio o carica un file...",
            show_label=False
        )

        # Buttons for clearing and submitting input
        with gr.Row():
            submit = gr.Button("Invia")
            clear = gr.ClearButton([chatbot, chat_input])
        
        # Bind buttons to functions
        submit.click(handle_query, [chat_input], chatbot)
        chat_input.submit(handle_query, [chat_input], chatbot)

    return demo

# Function to run Gradio
def run_gradio():
    demo = create_gradio_interface()
    demo.launch(share=False, server_port=7860)

if __name__ == "__main__":
    # Start Flask in a separate process
    flask_process = multiprocessing.Process(target=run_flask)
    flask_process.start()
      # Send the query and check the request tracking
    # Ensure the token and user_id are valid before running Gradio
    run_gradio()
   
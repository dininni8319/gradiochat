import multiprocessing
import gradio as gr
from main import handle_query
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={r"/token": {"origins": "*"}})

token = None  # Store token globally

# Route to receive token
@cross_origin(origin='*')
@app.route('/token', methods=['POST'])
def receive_token():
    global token
    data = request.get_json()
    token = data.get('token')
    print(f"Received token: {token}")
    return jsonify({'status': 'Token received'})

# Function to run Flask
def run_flask():
    app.run(host='0.0.0.0', port=7861, threaded=True)  # Disable reloader and run Flask without debug mode

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
    demo.launch(share=False, server_port=7860)  # Run Gradio on port 7860

if __name__ == "__main__":
    # Run Flask in a separate process
    flask_process = multiprocessing.Process(target=run_flask)
    flask_process.start()

    # Run Gradio in the main process
    run_gradio()

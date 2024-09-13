import gradio as gr
from main import handle_query
# Gradio interface setup
def create_gradio_interface():
    with gr.Blocks(fill_height=True) as demo:
        gr.Markdown("<h1><center> Gaja. Assistente Virtuale</center></h1>")

        # Chatbot and user input elements
        chatbot = gr.Chatbot(elem_id="chatbot", bubble_full_width=False, scale=1)
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

# Launch the Gradio demo
if __name__ == "__main__":
    demo = create_gradio_interface()
    demo.launch(share=True)

from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import CORS
from db import is_token_valid
from gradio_ui import create_gradio_interface

app = Flask(__name__)
CORS(app, resources={r"/token": {"origins": ["https://chat-w3innovation.pythonanywhere.com", "https://w3Innovation.pythonanywhere.com"]}})


# Route to receive token
@app.route('/token', methods=['POST'])
def receive_token():
    data = request.get_json()
    if not data:
        return jsonify({'status': 'Error', 'message': 'No JSON data received'}), 400  # Bad Request

    token = data.get('token')
    user_id = data.get('user_id')
    assistant = data.get('assistant')

    if not token or not user_id or not assistant:
        return jsonify({'status': 'Error', 'message': 'Missing token, user_id, or assistant'}), 400

    # Write data to a plain text file (ensure file is secure)
    with open("data.txt", 'w') as file:
        file.write(f"user_id={user_id}\n")
        file.write(f"token={token}\n")
        file.write(f"assistant={assistant}\n")

    if not is_token_valid(user_id, token):
        return redirect(url_for('login'))  # Use `url_for` for better URL management

    return jsonify({'status': 'Success', 'message': 'Token received'})


# Serve Gradio interface on the root route
@app.route("/", methods=["GET", "POST"])
def run_gradio():
    demo = create_gradio_interface()
    return demo.launch(
        share=False, 
        inline=True, 
        prevent_thread_lock=True, 
        server_name="127.0.0.1",
        # show_error=False,
        # show_api=False
    )  # Prevent thread lock


if __name__ == "__main__":
    app.run()

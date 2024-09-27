from flask import Flask, request, jsonify, redirect, url_for
from flask_cors import CORS
from db import is_token_valid


app = Flask(__name__)
CORS(app, resources={r"/token": {"origins": ["https://chat-w3innovation.pythonanywhere.com/", "w3Innovation.pythonanywhere.com"]}})

# Route to receive token
@app.route('/token', methods=['POST'])
def receive_token():
    data = request.get_json()
    token = data.get('token')
    user_id = data.get('user_id')
    assistant = data.get('assistant')

    # Write data to a plain text file
    with open("data.txt", 'w') as file:
        file.write(f"user_id={user_id}\n")
        file.write(f"token={token}\n")
        file.write(f"assistant={assistant}\n")

    if not token or not user_id or not is_token_valid(user_id, token):
        return redirect(url_for('login'))  # Use `url_for` for better URL management
    
    return jsonify({'status': 'Success', 'message': 'Token received'})

# Function to run Flask
def run_flask():
    app.run(host='0.0.0.0', port=5000, threaded=True)

from flask import Flask, render_template_string
from flask_cors import CORS
# from db import is_token_valid
from gradio_ui import create_gradio_interface

app = Flask(__name__)

CORS(app)


@app.route("/")
def index():
    # Create the Gradio app and pass it to the template
    gradio_app_html = create_gradio_interface()
    
    # Flask will render this template with the Gradio Blocks app embedded
    template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Gradio Blocks in Flask</title>
    </head>
    <body>
        <h1>Gradio Blocks with Flask</h1>
        <div>
            {{ gradio_app|safe }}
        </div>
    </body>
    </html>
    """
    return render_template_string(template, gradio_app=gradio_app_html)

if __name__ == "__main__":
    app.run()

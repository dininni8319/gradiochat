from openai import OpenAI
import gradio as gr
from transformers import pipeline
import numpy as np

# Set up your OpenAI API key
openai_key = 'sk-OPBuCwqWRlY76mFOiP2sfkCJpbWEVCBoRkGD3i9WU6T3BlbkFJRkyMunEvtK3ElYElJk_z0wn4vs-CWfHaaigQRUIQQA'

# Load a pre-trained speech-to-text model
# device = 0  # Change to -1 if you want to use CPU
# stt_pipeline = pipeline(
#     "automatic-speech-recognition",
#     framework="pt", device=device)

# def speech_to_text(audio):
#     sampling_rate, audio_data = audio
#     audio_data = np.array(audio_data, dtype=np.float32)
    
#     if audio_data.ndim > 1:
#         audio_data = np.mean(audio_data, axis=1)  # Convert stereo to mono
    
#     print("Audio shape:", audio_data.shape)
    
#     try:
#         text = stt_pipeline(audio_data)["text"]
#         print("Transcribed text:", text)
#         return text
#     except Exception as e:
#         print(f"Error in speech-to-text conversion: {e}")
#         return "Speech-to-text conversion failed."

def ask_chatgpt(question, document_text="Sample text from PDF."):
    client = OpenAI(openai_key)
   
    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": question},
            {"role": "assistant", "content": document_text},
        ],
        model="gpt-4o-mini",
    )
    return response.choices[0].message.content
    
# def gradio_interface(question, audio):
#     # if audio is not None:
#     #     # transcribed_text = speech_to_text(audio)
#     #     # if transcribed_text and transcribed_text != "Speech-to-text conversion failed.":
#     #     #     response = ask_chatgpt(transcribed_text)
#     #     #     return f"Transcribed: {transcribed_text}", response
#     #     # else:
#     #     #     return "Audio transcription failed.", "No response due to transcription failure."
#     # else:
#     response = ask_chatgpt(question)
#     return f"Text Input: {question}", response

# Set up the Gradio interface
# interface = gr.Interface(
#     fn=gradio_interface,
#     inputs=[
#         gr.Textbox(
#             placeholder="Salve! Come posso assisterti?",
#             label="Inserisci una domanda",
#             lines=2,
#             elem_id="question_input"
#         ),
#         # gr.Audio(sources=["microphone", 'upload'], type="numpy")  # Capture audio from microphone
#     ],
#     outputs=[
#         # gr.Textbox(label="Testo Trascritto"),
#         gr.Textbox(label="Risposta GPT")
#     ],
#     title="Chat con GPT",
#     description="Inserisci una domanda o parla al microfono per ottenere una risposta.",
#     theme="default"
# )
import requests
# import json
# import os

openai_api_key = "sk-OPBuCwqWRlY76mFOiP2sfkCJpbWEVCBoRkGD3i9WU6T3BlbkFJRkyMunEvtK3ElYElJk_z0wn4vs-CWfHaaigQRUIQQA" # put yout api key here
if openai_api_key is None:
    raise ValueError("OpenAI API key is not set in environment variables.")

url = "https://api.openai.com/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai_api_key}"
}

data = {
    "model": "gpt-3.5-turbo",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "Hello!"
        }
    ]
}

response = requests.post(url, headers=headers, json=data)

# Check if the request was successful
if response.status_code == 200:
    print("Response from OpenAI:", response.json())
    print('\n')
    print(response.json()['choices'][0]['message']['content'])
else:
    print("Error:", response.status_code, response.text)
# interface.launch(share=True)

def gradio_interface(text_input):
    response = ask_chatgpt(text_input)
    return response

# Set up the Gradio interface
interface = gr.Interface(
    fn=gradio_interface,
    inputs=gr.Textbox(
        placeholder="Type your question here...",
        label="Enter your question",
        lines=2
    ),
    outputs=gr.Textbox(
        label="ChatGPT Response"
    ),
    title="Chat with GPT",
    description="Type a question or prompt to get a response from GPT-3."
)

interface.launch(share=True)
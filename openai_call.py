import requests
import os
from dotenv import load_dotenv


# Set up your OpenAI API key
def call_openai(message): 
    load_dotenv()
    openai_key = os.getenv("OPENAI")
    if openai_key is None:
        raise ValueError("OpenAI API key is not set in environment variables.")
    else:
        url = "https://api.openai.com/v1/chat/completions"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai_key}"
        }

        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": message or "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": "Hello!"
                }
            ]
        }
  
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            print("Response from OpenAI:", response.json())
            print('\n')
            print(response.json()['choices'][0]['message']['content'])
            return response.json()['choices'][0]['message']['content']
        else:
            print("Error:", response.status_code, response.text)
    

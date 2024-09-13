# import gradio as gr
# from transformers import pipeline
# import numpy as np
# from openai_call import call_openai
 

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
    
# def gradio_interface(question, audio):
#     if audio is not None:
#         transcribed_text = speech_to_text(audio)
#         if transcribed_text and transcribed_text != "Speech-to-text conversion failed.":
#             response = call_openai(transcribed_text)
#             return f"Transcribed: {transcribed_text}", response
#         else:
#             return "Audio transcription failed.", "No response due to transcription failure."
#     if question:
#         response = call_openai(question)
#         return response

# def gradio_interface(question): 
#   if question:
#     return "Hello" + question
  
# # Set up the Gradio interface
# interface = gr.ChatInterface(
#   fn=gradio_interface,
#   title="Chat Interface",
#   description="This is a Chatbot Interface",

# )
# interface.launch(share=True)
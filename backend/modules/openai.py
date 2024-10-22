import openai
from openai import OpenAI
import os
import json
import requests  # Add this import to use the requests library
from loguru import logger

openai.api_key = os.getenv("OPENAI_API_KEY")  # Set your OpenAI API key from environment variable
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def openai_call(prompt) -> dict:
            # Call the OpenAI API with the provided message
        response = openai.chat.completions.create(
            model="gpt-4o-mini",  # Specify the model
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )
        
        response_message = ""
        # Use a synchronous loop to handle the response
        for chunk in response:  # Iterate over the response chunks
            if chunk.choices and chunk.choices[0].delta.content:  # Check if choices exist and content is not None
                delta_content = chunk.choices[0].delta.content  # Extract the response message
                response_message += delta_content  # Append to the response message
        # Parse the JSON response
        response_message
        output= {"content":response_message}
        return output


# New function to send audio to OpenAI Whisper model
async def send_to_whisper_model(audio_file):
    file_path = os.path.join(UPLOAD_FOLDER, "recording.wav")
    with open(file_path, 'wb') as f:  # Open the file in write-binary mode
        f.write(audio_file)
    audio_filea= open(file_path,"rb")
    
    client = OpenAI()
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_filea
    )
    return transcription.text
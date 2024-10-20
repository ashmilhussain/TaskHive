import openai
import os
import json

openai.api_key = os.getenv("OPENAI_API_KEY")  # Set your OpenAI API key from environment variable

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

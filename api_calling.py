from google import genai
# from google.genai import types
from dotenv import load_dotenv
import os
import streamlit as st
from gtts import gTTS
import io

from PIL import Image



load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# images = st.file_uploader(
#         "Upload the photos of your note",
#         type=['jpg','jpeg','png'],
#         accept_multiple_files = True
#     )


def note_generator(images):
    prompt = (
        "You are given images of notes. Extract and summarise all important "
        "information clearly and concisely."
    )

    contents = [images, prompt]

    # for image in images:
    #     image_bytes = image.read()

    #     contents.append(
    #         types.Part.from_bytes(
    #             data=image_bytes,
    #             mime_type=image.type
    #         )
    #     )

    # contents.append(prompt)

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=contents
    )

    return response.text

def audio_transcription(text):
    speech = gTTS(text=text, lang='en', slow=False)
    audio_buffer = io.BytesIO() #create an in-memory buffer to hold the audio data
    speech.write_to_fp(audio_buffer) #write the audio data to the buffer, write to fp means write to file-like object
    audio_buffer.seek(0) #reset the buffer's position to the beginning so that it
    return audio_buffer

def quiz_generator(image, difficulty):
    prompt = f"Generate a quiz based on the content of the image. The quiz should be of {difficulty} difficulty level and should include multiple-choice questions with four options each, along with the correct answer.Add correct answer after the quiz"
    contents = [image, prompt]
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=contents
    )
    return response.text
from turtle import st

from google import genai
from dotenv import load_dotenv
import os
from gtts import gTTS
import io



load_dotenv()
my_api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=my_api_key)


#Note Generator

def note_generator(images):
    
    prompt = """Summarize the picture in notes at maximum 100 Words,
        make sure to add necessary markdown to differentiate different sections"""

    response =client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[images,prompt]
    )

    return response.text



def audio_transcription(text):
    speech = gTTS(text, lang='en', slow=False)
    audio_buffer = io.BytesIO()
    speech.write_to_fp(audio_buffer)
    return audio_buffer


def quiz_generator(images, difficulty):
    prompt = f"""Generate a {difficulty} difficulty quiz based on the content of the images. 
    Include multiple-choice questions with options and a correct answer."""

    response =client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[images,prompt]
    )

    return response.text

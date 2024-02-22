from pathlib import Path
from openai import OpenAI
import pygame

api_key = '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'
client = OpenAI(api_key=api_key)
my_own_message = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
]

# Get user input dynamically
user_input = input("Enter your message: ")

# Append user input to the list
my_own_message.append({"role": "user", "content": user_input})

print(my_own_message)
completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=my_own_message
)

assistant_response = completion.choices[0].message.content

response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    input=assistant_response  # Pass the text content here
)

speech_file_path = Path(__file__).parent / "speech.mp3"
response.stream_to_file(speech_file_path)


audio_file = open(speech_file_path, "rb")
transcript = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file, 
  response_format="text",
)
print(transcript)

# Play the audio automatically using pygame
pygame.mixer.init()
pygame.mixer.music.load(str(speech_file_path))
pygame.mixer.music.play()

# Wait for the audio to finish playing
pygame.time.wait(int(pygame.mixer.Sound(speech_file_path).get_length() * 1000))

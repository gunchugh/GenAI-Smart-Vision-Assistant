from gtts import gTTS
import os
import time

# Audio folder
AUDIO_FOLDER = "static/audio"

# Folder create if not exists
os.makedirs(AUDIO_FOLDER, exist_ok=True)

def text_to_speech(text):

    # Unique filename
    filename = f"caption_{int(time.time())}.mp3"

    # Full path
    audio_path = os.path.join(AUDIO_FOLDER, filename)

    # Generate speech
    tts = gTTS(
        text=text,
        lang="en"
    )

    # Save audio
    tts.save(audio_path)

    # Debug prints
    print("Audio saved at:", audio_path)
    print("File exists:", os.path.exists(audio_path))
    print("File size:", os.path.getsize(audio_path), "bytes")

    # Return relative path for Flask
    return f"audio/{filename}"
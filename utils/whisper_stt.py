from faster_whisper import WhisperModel

# Lazy Load
model = None


def get_model():
    global model

    if model is None:

        model = WhisperModel(
            "tiny",
            device="cpu",
            compute_type="int8"
        )

    return model


def speech_to_text(audio_path):

    model = get_model()

    segments, info = model.transcribe(audio_path)

    text = ""

    for segment in segments:
        text += segment.text + " "

    return text.strip()
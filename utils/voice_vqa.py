from utils.whisper_stt import speech_to_text
from utils.vqa import answer_question
from utils.speech import text_to_speech


def voice_question_answer(audio_path, image_path):

    question = speech_to_text(audio_path)

    answer = answer_question(
        image_path,
        question
    )

    audio = text_to_speech(answer)

    return question, answer, audio
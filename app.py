from flask import Flask, render_template, request, send_from_directory
import os
import gc

from utils.detection import detect_image
from utils.video_detection import detect_video
from utils.tracking import track_video
from utils.caption import generate_caption
from utils.speech import text_to_speech
from utils.whisper_stt import speech_to_text
from utils.vqa import answer_question
from utils.voice_vqa import voice_question_answer
from utils.pdf_report import generate_report
from utils.charts import generate_charts

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ---------------- HOME ---------------- #

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- IMAGE DETECTION ---------------- #

@app.route("/detect", methods=["POST"])
def detect():

    if "image" not in request.files:
        return "No image uploaded!"

    image = request.files["image"]

    if image.filename == "":
        return "Please select an image!"

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        image.filename
    )

    image.save(filepath)

    # Save image path for VQA
    app.config["LAST_IMAGE"] = filepath

    image_name, dashboard, total_objects = detect_image(filepath)

    caption = generate_caption(filepath)
    app.config["LAST_CAPTION"] = caption
    audio = text_to_speech(caption)

    bar_chart, pie_chart, confidence_chart, summary = generate_charts(dashboard)
    
    gc.collect()
    return render_template(
        "result.html",
        image=image_name,
        dashboard=dashboard,
        total_objects=total_objects,
        caption=caption,
        audio=audio,
        bar_chart=bar_chart,
        pie_chart=pie_chart,
        confidence_chart=confidence_chart,
        summary=summary
    )


# ---------------- VIDEO DETECTION ---------------- #

@app.route("/video_detect", methods=["POST"])
def video_detect():

    if "video" not in request.files:
        return "No video uploaded!"

    video = request.files["video"]

    if video.filename == "":
        return "Please select a video."

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        video.filename
    )

    video.save(filepath)

    output_video = detect_video(filepath)

    gc.collect()
    return render_template(
        "video_result.html",
        video=os.path.basename(output_video)
    )


# ---------------- OBJECT TRACKING ---------------- #

@app.route("/track", methods=["POST"])
def track():

    if "video" not in request.files:
        return "No video uploaded."

    video = request.files["video"]

    if video.filename == "":
        return "Please select a video."

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        video.filename
    )

    video.save(filepath)

    output_video = track_video(filepath)

    gc.collect()
    return render_template(
        "tracking_result.html",
        video=os.path.basename(output_video)
    )


# ---------------- VISUAL QUESTION ANSWERING ---------------- #

@app.route("/ask", methods=["POST"])
def ask():

    question = request.form.get("question")

    image_path = app.config.get("LAST_IMAGE")

    if image_path is None:
        return {"answer": "No image found."}

    answer = answer_question(
        image_path,
        question
    )
    app.config["LAST_QUESTION"] = question
    app.config["LAST_ANSWER"] = answer

    return {
        "answer": answer
    }


# ---------------- SPEECH TO TEXT ---------------- #

@app.route("/speech_to_text", methods=["POST"])
def speech_to_text_route():

    if "audio" not in request.files:
        return {"text": "No audio received"}

    audio = request.files["audio"]

    RECORDING_FOLDER = "static/recordings"

    os.makedirs(RECORDING_FOLDER, exist_ok=True)

    audio_path = os.path.join(
        RECORDING_FOLDER,
        "recording.webm"
    )

    audio.save(audio_path)

    try:

        text = speech_to_text(audio_path)

        print("Recognized:", text)

        return {"text": text}

    except Exception as e:

        print(e)

        return {"text": str(e)}

#----------------VOICE ANSWER--------------#
@app.route("/voice_ask", methods=["POST"])
def voice_ask():

    if "audio" not in request.files:
        return {"error": "No audio"}

    audio = request.files["audio"]

    folder = "static/recordings"

    os.makedirs(folder, exist_ok=True)

    audio_path = os.path.join(
        folder,
        "voice_question.webm"
    )

    audio.save(audio_path)

    image_path = app.config.get("LAST_IMAGE")

    question, answer, audio_file = voice_question_answer(
        audio_path,
        image_path
    )
    
    
    return {
        "question": question,
        "answer": answer,
        "audio": audio_file
    }
#----------------DOWNLOAD REPORT-------#
@app.route("/download_report")
def download_report():

    caption = app.config.get("LAST_CAPTION", "Not Available")
    question = app.config.get("LAST_QUESTION", "Not Asked")
    answer = app.config.get("LAST_ANSWER", "Not Answered")

    pdf = generate_report(
        caption,
        question,
        answer
    )

    return send_from_directory(
        "static",
        pdf,
        as_attachment=True
    )
# ---------------- RUN APP ---------------- #

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)
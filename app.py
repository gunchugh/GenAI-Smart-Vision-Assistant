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
from utils.video_report import generate_video_report
from utils.tracking_report import generate_tracking_report

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
    app.config["LAST_RESULT_IMAGE"] = image_name
    app.config["LAST_BAR_CHART"] = bar_chart
    app.config["LAST_SUMMARY"] = summary
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

    video_name, dashboard, total_objects, summary, first_frame_path = detect_video(filepath)
    caption = generate_caption(first_frame_path)

    app.config["VIDEO_FRAME"] = first_frame_path
    app.config["VIDEO_CAPTION"] = caption
    app.config["VIDEO_DASHBOARD"] = dashboard
    app.config["VIDEO_SUMMARY"] = summary

    gc.collect()

    return render_template(
    "video_result.html",
    video=video_name,
    dashboard=dashboard,
    total_objects=total_objects,
    summary=summary,
    caption=caption,
    frame=os.path.basename(first_frame_path)
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
    result = track_video(filepath)
    print(result)
    tracked_video, summary, dashboard = track_video(filepath)
    app.config["TRACKING_DASHBOARD"] = dashboard
    gc.collect()
    
    return render_template(
    "tracking_result.html",
    video=os.path.basename(tracked_video),
    summary=summary,
    dashboard=dashboard
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
    app.config["LAST_VOICE_QUESTION"] = question
    app.config["LAST_VOICE_ANSWER"] = answer
    
    
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

    caption=caption,

    question=question,

    answer=answer,

    original_image=app.config.get("LAST_IMAGE"),

    detected_image=os.path.join(
        "static",
        "results",
        app.config.get("LAST_RESULT_IMAGE")
    ),

    chart=os.path.join(
        "static",
        "charts",
        app.config.get("LAST_BAR_CHART")
    ),

    summary=app.config.get("LAST_SUMMARY"),

    voice_question=app.config.get(
        "LAST_VOICE_QUESTION",
        "Not Asked"
    ),

    voice_answer=app.config.get(
        "LAST_VOICE_ANSWER",
        "Not Answered"
    )

)

    return send_from_directory(
        "static",
        pdf,
        as_attachment=True
    )
# ---------------- VIDEO REPORT ---------------- #

@app.route("/download_video_report")
def download_video_report():

    frame = app.config.get("VIDEO_FRAME")
    caption = app.config.get("VIDEO_CAPTION")
    dashboard = app.config.get("VIDEO_DASHBOARD")
    summary = app.config.get("VIDEO_SUMMARY")

    pdf = generate_video_report(
        frame,
        caption,
        dashboard,
        summary
    )

    return send_from_directory(
        "static",
        pdf,
        as_attachment=True
    )
# ---------------- TRACKING REPORT ---------------- #

@app.route("/download_tracking_report")
def download_tracking_report():

    dashboard = app.config["TRACKING_DASHBOARD"]

    pdf = generate_tracking_report(
        dashboard
    )

    return send_from_directory(
        "static",
        pdf,
        as_attachment=True
    )
# ---------------- RUN APP ---------------- #

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="127.0.0.1", port=port)
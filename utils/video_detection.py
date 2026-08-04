from ultralytics import YOLO
import os

# Lazy Load
model = None


def get_model():
    global model

    if model is None:
        model = YOLO("yolo11n.pt")

    return model


def detect_video(video_path):

    model = get_model()

    os.makedirs("static/videos", exist_ok=True)

    model.predict(
        source=video_path,
        save=True,
        project="static",
        name="videos",
        exist_ok=True
    )

    output_path = os.path.join(
        "static",
        "videos",
        os.path.basename(video_path)
    )

    return output_path
from ultralytics import YOLO
import os

model = YOLO("yolo11n.pt")


def detect_video(video_path):

    os.makedirs("static/videos", exist_ok=True)

    results = model.predict(
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
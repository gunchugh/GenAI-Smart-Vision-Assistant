from ultralytics import YOLO
import os
import gc
import torch

# CPU Optimization
torch.set_num_threads(2)

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

    with torch.inference_mode():
        model.predict(
            source=video_path,
            save=True,
            project="static",
            name="videos",
            exist_ok=True,
            verbose=False,
            stream=False
        )

    output_path = os.path.join(
        "static",
        "videos",
        os.path.basename(video_path)
    )

    gc.collect()

    return output_path
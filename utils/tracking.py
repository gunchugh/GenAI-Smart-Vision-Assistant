from ultralytics import YOLO
import os
import gc
import torch

torch.set_num_threads(2)

model = None

def get_model():
    global model
    if model is None:
        model = YOLO("yolo11n.pt")
    return model


def track_video(video_path):

    model = get_model()

    os.makedirs("static/tracking", exist_ok=True)

    with torch.inference_mode():
        model.track(
            source=video_path,
            tracker="bytetrack.yaml",
            save=True,
            project="static",
            name="tracking",
            exist_ok=True,
            persist=True,
            verbose=False
        )

    gc.collect()

    return os.path.join(
        "static",
        "tracking",
        os.path.basename(video_path)
    )
print("TRACKING.PY LOADED")

from ultralytics import YOLO
import torch
import os
import gc
import glob
import shutil
from collections import defaultdict

torch.set_num_threads(2)

model = None


def get_model():

    global model

    if model is None:
        model = YOLO("yolo11n.pt")

    return model


def track_video(video_path):

    model = get_model()

    object_count = defaultdict(int)

    with torch.inference_mode():

        results = model.track(

            source=video_path,

            tracker="bytetrack.yaml",

            stream=True,

            save=True,

            project="runs",

            name="tracking",

            exist_ok=True,

            persist=True,

            verbose=False

        )

        for result in results:

            if result.boxes is None:
                continue

            for box in result.boxes:

                cls = int(box.cls[0])

                label = model.names[cls]

                object_count[label] += 1

    generated = glob.glob(
        "runs/**/*.*",
        recursive=True
    )

    videos = [
        f for f in generated
        if f.lower().endswith(
            (".mp4", ".avi", ".mov", ".mkv")
        )
    ]

    if not videos:
        raise Exception("Tracked video not found.")

    latest = max(
        videos,
        key=os.path.getctime
    )

    os.makedirs(
        "static/tracking",
        exist_ok=True
    )

    final_path = os.path.join(
        "static",
        "tracking",
        os.path.basename(latest)
    )

    shutil.copy(
        latest,
        final_path
    )

    gc.collect()

    dashboard = {}

    for label in object_count:

        dashboard[label] = {

            "count": object_count[label]

        }

    summary = {

        "tracking_status": "Completed",

        "model": "YOLO11",

        "tracker": "ByteTrack",

        "input_type": "Video",

        "total_objects": sum(object_count.values()),

        "unique_classes": len(object_count),

        "most_detected": (

            max(
                object_count,
                key=object_count.get
            )

            if object_count else "-"

        )

    }

    print("RETURNING:", final_path)
    print("SUMMARY:", summary)

    return (

        final_path,

        summary,

        dashboard

    )
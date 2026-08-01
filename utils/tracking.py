from ultralytics import YOLO
import os

model = YOLO("yolo11n.pt")


def track_video(video_path):

    os.makedirs("static/tracking", exist_ok=True)

    model.track(
        source=video_path,
        tracker="bytetrack.yaml",
        save=True,
        project="static",
        name="tracking",
        exist_ok=True,
        persist=True
    )

    output_path = os.path.join(
        "static",
        "tracking",
        os.path.basename(video_path)
    )

    return output_path
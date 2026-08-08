from ultralytics import YOLO
import cv2
import os
import gc
import time
import torch
from collections import defaultdict


# ---------------- CPU ---------------- #

torch.set_num_threads(2)

# ---------------- MODEL ---------------- #

model = None


def get_model():

    global model

    if model is None:
        model = YOLO("yolo11n.pt")

    return model


# ---------------- VIDEO DETECTION ---------------- #

def detect_video(video_path):

    model = get_model()

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise Exception("Unable to open video.")

    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps == 0:
        fps = 30

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    timestamp = str(int(time.time()))

    output_folder = "static/videos"
    os.makedirs(output_folder, exist_ok=True)

    output_name = f"detected_{timestamp}.mp4"

    output_path = os.path.join(
        output_folder,
        output_name
    )

    # Browser compatible codec
    fourcc = cv2.VideoWriter_fourcc(*"avc1")

    writer = cv2.VideoWriter(
        output_path,
        fourcc,
        fps,
        (width, height)
    )

    # ---------- First Frame ---------- #

    first_frame_saved = False

    frame_folder = "static/video_frames"

    os.makedirs(
        frame_folder,
        exist_ok=True
    )

    first_frame_path = ""

    # ---------- Dashboard ---------- #

    object_count = defaultdict(int)

    confidence_sum = defaultdict(float)
    tracked_ids = defaultdict(set)

    total_frames = 0

    # ---------- PROCESS VIDEO ---------- #

    with torch.inference_mode():

        while True:

            success, frame = cap.read()

            if not success:
                break

            total_frames += 1

            results = model.track(
    frame,
    persist=True,
    tracker="bytetrack.yaml",
    verbose=False
)

            result = results[0]

            annotated_frame = result.plot()
            # ---------- DRAW TRACKING IDs ---------- #

            if result.boxes is not None:

             for box in result.boxes:

              if box.id is None:
                continue

             track_id = int(box.id.item())

             cls = int(box.cls[0])
 
             label = model.names[cls]

             x1, y1, x2, y2 = map(
             int,
             box.xyxy[0]
        )

             cv2.putText(

             annotated_frame,

            f"{label} #{track_id}",

            (x1, y1 - 10),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.6,

            (0, 255, 0),

            2

        )

             writer.write(annotated_frame)

            # ---------- SAVE FIRST FRAME ---------- #

             if not first_frame_saved:

                first_frame_path = os.path.join(
                    frame_folder,
                    f"{timestamp}.jpg"
                )

                cv2.imwrite(
                    first_frame_path,
                    annotated_frame
                )

                first_frame_saved = True

            # ---------- OBJECT COUNT ---------- #

            if result.boxes is None:
             continue

            for box in result.boxes:

             cls = int(box.cls[0])

            label = model.names[cls]

            confidence = float(box.conf[0]) * 100

    # -------- Tracking ID -------- #

            if box.id is None:
             continue

            track_id = int(box.id.item())

    # -------- Count only once -------- #

    if track_id not in tracked_ids[label]:

        tracked_ids[label].add(track_id)

        object_count[label] += 1

        confidence_sum[label] += confidence

    # ---------- RELEASE ---------- #

    cap.release()

    writer.release()

    cv2.destroyAllWindows()

    # ---------- DASHBOARD ---------- #

    dashboard = {}

    for label in object_count:

        avg_confidence = round(
    confidence_sum[label] /
    len(tracked_ids[label]),
    2
)

        dashboard[label] = {

            "count": object_count[label],

            "confidence": avg_confidence

        }

    total_objects = sum(object_count.values())

    summary = {

        "total_objects": total_objects,

        "unique_classes": len(dashboard),

        "most_detected": (
    max(
        object_count.items(),
        key=lambda x: x[1]
    )[0]
    if object_count else "-"
),

        "average_confidence": (
            round(
                sum(confidence_sum.values()) /
                total_objects,
                2
            )
            if total_objects else 0
        ),

        "total_frames": total_frames

    }

    gc.collect()

    return (
        output_name,
        dashboard,
        total_objects,
        summary,
        first_frame_path
    )
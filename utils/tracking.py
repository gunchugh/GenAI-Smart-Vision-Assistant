print("TRACKING.PY LOADED")

from ultralytics import YOLO
import torch
import os
import gc
import glob
import subprocess
import time
import subprocess
from collections import defaultdict


torch.set_num_threads(2)

model = None


# =========================================================
# MODEL
# =========================================================

def get_model():

    global model

    if model is None:

        model = YOLO("yolo11n.pt")

    return model


# =========================================================
# OBJECT TRACKING
# =========================================================

def track_video(video_path):

    model = get_model()

    object_count = defaultdict(int)

    # -----------------------------------------------------
    # RUN YOLO + BYTE TRACK
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # FIND GENERATED TRACKING VIDEO
    # -----------------------------------------------------

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

    timestamp = int(os.path.getctime(latest))

    final_name = f"tracked_{timestamp}.mp4"

    # ---------------- CONVERT TO BROWSER MP4 ---------------- #

    os.makedirs("static/tracking", exist_ok=True)

    mp4_name = os.path.splitext(
    os.path.basename(latest)
)[0] + ".mp4"

    final_path = os.path.join(
    "static",
    "tracking",
    mp4_name
)

    subprocess.run(
    [
        "ffmpeg",
        "-y",
        "-i",
        latest,
        "-c:v",
        "libx264",
        "-preset",
        "fast",
        "-pix_fmt",
        "yuv420p",
        "-movflags",
        "+faststart",
        final_path
    ],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

    if not os.path.exists(final_path):
     raise Exception("MP4 conversion failed.")

    print("BROWSER MP4:", final_path)
    # OUTPUT FOLDER
    # -----------------------------------------------------

    output_folder = "static/tracking"

    os.makedirs(
        output_folder,
        exist_ok=True
    )


    # -----------------------------------------------------
    # UNIQUE FINAL FILE NAME
    # -----------------------------------------------------

    timestamp = int(time.time())

    final_name = (
        f"tracked_{timestamp}.mp4"
    )

    final_path = os.path.join(
        output_folder,
        final_name
    )


    # -----------------------------------------------------
    # FFMPEG BROWSER COMPATIBLE CONVERSION
    # -----------------------------------------------------

    print("Converting tracking video for browser...")


    ffmpeg_command = [

        "ffmpeg",

        "-y",

        "-i",
        latest,

        # Video
        "-map",
        "0:v:0",

        # Audio if available
        "-map",
        "0:a?",

        # H.264
        "-c:v",
        "libx264",

        # Browser compatible profile
        "-profile:v",
        "main",

        "-level",
        "4.0",

        # Browser compatible pixel format
        "-pix_fmt",
        "yuv420p",

        # Fast encoding
        "-preset",
        "veryfast",

        # Audio
        "-c:a",
        "aac",

        "-b:a",
        "128k",

        # Put MP4 metadata at beginning
        "-movflags",
        "+faststart",

        final_path

    ]


    conversion = subprocess.run(

        ffmpeg_command,

        stdout=subprocess.PIPE,

        stderr=subprocess.PIPE

    )


    # -----------------------------------------------------
    # CHECK FFMPEG
    # -----------------------------------------------------

    if conversion.returncode != 0:

        error_message = (
            conversion.stderr
            .decode(
                errors="ignore"
            )
        )

        print(
            "FFMPEG ERROR:"
        )

        print(
            error_message
        )

        raise Exception(
            "Tracking video conversion failed."
        )


    print(
        "Tracking video converted successfully."
    )


    # -----------------------------------------------------
    # CHECK FINAL FILE
    # -----------------------------------------------------

    if not os.path.exists(final_path):

        raise Exception(
            "Final tracking video was not created."
        )


    print(
        "FINAL TRACKING VIDEO:"
    )

    print(
        final_path
    )


    # -----------------------------------------------------
    # DASHBOARD
    # -----------------------------------------------------

    dashboard = {}


    for label in object_count:

        dashboard[label] = {

            "count":
            object_count[label]

        }


    # -----------------------------------------------------
    # SUMMARY
    # -----------------------------------------------------

    summary = {

        "tracking_status":
        "Completed",

        "model":
        "YOLO11",

        "tracker":
        "ByteTrack",

        "input_type":
        "Video",

        "total_objects":
        sum(
            object_count.values()
        ),

        "unique_classes":
        len(
            object_count
        ),

        "most_detected":

        (

            max(
                object_count,
                key=object_count.get
            )

            if object_count

            else "-"

        )

    }


    # -----------------------------------------------------
    # CLEAN MEMORY
    # -----------------------------------------------------

    gc.collect()


    # -----------------------------------------------------
    # PRINT RESULTS
    # -----------------------------------------------------

    print(
        "RETURNING:",
        final_path
    )

    print(
        "SUMMARY:",
        summary
    )


    # -----------------------------------------------------
    # RETURN
    # -----------------------------------------------------

    return (

        final_path,

        summary,

        dashboard

    )
from ultralytics import YOLO
import os
import gc
import glob
import shutil
import torch

torch.set_num_threads(2)

model = None


def get_model():
    global model

    if model is None:
        model = YOLO("yolo11n.pt")

    return model


def detect_video(video_path):

    model = get_model()

    output_folder = "static/videos"

    os.makedirs(output_folder, exist_ok=True)

    # Purani mp4 files hata do
    for f in glob.glob(os.path.join(output_folder, "*.mp4")):
        try:
            os.remove(f)
        except:
            pass

    with torch.inference_mode():

        model.predict(
            source=video_path,
            save=True,
            project="runs",
            name="detect_video",
            exist_ok=True,
            verbose=False
        )

    # Latest generated video
    generated = glob.glob("runs/detect_video/*.mp4")

    if not generated:
        raise Exception("Output video not found.")

    latest = max(generated, key=os.path.getctime)

    final_name = "detected_video.mp4"

    final_path = os.path.join(
        output_folder,
        final_name
    )

    shutil.copy(latest, final_path)

    gc.collect()
    print("Generated files:")
    print(glob.glob("runs/detect_video/*"))

    print("Final video:")
    print(final_path)

    print("Exists:", os.path.exists(final_path))
    gc.collect()
    return final_path
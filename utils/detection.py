from ultralytics import YOLO
import cv2
import os

# Lazy Load
model = None

def get_model():
    global model
    if model is None:
        model = YOLO("yolo11n.pt")
    return model


def detect_image(image_path):

    model = get_model()

    results = model(image_path)

    annotated_image = results[0].plot()

    os.makedirs("static/results", exist_ok=True)

    output_path = os.path.join(
        "static",
        "results",
        os.path.basename(image_path)
    )

    cv2.imwrite(output_path, annotated_image)

    names = model.names

    object_count = {}
    confidence_sum = {}

    for box in results[0].boxes:

        cls = int(box.cls[0])
        label = names[cls]

        confidence = float(box.conf[0]) * 100

        object_count[label] = object_count.get(label, 0) + 1

        confidence_sum[label] = (
            confidence_sum.get(label, 0) + confidence
        )

    dashboard = {}

    for label in object_count:

        dashboard[label] = {
            "count": object_count[label],
            "confidence": round(
                confidence_sum[label] / object_count[label],
                2
            )
        }

    total_objects = sum(object_count.values())

    return (
        os.path.basename(image_path),
        dashboard,
        total_objects
    )

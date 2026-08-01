import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import os
import time

CHART_FOLDER = "static/charts"
os.makedirs(CHART_FOLDER, exist_ok=True)


def generate_charts(dashboard):

    labels = []
    counts = []
    confidences = []

    total_objects = 0

    for label, data in dashboard.items():
        labels.append(label)
        counts.append(data["count"])
        confidences.append(data["confidence"])
        total_objects += data["count"]

    timestamp = str(int(time.time()))

    # ---------- Bar ----------
    bar_file = f"bar_{timestamp}.png"

    plt.figure(figsize=(8,5))
    plt.bar(labels, counts)
    plt.title("Detected Objects")
    plt.tight_layout()
    plt.savefig(os.path.join(CHART_FOLDER, bar_file))
    plt.close()

    # ---------- Pie ----------
    pie_file = f"pie_{timestamp}.png"

    plt.figure(figsize=(6,6))
    plt.pie(
        counts,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90
    )
    plt.title("Object Distribution")
    plt.tight_layout()
    plt.savefig(os.path.join(CHART_FOLDER, pie_file))
    plt.close()

    # ---------- Confidence ----------
    confidence_file = f"confidence_{timestamp}.png"

    plt.figure(figsize=(8,5))
    plt.bar(labels, confidences)
    plt.title("Confidence")
    plt.tight_layout()
    plt.savefig(
        os.path.join(CHART_FOLDER, confidence_file)
    )
    plt.close()

    summary = {

        "total_objects": total_objects,

        "unique_classes": len(labels),

        "most_detected":
            labels[counts.index(max(counts))]
            if labels else "-",

        "highest_confidence":
            max(confidences)
            if confidences else 0,

        "average_confidence":
            round(
                sum(confidences) /
                len(confidences),
                2
            ) if confidences else 0

    }

    return (
        bar_file,
        pie_file,
        confidence_file,
        summary
    )
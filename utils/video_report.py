from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.lib import colors

import os
import time


# ---------------- REPORT FOLDER ---------------- #

REPORT_FOLDER = "static/video_reports"

os.makedirs(
    REPORT_FOLDER,
    exist_ok=True
)


# ---------------- STYLES ---------------- #

styles = getSampleStyleSheet()

title_style = styles["Heading1"]
title_style.alignment = TA_CENTER

heading_style = styles["Heading2"]

normal_style = styles["BodyText"]


# ---------------- VIDEO REPORT ---------------- #

def generate_video_report(
    frame,
    caption,
    dashboard,
    summary
):

    filename = f"video_report_{int(time.time())}.pdf"

    pdf_path = os.path.join(
        REPORT_FOLDER,
        filename
    )

    doc = SimpleDocTemplate(
        pdf_path,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    story = []
        # ---------------- LOGO ---------------- #

    logo_path = "static/images/logo.png"

    if os.path.exists(logo_path):

        logo = Image(
            logo_path,
            width=1.2 * inch,
            height=1.2 * inch
        )

        logo.hAlign = "CENTER"

        story.append(logo)

    story.append(
        Paragraph(
            "<b>GenAI Smart Vision Assistant</b>",
            title_style
        )
    )

    story.append(
        Paragraph(
            "<b>Video Detection Report</b>",
            heading_style
        )
    )

    story.append(
        Paragraph(
            time.strftime("%d %B %Y  %I:%M %p"),
            normal_style
        )
    )

    story.append(
        Spacer(1, 20)
    )

    # ---------------- FIRST FRAME ---------------- #

    if os.path.exists(frame):

        frame_image = Image(
            frame,
            width=5.5 * inch,
            height=3.2 * inch
        )

        frame_image.hAlign = "CENTER"

        story.append(frame_image)

        story.append(
            Spacer(1, 15)
        )

    # ---------------- AI CAPTION ---------------- #

    story.append(
        Paragraph(
            "<b>AI Generated Caption</b>",
            heading_style
        )
    )

    story.append(
        Paragraph(
            caption,
            normal_style
        )
    )

    story.append(
        Spacer(1, 20)
    )

    # ---------------- SUMMARY ---------------- #

    story.append(
        Paragraph(
            "<b>Detection Summary</b>",
            heading_style
        )
    )

    summary_data = [

        ["Total Objects", str(summary["total_objects"])],

        ["Unique Classes", str(summary["unique_classes"])],

        ["Most Detected", summary["most_detected"].title()],

        [
            "Average Confidence",
            f'{summary["average_confidence"]}%'
        ]

    ]

    summary_table = Table(
        summary_data,
        colWidths=[200, 220]
    )

    summary_table.setStyle(

        TableStyle([

            ("GRID", (0, 0), (-1, -1), 1, colors.grey),

            ("BACKGROUND", (0, 0), (0, -1),
             colors.HexColor("#EAF2FF")),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),

            ("TOPPADDING", (0, 0), (-1, -1), 8)

        ])

    )

    story.append(summary_table)

    story.append(
        Spacer(1, 20)
    )
        # ---------------- OBJECT TABLE ---------------- #

    story.append(
        Paragraph(
            "<b>Detected Objects</b>",
            heading_style
        )
    )

    table_data = [
        ["Object", "Count", "Average Confidence"]
    ]

    for label, data in dashboard.items():

        table_data.append([
            label.title(),
            str(data["count"]),
            f'{data["confidence"]}%'
        ])

    object_table = Table(
        table_data,
        colWidths=[180, 120, 120]
    )

    object_table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, 0),
             colors.HexColor("#4F81BD")),

            ("TEXTCOLOR", (0, 0), (-1, 0),
             colors.white),

            ("GRID", (0, 0), (-1, -1),
             1, colors.black),

            ("ALIGN", (0, 0), (-1, -1),
             "CENTER"),

            ("BOTTOMPADDING", (0, 0), (-1, -1),
             8),

            ("TOPPADDING", (0, 0), (-1, -1),
             8)

        ])

    )

    story.append(object_table)

    story.append(
        Spacer(1, 20)
    )

    # ---------------- FOOTER ---------------- #

    story.append(

        Paragraph(

            "<b>Developed by Gun Chugh</b>",

            heading_style

        )

    )

    story.append(

        Paragraph(

            "GenAI Smart Vision Assistant",

            normal_style

        )

    )

    story.append(

        Paragraph(

            "Powered by YOLO11 • OpenCV • Flask • BLIP",

            normal_style

        )

    )

    # ---------------- SAVE PDF ---------------- #

    doc.build(story)

    return f"video_reports/{filename}"
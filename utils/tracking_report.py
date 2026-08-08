from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.lib import colors

import os
import time


REPORT_FOLDER = "static/tracking_reports"

os.makedirs(
    REPORT_FOLDER,
    exist_ok=True
)

styles = getSampleStyleSheet()

title_style = styles["Heading1"]
title_style.alignment = TA_CENTER

heading_style = styles["Heading2"]

normal_style = styles["BodyText"]


def generate_tracking_report(dashboard):

    filename = f"tracking_report_{int(time.time())}.pdf"

    pdf_path = os.path.join(
        REPORT_FOLDER,
        filename
    )

    doc = SimpleDocTemplate(
        pdf_path
    )

    story = []

    # ---------------- LOGO ---------------- #

    logo = "static/images/logo.png"

    if os.path.exists(logo):

        img = Image(
            logo,
            width=1.2 * inch,
            height=1.2 * inch
        )

        img.hAlign = "CENTER"

        story.append(img)

    # ---------------- TITLE ---------------- #

    story.append(
        Paragraph(
            "<b>GenAI Smart Vision Assistant</b>",
            title_style
        )
    )

    story.append(
        Paragraph(
            "<b>Object Tracking Report</b>",
            heading_style
        )
    )

    story.append(
        Paragraph(
            time.strftime("%d %B %Y %I:%M %p"),
            normal_style
        )
    )

    story.append(
        Spacer(1, 20)
    )

    # ---------------- TRACKING SUMMARY ---------------- #

    story.append(
        Paragraph(
            "<b>Tracking Summary</b>",
            heading_style
        )
    )

    summary_data = [

        ["Detection Model", "YOLO11"],

        ["Tracking Algorithm", "ByteTrack"],

        ["Tracking Type", "Multi Object"],

        ["Unique IDs", "Enabled"]

    ]

    summary_table = Table(
        summary_data,
        colWidths=[200, 220]
    )

    summary_table.setStyle(

        TableStyle([

            ("GRID",(0,0),(-1,-1),1,colors.grey),

            ("BACKGROUND",(0,0),(0,-1),
             colors.HexColor("#EAF2FF")),

            ("BOTTOMPADDING",(0,0),(-1,-1),8),

            ("TOPPADDING",(0,0),(-1,-1),8)

        ])

    )

    story.append(summary_table)

    story.append(
        Spacer(1,20)
    )

    # ---------------- TRACKED OBJECTS ---------------- #

    story.append(
        Paragraph(
            "<b>Tracked Objects Summary</b>",
            heading_style
        )
    )

    table_data = [

        ["Object", "Count"]

    ]

    for label, data in dashboard.items():

        table_data.append(

            [

                label.title(),

                str(data["count"])

            ]

        )

    object_table = Table(
        table_data,
        colWidths=[220,180]
    )

    object_table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(-1,0),
             colors.HexColor("#4F81BD")),

            ("TEXTCOLOR",(0,0),(-1,0),
             colors.white),

            ("GRID",(0,0),(-1,-1),
             1,colors.grey),

            ("ALIGN",(0,0),(-1,-1),
             "CENTER"),

            ("BOTTOMPADDING",(0,0),(-1,-1),
             8),

            ("TOPPADDING",(0,0),(-1,-1),
             8)

        ])

    )

    story.append(object_table)

    story.append(
        Spacer(1,20)
    )

    # ---------------- ABOUT TRACKING ---------------- #

    story.append(
        Paragraph(
            "<b>About Object Tracking</b>",
            heading_style
        )
    )

    story.append(
        Paragraph(
            "This module performs multi-object tracking using "
            "<b>YOLO11</b> together with <b>ByteTrack</b>. "
            "Each detected object is assigned a unique tracking ID "
            "that remains consistent across consecutive video frames. "
            "This technology is useful for surveillance, traffic "
            "monitoring, crowd analysis and smart city applications.",
            normal_style
        )
    )

    story.append(
        Spacer(1,20)
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
            "YOLO11 • ByteTrack • OpenCV • Flask",
            normal_style
        )
    )

    story.append(
        Paragraph(
            "GenAI Smart Vision Assistant",
            normal_style
        )
    )

    # ---------------- SAVE PDF ---------------- #

    doc.build(story)

    return f"tracking_reports/{filename}"
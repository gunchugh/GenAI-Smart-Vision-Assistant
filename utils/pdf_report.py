from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth

import os
import time

REPORT_FOLDER = "static/reports"
os.makedirs(REPORT_FOLDER, exist_ok=True)


styles = getSampleStyleSheet()

title_style = styles["Heading1"]
title_style.alignment = TA_CENTER

heading_style = styles["Heading2"]

normal_style = styles["BodyText"]


def generate_report(
        caption,
        question,
        answer,
        original_image,
        detected_image,
        chart,
        summary,
        voice_question,
        voice_answer
):

    filename = f"report_{int(time.time())}.pdf"

    pdf_path = os.path.join(
        REPORT_FOLDER,
        filename
    )

    doc = SimpleDocTemplate(

        pdf_path,

        rightMargin=20,
        leftMargin=20,
        topMargin=20,
        bottomMargin=20

    )

    story = []

    logo = "static/images/logo.png"

    if os.path.exists(logo):

        img = Image(
            logo,
            width=1.1 * inch,
            height=1.1 * inch
        )

        img.hAlign = "CENTER"

        story.append(img)

    story.append(
        Paragraph(
            "<b>GenAI Smart Vision Assistant</b>",
            title_style
        )
    )

    story.append(

        Paragraph(

            "<b>AI Detection Report</b>",

            heading_style

        )

    )

    story.append(

        Paragraph(

            time.strftime(
                "%d %B %Y   %I:%M %p"
            ),

            normal_style

        )

    )

    story.append(Spacer(1, 15))
        # ---------------- Images ---------------- #

    story.append(
        Paragraph(
            "<b>Detection Images</b>",
            heading_style
        )
    )

    image_data = []

    if os.path.exists(original_image):
        original = Image(
            original_image,
            width=2.6 * inch,
            height=2.1 * inch
        )
    else:
        original = Paragraph("Original Image Not Found", normal_style)

    if os.path.exists(detected_image):
        detected = Image(
            detected_image,
            width=2.6 * inch,
            height=2.1 * inch
        )
    else:
        detected = Paragraph("Detected Image Not Found", normal_style)

    image_data.append([original, detected])

    image_table = Table(image_data)

    image_table.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 1, colors.grey),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 8),
    ]))

    story.append(image_table)

    story.append(Spacer(1, 15))


    # ---------------- Summary ---------------- #

    story.append(
        Paragraph(
            "<b>Detection Summary</b>",
            heading_style
        )
    )

    summary_table = Table([

        ["Total Objects", str(summary["total_objects"])],

        ["Unique Classes", str(summary["unique_classes"])],

        ["Most Detected", summary["most_detected"]],

        ["Average Confidence",
         str(summary["average_confidence"]) + "%"]

    ])

    summary_table.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#E8F0FE")),

        ("GRID",(0,0),(-1,-1),1,colors.grey),

        ("FONTNAME",(0,0),(-1,-1),"Helvetica"),

        ("BOTTOMPADDING",(0,0),(-1,-1),8),

        ("TOPPADDING",(0,0),(-1,-1),8),

    ]))

    story.append(summary_table)

    story.append(Spacer(1,12))


    # ---------------- Caption ---------------- #

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

    story.append(Spacer(1,15))
        # ---------------- Ask AI ---------------- #

    story.append(
        Paragraph(
            "<b>Ask AI Result</b>",
            heading_style
        )
    )

    story.append(
        Paragraph(
            f"<b>Question:</b> {question}",
            normal_style
        )
    )

    story.append(
        Paragraph(
            f"<b>Answer:</b> {answer}",
            normal_style
        )
    )

    story.append(Spacer(1,12))
    # ---------------- Voice AI ---------------- #

    story.append(
    Paragraph(
        "<b>Voice Question Answering</b>",
        heading_style
    )
)

    story.append(
    Paragraph(
        f"<b>Voice Question:</b> {voice_question}",
        normal_style
    )
)

    story.append(
    Paragraph(
        f"<b>Voice Answer:</b> {voice_answer}",
        normal_style
    )
)

    story.append(Spacer(1,12))

    # ---------------- Chart ---------------- #

    if chart and os.path.exists(chart):

        story.append(
            Paragraph(
                "<b>Detection Analytics</b>",
                heading_style
            )
        )

        chart_img = Image(
            chart,
            width=5.8 * inch,
            height=3.2 * inch
        )

        chart_img.hAlign = "CENTER"

        story.append(chart_img)

        story.append(Spacer(1,12))


    # ---------------- Status ---------------- #

    status = Table([
        ["AI Analysis Status", "Completed Successfully"]
    ])

    status.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(0,0),colors.HexColor("#0F62FE")),
        ("TEXTCOLOR",(0,0),(0,0),colors.white),

        ("BACKGROUND",(1,0),(1,0),colors.HexColor("#DFF6DD")),

        ("GRID",(0,0),(-1,-1),1,colors.grey),

        ("ALIGN",(0,0),(-1,-1),"CENTER"),

        ("BOTTOMPADDING",(0,0),(-1,-1),8),

        ("TOPPADDING",(0,0),(-1,-1),8)

    ]))

    story.append(status)

    story.append(Spacer(1,12))


    # ---------------- Footer ---------------- #

    story.append(
        Paragraph(
            "<b>Developed by Gun Chugh</b>",
            heading_style
        )
    )

    story.append(
        Paragraph(
            "YOLOv11 | ByteTrack | BLIP | Whisper | ViLT",
            normal_style
        )
    )

    story.append(
        Paragraph(
            "GenAI Smart Vision Assistant",
            normal_style
        )
    )

    doc.build(story)

    return f"reports/{filename}"
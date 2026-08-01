from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os
import time

REPORT_FOLDER = "static/reports"
os.makedirs(REPORT_FOLDER, exist_ok=True)

def generate_report(caption, question, answer):

    filename = f"report_{int(time.time())}.pdf"
    pdf_path = os.path.join(REPORT_FOLDER, filename)

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(pdf_path)

    story = [
        Paragraph("<b>AI Vision Assistant Report</b>", styles["Title"]),
        Paragraph(f"<b>Caption:</b> {caption}", styles["BodyText"]),
        Paragraph(f"<b>Question:</b> {question}", styles["BodyText"]),
        Paragraph(f"<b>Answer:</b> {answer}", styles["BodyText"])
    ]

    doc.build(story)

    return f"reports/{filename}"
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
from typing import List, Tuple
import os


def calculate_grade(score: float) -> str:
    """Ballga qarab bahoni aniqlash (78 ball tizimi)"""
    if score >= 70:
        return "A+"
    elif score >= 65:
        return "A"
    elif score >= 60:
        return "B+"
    elif score >= 55:
        return "B"
    elif score >= 50:
        return "C+"
    elif score >= 46:
        return "C"
    else:
        return "NC"


def calculate_percent(score: float, max_score: float = 78) -> float:
    """Ballni foizga o'girish"""
    if max_score == 0:
        return 0.0
    return round((score / max_score) * 100, 2)


def generate_test_results_pdf(test_name: str, results: List[Tuple[int, str, float, str]], output_path: str):
    """
    Test natijalari PDF hisobotini yaratish

    Args:
        test_name: Test nomi
        results: [(correct_count, full_name, score, completed_at), ...] formatdagi natijalar ro'yxati
        output_path: PDF faylni saqlash yo'li
    """
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    elements = []

    # Styles
    styles = getSampleStyleSheet()

    # Title style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=14,
        textColor=colors.black,
        spaceAfter=10,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.black,
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )

    # Title
    title = Paragraph("Milliy sertifikat", title_style)
    elements.append(title)

    # Subtitle
    subtitle = Paragraph(
        f"{test_name.upper()}<br/>"
        "IMTIHONIDA TALABGORLARNING RASH MODELI BO'YICHA TEKSHIRILGAN<br/>"
        "TEST NATIJALARI",
        subtitle_style
    )
    elements.append(subtitle)
    elements.append(Spacer(1, 0.2*inch))

    # Table data
    data = [
        ['№', 'Ism va familiya', "To'g'ri\njavoblar", 'Ball', 'Foiz', 'Daraja']
    ]

    for idx, (correct_count, full_name, score, completed_at) in enumerate(results, 1):
        grade = calculate_grade(score)
        percent = calculate_percent(score)
        data.append([
            str(idx),
            full_name,
            str(correct_count),
            f"{score:.2f}",
            f"{percent:.2f}%",
            grade
        ])

    # Create table
    table = Table(data, colWidths=[0.5*inch, 2.5*inch, 0.9*inch, 0.9*inch, 0.9*inch, 0.9*inch])

    # Table style
    table_style = TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),

        # Body
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (0, -1), 'CENTER'),  # № column
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),     # Name column
        ('ALIGN', (2, 1), (-1, -1), 'CENTER'),  # Other columns
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),

        # Grid
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])

    table.setStyle(table_style)
    elements.append(table)

    # Build PDF
    doc.build(elements)

    return output_path

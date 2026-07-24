#!/usr/bin/env python3
"""Shared colors and paragraph styles for training PDFs."""

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm

NAVY = colors.HexColor("#0B2B3C")
TEAL = colors.HexColor("#0E6B6B")
TEAL_LIGHT = colors.HexColor("#E6F3F3")
ACCENT = colors.HexColor("#C45C26")
SLATE = colors.HexColor("#334155")
MUTED = colors.HexColor("#64748B")
LINE = colors.HexColor("#CBD5E1")
WHITE = colors.white
SOFT = colors.HexColor("#F8FAFC")
CODE_BG = colors.HexColor("#F1F5F9")
WARN_BG = colors.HexColor("#FFF7ED")


def doc_styles():
    return {
        "h1": ParagraphStyle(
            "h1", fontName="Helvetica-Bold", fontSize=16, textColor=NAVY,
            spaceBefore=4, spaceAfter=8, leading=20,
        ),
        "h2": ParagraphStyle(
            "h2", fontName="Helvetica-Bold", fontSize=12.5, textColor=TEAL,
            spaceBefore=10, spaceAfter=5, leading=16,
        ),
        "h3": ParagraphStyle(
            "h3", fontName="Helvetica-Bold", fontSize=10.5, textColor=NAVY,
            spaceBefore=7, spaceAfter=3, leading=13,
        ),
        "body": ParagraphStyle(
            "body", fontName="Helvetica", fontSize=9.5, textColor=SLATE,
            alignment=TA_JUSTIFY, leading=13.2, spaceAfter=5,
        ),
        "bullet": ParagraphStyle(
            "bullet", fontName="Helvetica", fontSize=9, textColor=SLATE,
            leading=12.4, leftIndent=8, spaceAfter=2,
        ),
        "meta": ParagraphStyle(
            "meta", fontName="Helvetica-Oblique", fontSize=8.5, textColor=MUTED,
            leading=11, spaceAfter=4,
        ),
        "code": ParagraphStyle(
            "code", fontName="Courier", fontSize=7.8, textColor=NAVY,
            leading=10.5, spaceAfter=1,
        ),
        "callout": ParagraphStyle(
            "callout", fontName="Helvetica", fontSize=9, textColor=NAVY,
            leading=12.2,
        ),
        "table_h": ParagraphStyle(
            "table_h", fontName="Helvetica-Bold", fontSize=8, textColor=WHITE, leading=10,
        ),
        "table_c": ParagraphStyle(
            "table_c", fontName="Helvetica", fontSize=7.8, textColor=SLATE, leading=10,
        ),
        "toc_part": ParagraphStyle(
            "toc_part", fontName="Helvetica-Bold", fontSize=11, textColor=NAVY,
            spaceBefore=8, spaceAfter=2,
        ),
        "toc_item": ParagraphStyle(
            "toc_item", fontName="Helvetica", fontSize=9.5, textColor=SLATE, leading=13,
        ),
        "cover_title": ParagraphStyle(
            "cover_title", fontName="Helvetica-Bold", fontSize=26, textColor=NAVY,
            leading=32, alignment=TA_CENTER,
        ),
        "module_title": ParagraphStyle(
            "module_title", fontName="Helvetica-Bold", fontSize=11, textColor=WHITE, leading=14,
        ),
    }


def slide_styles():
    return {
        "eyebrow": ParagraphStyle(
            "eyebrow", fontName="Helvetica-Bold", fontSize=11, textColor=TEAL, spaceAfter=6,
        ),
        "h": ParagraphStyle(
            "h", fontName="Helvetica-Bold", fontSize=22, textColor=NAVY, leading=26, spaceAfter=10,
        ),
        "h2": ParagraphStyle(
            "h2", fontName="Helvetica-Bold", fontSize=16, textColor=NAVY, leading=20, spaceAfter=8,
        ),
        "body": ParagraphStyle(
            "body", fontName="Helvetica", fontSize=13, textColor=SLATE, leading=18, spaceAfter=6,
        ),
        "bullet": ParagraphStyle(
            "bullet", fontName="Helvetica", fontSize=12.5, textColor=SLATE, leading=17, spaceAfter=3,
        ),
        "small": ParagraphStyle(
            "small", fontName="Helvetica", fontSize=11, textColor=MUTED, leading=14,
        ),
        "code": ParagraphStyle(
            "code", fontName="Courier", fontSize=10.5, textColor=NAVY, leading=14, spaceAfter=2,
        ),
        "card_title": ParagraphStyle(
            "card_title", fontName="Helvetica-Bold", fontSize=12, textColor=NAVY, leading=15, spaceAfter=4,
        ),
        "card_body": ParagraphStyle(
            "card_body", fontName="Helvetica", fontSize=11, textColor=SLATE, leading=14,
        ),
        "white_title": ParagraphStyle(
            "white_title", fontName="Helvetica-Bold", fontSize=26, textColor=WHITE,
            leading=32, alignment=TA_CENTER,
        ),
        "white_sub": ParagraphStyle(
            "white_sub", fontName="Helvetica", fontSize=13,
            textColor=colors.HexColor("#D1E8E8"), leading=18, alignment=TA_CENTER,
        ),
        "brand": ParagraphStyle(
            "brand", fontName="Helvetica-Bold", fontSize=13,
            textColor=colors.HexColor("#7DCBCB"), alignment=TA_CENTER, spaceAfter=8,
        ),
        "table_h": ParagraphStyle(
            "table_h", fontName="Helvetica-Bold", fontSize=11, textColor=WHITE, leading=14,
        ),
        "table_c": ParagraphStyle(
            "table_c", fontName="Helvetica", fontSize=10.5, textColor=SLATE, leading=14,
        ),
        "callout": ParagraphStyle(
            "callout", fontName="Helvetica", fontSize=12, textColor=NAVY, leading=16,
        ),
        "example_label": ParagraphStyle(
            "example_label", fontName="Helvetica-Bold", fontSize=11, textColor=ACCENT, spaceAfter=4,
        ),
    }

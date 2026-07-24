#!/usr/bin/env python3
"""Shared colors and paragraph styles — Cookie Beamer inspired theme."""

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Cookie-like professional blue palette
BLUE = colors.HexColor("#2563EB")
BLUE_DARK = colors.HexColor("#1E40AF")
BLUE_SOFT = colors.HexColor("#DBEAFE")
BLUE_MID = colors.HexColor("#3B82F6")
INK = colors.HexColor("#0F172A")
SLATE = colors.HexColor("#334155")
MUTED = colors.HexColor("#64748B")
LINE = colors.HexColor("#E2E8F0")
SOFT = colors.HexColor("#F8FAFC")
WHITE = colors.white
CODE_BG = colors.HexColor("#F1F5F9")
WARN_BG = colors.HexColor("#FFF7ED")
ACCENT = colors.HexColor("#EA580C")
WATERMARK = colors.HexColor("#EEF2F7")

# Legacy aliases used by documentation builders
NAVY = INK
TEAL = BLUE
TEAL_LIGHT = BLUE_SOFT

_FONT_READY = False
FONT = "Helvetica"
FONT_BOLD = "Helvetica-Bold"
FONT_MED = "Helvetica-Bold"
FONT_MONO = "Courier"


def ensure_fonts():
    global _FONT_READY, FONT, FONT_BOLD, FONT_MED, FONT_MONO
    if _FONT_READY:
        return FONT, FONT_BOLD, FONT_MED, FONT_MONO
    try:
        pdfmetrics.registerFont(TTFont("Inter", "/usr/share/fonts/truetype/macos/Inter-Regular.ttf"))
        pdfmetrics.registerFont(TTFont("Inter-Bold", "/usr/share/fonts/truetype/macos/Inter-Bold.ttf"))
        pdfmetrics.registerFont(TTFont("Inter-Semi", "/usr/share/fonts/truetype/macos/Inter-SemiBold.ttf"))
        pdfmetrics.registerFont(TTFont("Inter-Med", "/usr/share/fonts/truetype/macos/Inter-Medium.ttf"))
        pdfmetrics.registerFont(TTFont("JBMono", "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Regular.ttf"))
        FONT, FONT_BOLD, FONT_MED = "Inter", "Inter-Bold", "Inter-Semi"
        FONT_MONO = "JBMono"
    except Exception:
        FONT, FONT_BOLD, FONT_MED, FONT_MONO = "Helvetica", "Helvetica-Bold", "Helvetica-Bold", "Courier"
    _FONT_READY = True
    return FONT, FONT_BOLD, FONT_MED, FONT_MONO


def doc_styles():
    f, fb, fm, mono = ensure_fonts()
    return {
        "h1": ParagraphStyle(
            "h1", fontName=fb, fontSize=16, textColor=INK, spaceBefore=4, spaceAfter=8, leading=20
        ),
        "h2": ParagraphStyle(
            "h2", fontName=fb, fontSize=12.5, textColor=BLUE, spaceBefore=10, spaceAfter=5, leading=16
        ),
        "h3": ParagraphStyle(
            "h3", fontName=fm, fontSize=10.5, textColor=INK, spaceBefore=7, spaceAfter=3, leading=13
        ),
        "body": ParagraphStyle(
            "body", fontName=f, fontSize=9.5, textColor=SLATE, alignment=TA_JUSTIFY, leading=13.2, spaceAfter=5
        ),
        "bullet": ParagraphStyle(
            "bullet", fontName=f, fontSize=9, textColor=SLATE, leading=12.4, leftIndent=8, spaceAfter=2
        ),
        "meta": ParagraphStyle(
            "meta", fontName=f, fontSize=8.5, textColor=MUTED, leading=11, spaceAfter=4
        ),
        "code": ParagraphStyle(
            "code", fontName=mono, fontSize=7.8, textColor=INK, leading=10.5, spaceAfter=1
        ),
        "callout": ParagraphStyle(
            "callout", fontName=f, fontSize=9, textColor=INK, leading=12.2
        ),
        "table_h": ParagraphStyle(
            "table_h", fontName=fb, fontSize=8, textColor=WHITE, leading=10
        ),
        "table_c": ParagraphStyle(
            "table_c", fontName=f, fontSize=7.8, textColor=SLATE, leading=10
        ),
        "toc_part": ParagraphStyle(
            "toc_part", fontName=fb, fontSize=11, textColor=INK, spaceBefore=8, spaceAfter=2
        ),
        "toc_item": ParagraphStyle(
            "toc_item", fontName=f, fontSize=9.5, textColor=SLATE, leading=13
        ),
        "cover_title": ParagraphStyle(
            "cover_title", fontName=fb, fontSize=26, textColor=INK, leading=32, alignment=TA_CENTER
        ),
        "module_title": ParagraphStyle(
            "module_title", fontName=fb, fontSize=11, textColor=WHITE, leading=14
        ),
    }


def slide_styles():
    f, fb, fm, mono = ensure_fonts()
    return {
        "eyebrow": ParagraphStyle(
            "eyebrow", fontName=fb, fontSize=10, textColor=BLUE, spaceAfter=8, leading=12,
            tracking=0.6,
        ),
        "h": ParagraphStyle(
            "h", fontName=fb, fontSize=26, textColor=INK, leading=30, spaceAfter=12
        ),
        "h2": ParagraphStyle(
            "h2", fontName=fb, fontSize=18, textColor=INK, leading=22, spaceAfter=8
        ),
        "body": ParagraphStyle(
            "body", fontName=f, fontSize=13, textColor=SLATE, leading=18, spaceAfter=6
        ),
        "bullet": ParagraphStyle(
            "bullet", fontName=f, fontSize=13, textColor=SLATE, leading=18, spaceAfter=4
        ),
        "small": ParagraphStyle(
            "small", fontName=f, fontSize=11, textColor=MUTED, leading=14
        ),
        "code": ParagraphStyle(
            "code", fontName=mono, fontSize=10.5, textColor=INK, leading=14, spaceAfter=2
        ),
        "card_title": ParagraphStyle(
            "card_title", fontName=fb, fontSize=11, textColor=BLUE, leading=14, spaceAfter=5
        ),
        "card_body": ParagraphStyle(
            "card_body", fontName=f, fontSize=11, textColor=SLATE, leading=15
        ),
        "white_title": ParagraphStyle(
            "white_title", fontName=fb, fontSize=28, textColor=WHITE, leading=34, alignment=TA_LEFT
        ),
        "white_sub": ParagraphStyle(
            "white_sub", fontName=f, fontSize=13, textColor=colors.HexColor("#DBEAFE"),
            leading=18, alignment=TA_LEFT
        ),
        "brand": ParagraphStyle(
            "brand", fontName=fb, fontSize=11, textColor=BLUE, alignment=TA_LEFT, spaceAfter=10
        ),
        "title_main": ParagraphStyle(
            "title_main", fontName=fb, fontSize=34, textColor=INK, leading=40, spaceAfter=8
        ),
        "title_sub": ParagraphStyle(
            "title_sub", fontName=f, fontSize=14, textColor=MUTED, leading=20, spaceAfter=10
        ),
        "meta_line": ParagraphStyle(
            "meta_line", fontName=f, fontSize=11, textColor=SLATE, leading=16, spaceAfter=2
        ),
        "agenda_num": ParagraphStyle(
            "agenda_num", fontName=fb, fontSize=16, textColor=BLUE, leading=20
        ),
        "agenda_item": ParagraphStyle(
            "agenda_item", fontName=f, fontSize=16, textColor=INK, leading=22, spaceAfter=8
        ),
        "section_num": ParagraphStyle(
            "section_num", fontName=fb, fontSize=64, textColor=BLUE, leading=68
        ),
        "section_title": ParagraphStyle(
            "section_title", fontName=fb, fontSize=32, textColor=INK, leading=38
        ),
        "table_h": ParagraphStyle(
            "table_h", fontName=fb, fontSize=11, textColor=WHITE, leading=14
        ),
        "table_c": ParagraphStyle(
            "table_c", fontName=f, fontSize=10.5, textColor=SLATE, leading=14
        ),
        "callout": ParagraphStyle(
            "callout", fontName=f, fontSize=12, textColor=INK, leading=16
        ),
        "example_label": ParagraphStyle(
            "example_label", fontName=fb, fontSize=11, textColor=BLUE, spaceAfter=4
        ),
        "tag": ParagraphStyle(
            "tag", fontName=fm, fontSize=9, textColor=BLUE, leading=11, alignment=TA_CENTER
        ),
    }

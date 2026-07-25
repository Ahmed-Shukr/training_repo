#!/usr/bin/env python3
"""Cookie Beamer replica theme — exact 16:9 Beamer page size and styling."""

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Exact Cookie palette sampled from the shared template
BLUE = colors.HexColor("#356AE6")
BLUE_DARK = colors.HexColor("#2F5BC2")
BLUE_SOFT = colors.HexColor("#A4BAEF")
BLUE_CHIP = colors.HexColor("#E8EEFB")
INK = colors.HexColor("#1F2937")
SLATE = colors.HexColor("#374151")
MUTED = colors.HexColor("#6B7280")
LINE = colors.HexColor("#D7DCE5")
SOFT = colors.HexColor("#F3F5F9")
BG = colors.HexColor("#FBFAF7")
FOOTER_BG = colors.HexColor("#F0F2F6")
WHITE = colors.white
CODE_BG = colors.HexColor("#F1F3F7")
ALERT = colors.HexColor("#DC2626")
ALERT_BG = colors.HexColor("#FEE2E2")
ALERT_HEAD = colors.HexColor("#FECACA")
EXAMPLE_BG = colors.HexColor("#ECFDF5")
EXAMPLE_HEAD = colors.HexColor("#A7F3D0")
EXAMPLE_FG = colors.HexColor("#047857")
PLAIN_BG = colors.HexColor("#EEF2FF")
PLAIN_HEAD = colors.HexColor("#C7D2FE")
WATERMARK = colors.HexColor("#E8ECF2")
ACCENT = ALERT
WARN_BG = ALERT_BG
TEAL = BLUE  # legacy
TEAL_LIGHT = BLUE_CHIP
NAVY = INK

# Exact Cookie Beamer page size from the uploaded PDF (points)
PAGE_W = 453.543
PAGE_H = 255.118

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
        pdfmetrics.registerFont(
            TTFont("NotoSC", "/usr/share/fonts/truetype/noto/NotoSans-SemiCondensed.ttf")
        )
        pdfmetrics.registerFont(
            TTFont("NotoSC-Bold", "/usr/share/fonts/truetype/noto/NotoSans-SemiCondensedBold.ttf")
        )
        pdfmetrics.registerFont(
            TTFont("NotoSC-Med", "/usr/share/fonts/truetype/noto/NotoSans-SemiCondensedMedium.ttf")
        )
        pdfmetrics.registerFont(
            TTFont("NotoSC-Semi", "/usr/share/fonts/truetype/noto/NotoSans-SemiCondensedSemiBold.ttf")
        )
        pdfmetrics.registerFont(
            TTFont("NotoMonoSC", "/usr/share/fonts/truetype/noto/NotoSansMono-SemiCondensed.ttf")
        )
        FONT, FONT_BOLD, FONT_MED = "NotoSC", "NotoSC-Bold", "NotoSC-Med"
        FONT_MONO = "NotoMonoSC"
    except Exception:
        FONT, FONT_BOLD, FONT_MED, FONT_MONO = "Helvetica", "Helvetica-Bold", "Helvetica-Bold", "Courier"
    _FONT_READY = True
    return FONT, FONT_BOLD, FONT_MED, FONT_MONO


def doc_styles():
    f, fb, fm, mono = ensure_fonts()
    return {
        "h1": ParagraphStyle("h1", fontName=fb, fontSize=16, textColor=INK, spaceBefore=4, spaceAfter=8, leading=20),
        "h2": ParagraphStyle("h2", fontName=fb, fontSize=12.5, textColor=BLUE, spaceBefore=10, spaceAfter=5, leading=16),
        "h3": ParagraphStyle("h3", fontName=fm, fontSize=10.5, textColor=INK, spaceBefore=7, spaceAfter=3, leading=13),
        "body": ParagraphStyle("body", fontName=f, fontSize=9.5, textColor=SLATE, alignment=TA_JUSTIFY, leading=13.2, spaceAfter=5),
        "bullet": ParagraphStyle("bullet", fontName=f, fontSize=9, textColor=SLATE, leading=12.4, leftIndent=8, spaceAfter=2),
        "meta": ParagraphStyle("meta", fontName=f, fontSize=8.5, textColor=MUTED, leading=11, spaceAfter=4),
        "code": ParagraphStyle("code", fontName=mono, fontSize=7.8, textColor=INK, leading=10.5, spaceAfter=1),
        "callout": ParagraphStyle("callout", fontName=f, fontSize=9, textColor=INK, leading=12.2),
        "table_h": ParagraphStyle("table_h", fontName=fb, fontSize=8, textColor=WHITE, leading=10),
        "table_c": ParagraphStyle("table_c", fontName=f, fontSize=7.8, textColor=SLATE, leading=10),
        "toc_part": ParagraphStyle("toc_part", fontName=fb, fontSize=11, textColor=INK, spaceBefore=8, spaceAfter=2),
        "toc_item": ParagraphStyle("toc_item", fontName=f, fontSize=9.5, textColor=SLATE, leading=13),
        "cover_title": ParagraphStyle("cover_title", fontName=fb, fontSize=26, textColor=INK, leading=32, alignment=TA_CENTER),
        "module_title": ParagraphStyle("module_title", fontName=fb, fontSize=11, textColor=WHITE, leading=14),
    }


def slide_styles():
    f, fb, fm, mono = ensure_fonts()
    return {
        "eyebrow": ParagraphStyle("eyebrow", fontName=fb, fontSize=7.5, textColor=BLUE, spaceAfter=2, leading=9),
        "sec_num": ParagraphStyle("sec_num", fontName=fb, fontSize=18, textColor=BLUE, leading=20),
        "h": ParagraphStyle("h", fontName=fb, fontSize=15, textColor=INK, leading=17, spaceAfter=1),
        "subtitle": ParagraphStyle("subtitle", fontName=f, fontSize=9, textColor=MUTED, leading=11, spaceAfter=4),
        "body": ParagraphStyle("body", fontName=f, fontSize=8.3, textColor=SLATE, leading=10.8, spaceAfter=2),
        "bullet": ParagraphStyle("bullet", fontName=f, fontSize=8.2, textColor=SLATE, leading=10.6, spaceAfter=1.5),
        "bullet2": ParagraphStyle("bullet2", fontName=f, fontSize=7.8, textColor=MUTED, leading=10, leftIndent=8, spaceAfter=1),
        "small": ParagraphStyle("small", fontName=f, fontSize=7.2, textColor=MUTED, leading=9),
        "code": ParagraphStyle("code", fontName=mono, fontSize=6.8, textColor=INK, leading=8.6, spaceAfter=0),
        "card_title": ParagraphStyle("card_title", fontName=fb, fontSize=7.2, textColor=BLUE, leading=9, spaceAfter=2),
        "card_body": ParagraphStyle("card_body", fontName=f, fontSize=7.6, textColor=SLATE, leading=9.6),
        "block_title": ParagraphStyle("block_title", fontName=fb, fontSize=8, textColor=INK, leading=10),
        "block_body": ParagraphStyle("block_body", fontName=f, fontSize=7.6, textColor=SLATE, leading=9.6),
        "brand": ParagraphStyle("brand", fontName=fb, fontSize=7, textColor=BLUE, spaceAfter=4),
        "title_main": ParagraphStyle("title_main", fontName=fb, fontSize=20, textColor=INK, leading=23, spaceAfter=3),
        "title_sub": ParagraphStyle("title_sub", fontName=fm, fontSize=9.5, textColor=MUTED, leading=12, spaceAfter=4),
        "meta_line": ParagraphStyle("meta_line", fontName=f, fontSize=8, textColor=SLATE, leading=10, spaceAfter=0.5),
        "meta_muted": ParagraphStyle("meta_muted", fontName=f, fontSize=7.5, textColor=MUTED, leading=9.5, spaceAfter=0.5),
        "agenda_num": ParagraphStyle("agenda_num", fontName=fb, fontSize=11, textColor=BLUE, leading=14),
        "agenda_item": ParagraphStyle("agenda_item", fontName=f, fontSize=11, textColor=INK, leading=14, spaceAfter=5),
        "section_num": ParagraphStyle("section_num", fontName=fb, fontSize=42, textColor=BLUE, leading=44),
        "section_title": ParagraphStyle("section_title", fontName=fb, fontSize=20, textColor=INK, leading=23),
        "table_h": ParagraphStyle("table_h", fontName=fb, fontSize=7.5, textColor=WHITE, leading=9),
        "table_c": ParagraphStyle("table_c", fontName=f, fontSize=7.2, textColor=SLATE, leading=9),
        "callout": ParagraphStyle("callout", fontName=f, fontSize=7.8, textColor=INK, leading=10),
        "example_label": ParagraphStyle("example_label", fontName=fb, fontSize=7.5, textColor=BLUE, spaceAfter=2),
        "tag": ParagraphStyle("tag", fontName=fm, fontSize=6.5, textColor=BLUE, leading=8, alignment=TA_CENTER),
        "footer": ParagraphStyle("footer", fontName=f, fontSize=6.5, textColor=MUTED, leading=8),
        "counter": ParagraphStyle("counter", fontName=fb, fontSize=6.5, textColor=WHITE, leading=8, alignment=TA_CENTER),
    }

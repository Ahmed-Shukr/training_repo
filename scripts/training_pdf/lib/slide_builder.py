#!/usr/bin/env python3
"""Helpers for landscape teaching presentation PDFs."""

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.platypus import (
    NextPageTemplate,
    PageBreak,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus import Frame, PageTemplate, BaseDocTemplate
from datetime import datetime

from reportlab.lib import colors

from .styles import (
    ACCENT,
    CODE_BG,
    LINE,
    MUTED,
    NAVY,
    SOFT,
    TEAL,
    TEAL_LIGHT,
    WARN_BG,
    WHITE,
    slide_styles,
)

PAGE_W, PAGE_H = landscape(A4)


def _fix_import():
    pass


# re-export styles getter
get_styles = slide_styles


def slide_chrome(c, doc, series="Odoo Full-Stack Training"):
    c.saveState()
    c.setFillColor(TEAL)
    c.rect(0, 0, 0.45 * cm, PAGE_H, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.rect(0, PAGE_H - 1.05 * cm, PAGE_W, 1.05 * cm, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica", 9)
    c.drawString(0.9 * cm, PAGE_H - 0.65 * cm, "Weblearns Academy")
    c.drawRightString(PAGE_W - 0.9 * cm, PAGE_H - 0.65 * cm, series)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.5)
    c.line(0.9 * cm, 0.85 * cm, PAGE_W - 0.9 * cm, 0.85 * cm)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawString(0.9 * cm, 0.45 * cm, "Senior Developer Lecture Materials")
    c.drawRightString(PAGE_W - 0.9 * cm, 0.45 * cm, f"{doc.page}")
    c.restoreState()


def title_bg(c, doc):
    c.saveState()
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(0, 0, PAGE_W, 1.35 * cm, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#123A4C"))
    c.circle(PAGE_W - 2 * cm, PAGE_H - 2 * cm, 6 * cm, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#9FB3BD"))
    c.setFont("Helvetica", 8)
    c.drawCentredString(PAGE_W / 2, 0.5 * cm, datetime.now().strftime("%B %Y"))
    c.restoreState()


def section_bg(c, doc):
    c.saveState()
    c.setFillColor(TEAL)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W * 0.36, PAGE_H, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica", 9)
    c.drawString(1 * cm, 0.55 * cm, f"Section  ·  {doc.page}")
    c.restoreState()


def make_doc(path, series, title):
    doc = BaseDocTemplate(
        path,
        pagesize=landscape(A4),
        leftMargin=1.0 * cm,
        rightMargin=1.0 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.25 * cm,
        title=title,
        author="Weblearns Academy",
    )
    frame = Frame(1.0 * cm, 1.15 * cm, PAGE_W - 2.0 * cm, PAGE_H - 2.55 * cm, id="body")
    full = Frame(0, 0, PAGE_W, PAGE_H, id="full")

    def chrome(c, d):
        slide_chrome(c, d, series)

    doc.addPageTemplates(
        [
            PageTemplate(id="Title", frames=full, onPage=title_bg),
            PageTemplate(id="Section", frames=full, onPage=section_bg),
            PageTemplate(id="Slide", frames=frame, onPage=chrome),
        ]
    )
    return doc


def bullets(s, items):
    return [Paragraph(f"-  {item}", s["bullet"]) for item in items]


def code_block(s, text):
    pre = Preformatted(text.strip("\n"), s["code"])
    t = Table([[pre]], colWidths=[PAGE_W - 2.4 * cm])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), CODE_BG),
                ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return t


def callout(s, text, title="Remember", warn=False):
    bg = WARN_BG if warn else TEAL_LIGHT
    border = ACCENT if warn else TEAL
    content = Paragraph(f"<b>{title}:</b> {text}", s["callout"])
    t = Table([[content]], colWidths=[PAGE_W - 2.4 * cm])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg),
                ("BOX", (0, 0), (-1, -1), 0.9, border),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return t


def cards(s, items, widths=None):
    n = len(items)
    if not widths:
        widths = [(PAGE_W - 2.4 * cm) / n] * n
    cols = []
    for i, (title, body) in enumerate(items):
        inner = Table(
            [[Paragraph(title, s["card_title"])], [Paragraph(body, s["card_body"])]],
            colWidths=[widths[i] - 0.3 * cm],
        )
        inner.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), SOFT),
                    ("BOX", (0, 0), (-1, -1), 0.8, TEAL),
                    ("LEFTPADDING", (0, 0), (-1, -1), 9),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                    ("TOPPADDING", (0, 0), (-1, -1), 7),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]
            )
        )
        cols.append(inner)
    row = Table([cols], colWidths=widths)
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return row


def simple_table(s, headers, rows, col_widths):
    data = [[Paragraph(h, s["table_h"]) for h in headers]]
    for r in rows:
        data.append([Paragraph(c, s["table_c"]) for c in r])
    t = Table(data, colWidths=col_widths)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, SOFT]),
                ("GRID", (0, 0), (-1, -1), 0.4, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return t


class Deck:
    def __init__(self, path, series, title, subtitle):
        self.doc = make_doc(path, series, title)
        self.s = slide_styles()
        self.story = []
        self.series = series
        self.title = title
        self.subtitle = subtitle

    def title_slide(self):
        self.story.append(NextPageTemplate("Title"))
        self.story.append(Spacer(1, 4.8 * cm))
        self.story.append(Paragraph(self.series.upper(), self.s["brand"]))
        self.story.append(Paragraph(self.title, self.s["white_title"]))
        self.story.append(Spacer(1, 0.35 * cm))
        self.story.append(Paragraph(self.subtitle, self.s["white_sub"]))

    def section(self, code, title, subtitle=""):
        self.story.append(NextPageTemplate("Section"))
        self.story.append(PageBreak())
        self.story.append(Spacer(1, 4.3 * cm))
        self.story.append(Paragraph(code, self.s["white_sub"]))
        self.story.append(Spacer(1, 0.25 * cm))
        self.story.append(Paragraph(title, self.s["white_title"]))
        if subtitle:
            self.story.append(Spacer(1, 0.35 * cm))
            self.story.append(Paragraph(subtitle, self.s["white_sub"]))

    def slide(self, eyebrow, heading, builder):
        self.story.append(NextPageTemplate("Slide"))
        self.story.append(PageBreak())
        self.story.append(Paragraph(eyebrow, self.s["eyebrow"]))
        self.story.append(Paragraph(heading, self.s["h"]))
        builder(self.story, self.s)

    def closing(self, line1="Practice the labs", line2="Then continue to the next module"):
        self.story.append(NextPageTemplate("Title"))
        self.story.append(PageBreak())
        self.story.append(Spacer(1, 4.5 * cm))
        self.story.append(Paragraph("NEXT STEP", self.s["white_sub"]))
        self.story.append(Spacer(1, 0.3 * cm))
        self.story.append(Paragraph(line1, self.s["white_title"]))
        self.story.append(Paragraph(line2, self.s["white_title"]))

    def build(self):
        self.doc.build(self.story)
        return self.doc.filename

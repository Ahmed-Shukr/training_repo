#!/usr/bin/env python3
"""Helpers for dense A4 documentation PDFs."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.pdfgen import canvas

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
    doc_styles,
)

PAGE_W, PAGE_H = A4
MARGIN = 1.6 * cm


def header_footer(c, doc, title="Odoo Full-Stack Developer Training Documentation"):
    c.saveState()
    c.setStrokeColor(TEAL)
    c.setLineWidth(1.8)
    c.line(MARGIN, PAGE_H - 1.0 * cm, PAGE_W - MARGIN, PAGE_H - 1.0 * cm)
    c.setFont("Helvetica", 8)
    c.setFillColor(MUTED)
    c.drawString(MARGIN, PAGE_H - 0.75 * cm, title)
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 0.75 * cm, "Training Documentation")
    c.setStrokeColor(LINE)
    c.setLineWidth(0.5)
    c.line(MARGIN, 1.15 * cm, PAGE_W - MARGIN, 1.15 * cm)
    c.setFillColor(MUTED)
    c.drawString(MARGIN, 0.7 * cm, "Weblearns Academy  |  Odoo 17 / 18 / 19")
    c.drawRightString(PAGE_W - MARGIN, 0.7 * cm, f"Page {doc.page}")
    c.restoreState()


def banner(styles, code, title):
    data = [[Paragraph(f"<b>{code}</b>&nbsp;&nbsp;&nbsp;{title}", styles["module_title"])]]
    t = Table(data, colWidths=[PAGE_W - 2 * MARGIN])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), TEAL),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return t


def callout(styles, text, title="Note", warn=False):
    bg = WARN_BG if warn else TEAL_LIGHT
    border = ACCENT if warn else TEAL
    content = Paragraph(f"<b>{title}:</b> {text}", styles["callout"])
    t = Table([[content]], colWidths=[PAGE_W - 2 * MARGIN])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg),
                ("BOX", (0, 0), (-1, -1), 0.8, border),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    return t


def bullets(styles, items):
    return [Paragraph(f"•  {item}", styles["bullet"]) for item in items]


def code_block(styles, text):
    # Escape for Paragraph-less Preformatted
    lines = text.strip("\n").splitlines()
    # Keep readable width
    content = "\n".join(lines)
    pre = Preformatted(content, styles["code"])
    t = Table([[pre]], colWidths=[PAGE_W - 2 * MARGIN])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), CODE_BG),
                ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return t


def simple_table(styles, headers, rows, col_widths=None):
    header_row = [Paragraph(h, styles["table_h"]) for h in headers]
    data = [header_row]
    for row in rows:
        data.append([Paragraph(str(c), styles["table_c"]) for c in row])
    if not col_widths:
        w = (PAGE_W - 2 * MARGIN) / len(headers)
        col_widths = [w] * len(headers)
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, SOFT]),
                ("GRID", (0, 0), (-1, -1), 0.35, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return t


def lesson_block(styles, title, paragraphs, points=None, example=None, example_title="Example", lab=None, tip=None):
    elems = [Paragraph(title, styles["h2"])]
    for p in paragraphs:
        elems.append(Paragraph(p, styles["body"]))
    if points:
        elems.extend(bullets(styles, points))
    if example:
        elems.append(Paragraph(example_title, styles["h3"]))
        elems.append(code_block(styles, example))
    if tip:
        elems.append(Spacer(1, 4))
        elems.append(callout(styles, tip, title="Senior tip"))
    if lab:
        elems.append(Paragraph(f"<b>Lab / Practice:</b> {lab}", styles["meta"]))
    elems.append(Spacer(1, 4))
    return elems


def hr():
    return HRFlowable(width="100%", thickness=0.8, color=TEAL, spaceBefore=2, spaceAfter=8)

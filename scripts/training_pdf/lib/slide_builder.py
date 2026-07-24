#!/usr/bin/env python3
"""Cookie-Beamer-inspired landscape teaching presentation helpers."""

from __future__ import annotations

from datetime import datetime

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)

from .styles import (
    ACCENT,
    BLUE,
    BLUE_DARK,
    BLUE_SOFT,
    CODE_BG,
    INK,
    LINE,
    MUTED,
    SLATE,
    SOFT,
    WARN_BG,
    WATERMARK,
    WHITE,
    ensure_fonts,
    slide_styles,
)

PAGE_W, PAGE_H = landscape(A4)
RAIL = 0.38 * cm


def slide_chrome(c, doc, series="Odoo Full-Stack Training", progress=None):
    """Content slide chrome: blue left rail + thin footer progress."""
    ensure_fonts()
    c.saveState()
    # Left rail
    c.setFillColor(BLUE)
    c.rect(0, 0, RAIL, PAGE_H, fill=1, stroke=0)

    # Subtle top rule
    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    c.line(1.1 * cm, PAGE_H - 0.85 * cm, PAGE_W - 1.0 * cm, PAGE_H - 0.85 * cm)

    # Footer series + page
    c.setFillColor(MUTED)
    c.setFont("Inter", 8)
    c.drawString(1.1 * cm, 0.55 * cm, series)
    c.drawRightString(PAGE_W - 1.0 * cm, 0.55 * cm, f"{doc.page}")

    # Progress bar
    total = getattr(doc, "total_slides", None) or max(doc.page, 1)
    frac = min(1.0, doc.page / float(total))
    bar_x, bar_w = 1.1 * cm, PAGE_W - 2.1 * cm
    c.setFillColor(LINE)
    c.roundRect(bar_x, 0.28 * cm, bar_w, 0.12 * cm, 1, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.roundRect(bar_x, 0.28 * cm, bar_w * frac, 0.12 * cm, 1, fill=1, stroke=0)
    c.restoreState()


def title_bg(c, doc):
    """Title slide with diagonal blue panel (Cookie-style)."""
    ensure_fonts()
    c.saveState()
    c.setFillColor(WHITE)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    # Diagonal blue wedge on the right
    c.setFillColor(BLUE)
    path = c.beginPath()
    path.moveTo(PAGE_W * 0.62, 0)
    path.lineTo(PAGE_W, 0)
    path.lineTo(PAGE_W, PAGE_H)
    path.lineTo(PAGE_W * 0.72, PAGE_H)
    path.close()
    c.drawPath(path, fill=1, stroke=0)

    # Soft inner panel shape
    c.setFillColor(BLUE_DARK)
    path2 = c.beginPath()
    path2.moveTo(PAGE_W * 0.78, PAGE_H * 0.18)
    path2.lineTo(PAGE_W * 0.96, PAGE_H * 0.12)
    path2.lineTo(PAGE_W * 0.96, PAGE_H * 0.78)
    path2.lineTo(PAGE_W * 0.74, PAGE_H * 0.86)
    path2.close()
    c.drawPath(path2, fill=1, stroke=0)

    # Decorative white mark on wedge
    c.setFillColor(WHITE)
    c.setFont("Inter-Bold", 42)
    c.drawCentredString(PAGE_W * 0.86, PAGE_H * 0.48, "WL")

    c.setFillColor(MUTED)
    c.setFont("Inter", 9)
    c.drawString(1.4 * cm, 0.7 * cm, datetime.now().strftime("%B %Y"))
    c.restoreState()


def section_bg(c, doc):
    """Section divider with left rail, blue dots, progress underline."""
    ensure_fonts()
    c.saveState()
    c.setFillColor(WHITE)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.rect(0, 0, RAIL, PAGE_H, fill=1, stroke=0)

    # Two blue dots top-right
    c.circle(PAGE_W - 1.6 * cm, PAGE_H - 1.3 * cm, 0.18 * cm, fill=1, stroke=0)
    c.circle(PAGE_W - 1.05 * cm, PAGE_H - 1.3 * cm, 0.18 * cm, fill=1, stroke=0)

    # Progress baseline
    c.setStrokeColor(LINE)
    c.setLineWidth(3)
    c.line(1.4 * cm, 3.2 * cm, PAGE_W - 1.4 * cm, 3.2 * cm)
    c.setStrokeColor(BLUE)
    c.setLineWidth(3)
    # partial blue accent on left of baseline
    c.line(1.4 * cm, 3.2 * cm, 5.5 * cm, 3.2 * cm)

    c.setFillColor(MUTED)
    c.setFont("Inter", 9)
    c.drawString(1.4 * cm, 1.0 * cm, f"Section  ·  {doc.page}")
    c.restoreState()


def agenda_bg(c, doc):
    ensure_fonts()
    c.saveState()
    c.setFillColor(WHITE)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.rect(0, 0, RAIL, PAGE_H, fill=1, stroke=0)

    # Giant TOC watermark
    c.setFillColor(WATERMARK)
    c.setFont("Inter-Bold", 120)
    c.drawRightString(PAGE_W - 0.8 * cm, PAGE_H * 0.28, "TOC")

    c.setFillColor(MUTED)
    c.setFont("Inter", 9)
    c.drawString(1.4 * cm, 0.7 * cm, f"{doc.page}")
    c.restoreState()


def make_doc(path, series, title, total_slides=200):
    ensure_fonts()
    doc = BaseDocTemplate(
        path,
        pagesize=landscape(A4),
        leftMargin=1.2 * cm,
        rightMargin=1.1 * cm,
        topMargin=1.3 * cm,
        bottomMargin=1.2 * cm,
        title=title,
        author="Weblearns Academy",
    )
    doc.total_slides = total_slides
    frame = Frame(1.2 * cm, 1.1 * cm, PAGE_W - 2.4 * cm, PAGE_H - 2.3 * cm, id="body")
    full = Frame(1.4 * cm, 1.0 * cm, PAGE_W - 2.8 * cm, PAGE_H - 2.0 * cm, id="full")
    title_frame = Frame(1.4 * cm, 1.5 * cm, PAGE_W * 0.55, PAGE_H - 3.0 * cm, id="title")

    def chrome(c, d):
        slide_chrome(c, d, series)

    doc.addPageTemplates(
        [
            PageTemplate(id="Title", frames=title_frame, onPage=title_bg),
            PageTemplate(id="Agenda", frames=full, onPage=agenda_bg),
            PageTemplate(id="Section", frames=full, onPage=section_bg),
            PageTemplate(id="Slide", frames=frame, onPage=chrome),
        ]
    )
    return doc


def bullets(s, items):
    out = []
    for item in items:
        out.append(Paragraph(f"<font color='#2563EB'><b>–</b></font>  {item}", s["bullet"]))
    return out


def code_block(s, text):
    pre = Preformatted(text.strip("\n"), s["code"])
    t = Table([[pre]], colWidths=[PAGE_W - 2.8 * cm])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), CODE_BG),
                ("BOX", (0, 0), (-1, -1), 0.7, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    return t


def callout(s, text, title="Remember", warn=False):
    bg = WARN_BG if warn else BLUE_SOFT
    border = ACCENT if warn else BLUE
    content = Paragraph(f"<b>{title}</b>  —  {text}", s["callout"])
    t = Table([[content]], colWidths=[PAGE_W - 2.8 * cm])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg),
                ("BOX", (0, 0), (-1, -1), 0, WHITE),
                ("LINEBEFORE", (0, 0), (0, -1), 4, border),
                ("LEFTPADDING", (0, 0), (-1, -1), 14),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    return t


def cards(s, items, widths=None):
    n = len(items)
    if not widths:
        widths = [(PAGE_W - 2.8 * cm) / n] * n
    cols = []
    for i, (title, body) in enumerate(items):
        inner = Table(
            [[Paragraph(title.upper(), s["card_title"])], [Paragraph(body, s["card_body"])]],
            colWidths=[widths[i] - 0.25 * cm],
        )
        inner.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), SOFT),
                    ("BOX", (0, 0), (-1, -1), 0.6, LINE),
                    ("LINEABOVE", (0, 0), (-1, 0), 3, BLUE),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                    ("TOPPADDING", (0, 0), (-1, -1), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]
            )
        )
        cols.append(inner)
    row = Table([cols], colWidths=widths)
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return row


def tags_row(s, labels):
    pills = []
    for label in labels:
        cell = Paragraph(label, s["tag"])
        t = Table([[cell]], colWidths=[2.6 * cm])
        t.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), BLUE_SOFT),
                    ("BOX", (0, 0), (-1, -1), 0, WHITE),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ]
            )
        )
        pills.append(t)
    row = Table([pills], colWidths=[2.9 * cm] * len(labels))
    row.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 2), ("RIGHTPADDING", (0, 0), (-1, -1), 2)]))
    return row


def simple_table(s, headers, rows, col_widths):
    data = [[Paragraph(h, s["table_h"]) for h in headers]]
    for r in rows:
        data.append([Paragraph(c, s["table_c"]) for c in r])
    t = Table(data, colWidths=col_widths)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), BLUE),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, SOFT]),
                ("GRID", (0, 0), (-1, -1), 0.4, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return t


def blue_rule():
    t = Table([[""]], colWidths=[2.2 * cm], rowHeights=[0.18 * cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), BLUE)]))
    return t


class Deck:
    def __init__(self, path, series, title, subtitle, author_lines=None, total_estimate=200):
        self.doc = make_doc(path, series, title, total_slides=total_estimate)
        self.s = slide_styles()
        self.story = []
        self.series = series
        self.title = title
        self.subtitle = subtitle
        self.author_lines = author_lines or [
            "Weblearns Academy",
            "Odoo Full-Stack Developer Program",
            "Senior Developer Lecture Materials",
        ]
        self._section_index = 0

    def title_slide(self):
        self.story.append(NextPageTemplate("Title"))
        self.story.append(Paragraph("A SMALL THEME FOR MODERN SLIDES", self.s["brand"]))
        self.story.append(Paragraph(self.title, self.s["title_main"]))
        self.story.append(Paragraph(self.subtitle, self.s["title_sub"]))
        self.story.append(Spacer(1, 0.15 * cm))
        self.story.append(blue_rule())
        self.story.append(Spacer(1, 0.45 * cm))
        for line in self.author_lines:
            self.story.append(Paragraph(line, self.s["meta_line"]))

    def agenda_slide(self, items):
        """items: list of strings"""
        self.story.append(NextPageTemplate("Agenda"))
        self.story.append(PageBreak())
        self.story.append(Spacer(1, 1.2 * cm))
        self.story.append(Paragraph("ROADMAP", self.s["eyebrow"]))
        self.story.append(Paragraph("Agenda", self.s["h"]))
        self.story.append(Spacer(1, 0.35 * cm))
        for i, item in enumerate(items, start=1):
            row = Table(
                [[
                    Paragraph(str(i), self.s["agenda_num"]),
                    Paragraph(item, self.s["agenda_item"]),
                ]],
                colWidths=[1.2 * cm, 14 * cm],
            )
            row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
            self.story.append(row)

    def section(self, number, title, subtitle=""):
        self._section_index = number
        self.story.append(NextPageTemplate("Section"))
        self.story.append(PageBreak())
        self.story.append(Spacer(1, 3.2 * cm))
        row = Table(
            [[
                Paragraph(str(number), self.s["section_num"]),
                Paragraph(title, self.s["section_title"]),
            ]],
            colWidths=[2.6 * cm, 20 * cm],
        )
        row.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ]
            )
        )
        self.story.append(row)
        if subtitle:
            self.story.append(Spacer(1, 0.45 * cm))
            self.story.append(Paragraph(subtitle, self.s["title_sub"]))

    def slide(self, eyebrow, heading, builder):
        self.story.append(NextPageTemplate("Slide"))
        self.story.append(PageBreak())
        self.story.append(Paragraph(eyebrow.upper(), self.s["eyebrow"]))
        self.story.append(Paragraph(heading, self.s["h"]))
        builder(self.story, self.s)

    def closing(self, line1="Practice the labs", line2="Then continue to the next module"):
        self.story.append(NextPageTemplate("Title"))
        self.story.append(PageBreak())
        self.story.append(Paragraph("NEXT STEP", self.s["brand"]))
        self.story.append(Paragraph(line1, self.s["title_main"]))
        self.story.append(Paragraph(line2, self.s["title_sub"]))
        self.story.append(Spacer(1, 0.2 * cm))
        self.story.append(blue_rule())
        self.story.append(Spacer(1, 0.5 * cm))
        self.story.append(Paragraph(self.series, self.s["meta_line"]))

    def build(self):
        # First pass estimate is fine; update total for progress bar after counting is hard
        # so we set a better estimate based on story length before build.
        # Rough: each PageBreak ~ one page.
        breaks = sum(1 for x in self.story if isinstance(x, PageBreak)) + 1
        self.doc.total_slides = max(breaks, 10)
        self.doc.build(self.story)
        return self.doc.filename

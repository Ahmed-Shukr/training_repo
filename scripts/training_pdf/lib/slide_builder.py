#!/usr/bin/env python3
"""Cookie Beamer replica slide helpers — compact 16:9 frames, dense layouts."""

from __future__ import annotations

from datetime import datetime

from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
    Flowable,
)

from .styles import (
    ALERT,
    ALERT_BG,
    ALERT_HEAD,
    BG,
    BLUE,
    BLUE_CHIP,
    BLUE_DARK,
    CODE_BG,
    EXAMPLE_BG,
    EXAMPLE_FG,
    EXAMPLE_HEAD,
    FOOTER_BG,
    INK,
    LINE,
    MUTED,
    PAGE_H,
    PAGE_W,
    PLAIN_BG,
    PLAIN_HEAD,
    SLATE,
    SOFT,
    WATERMARK,
    WHITE,
    ensure_fonts,
    slide_styles,
)

# Content frame margins matching Cookie density
ML, MR, MT, MB = 12, 12, 10, 22  # points


class ProgressDot(Flowable):
    def __init__(self, x_frac=0.15):
        Flowable.__init__(self)
        self.x_frac = x_frac
        self.width = PAGE_W - ML - MR
        self.height = 4

    def draw(self):
        self.canv.setStrokeColor(LINE)
        self.canv.setLineWidth(1)
        y = 2
        self.canv.line(0, y, self.width, y)
        x = self.width * self.x_frac
        self.canv.setFillColor(BLUE)
        self.canv.circle(x, y, 2.2, fill=1, stroke=0)
        self.canv.setStrokeColor(BLUE)
        self.canv.setLineWidth(1.6)
        self.canv.line(0, y, x, y)


def _footer(c, doc, left="Weblearns", mid="Cookie", right="Training"):
    ensure_fonts()
    c.saveState()
    # footer strip
    c.setFillColor(FOOTER_BG)
    c.rect(0, 0, PAGE_W, 14, fill=1, stroke=0)

    # progress line above footer
    c.setStrokeColor(LINE)
    c.setLineWidth(0.8)
    y = 16
    c.line(ML, y, PAGE_W - MR - 34, y)
    total = max(getattr(doc, "total_slides", 1) or 1, 1)
    frac = min(0.98, doc.page / float(total))
    x = ML + (PAGE_W - MR - 34 - ML) * frac
    c.setStrokeColor(BLUE)
    c.setLineWidth(1.5)
    c.line(ML, y, x, y)
    c.setFillColor(BLUE)
    c.circle(x, y, 2.0, fill=1, stroke=0)

    # footer labels
    c.setFillColor(MUTED)
    c.setFont("NotoSC", 6.2)
    c.drawString(ML, 4.5, left)
    c.drawCentredString(PAGE_W / 2 - 10, 4.5, mid)
    c.drawRightString(PAGE_W - MR - 38, 4.5, right)

    # counter box
    box_w, box_h = 32, 14
    c.setFillColor(BLUE)
    c.rect(PAGE_W - box_w, 0, box_w, box_h, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("NotoSC-Bold", 6.2)
    c.drawCentredString(PAGE_W - box_w / 2, 4.5, f"{doc.page} / {total}")
    c.restoreState()


def content_chrome(c, doc, meta=None):
    c.saveState()
    c.setFillColor(BG)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    meta = meta or {}
    _footer(
        c,
        doc,
        left=meta.get("left", "Weblearns"),
        mid=meta.get("mid", "Cookie"),
        right=meta.get("right", "Training"),
    )
    c.restoreState()


def title_bg(c, doc):
    ensure_fonts()
    c.saveState()
    c.setFillColor(BG)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    # Diagonal blue wedge (Cookie title art)
    c.setFillColor(BLUE)
    p = c.beginPath()
    p.moveTo(PAGE_W * 0.62, 0)
    p.lineTo(PAGE_W, 0)
    p.lineTo(PAGE_W, PAGE_H)
    p.lineTo(PAGE_W * 0.70, PAGE_H)
    p.close()
    c.drawPath(p, fill=1, stroke=0)

    # Darker inner polygon
    c.setFillColor(BLUE_DARK)
    p2 = c.beginPath()
    p2.moveTo(PAGE_W * 0.78, PAGE_H * 0.16)
    p2.lineTo(PAGE_W * 0.97, PAGE_H * 0.10)
    p2.lineTo(PAGE_W * 0.97, PAGE_H * 0.82)
    p2.lineTo(PAGE_W * 0.74, PAGE_H * 0.90)
    p2.close()
    c.drawPath(p2, fill=1, stroke=0)

    # Cookie-like mark
    cx, cy, r = PAGE_W * 0.86, PAGE_H * 0.48, 16
    c.setFillColor(WHITE)
    c.circle(cx, cy, r, fill=1, stroke=0)
    c.setFillColor(BLUE_DARK)
    for dx, dy in [(-5, 3), (4, 5), (-2, -5), (6, -2), (0, 1)]:
        c.circle(cx + dx, cy + dy, 2.0, fill=1, stroke=0)

    c.setFillColor(MUTED)
    c.setFont("NotoSC", 6.5)
    c.drawString(14, 8, datetime.now().strftime("%B %Y"))
    c.restoreState()


def agenda_bg(c, doc):
    ensure_fonts()
    c.saveState()
    c.setFillColor(BG)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    # left rail
    c.setFillColor(BLUE)
    c.rect(0, 0, 3.2, PAGE_H, fill=1, stroke=0)
    # TOC watermark
    c.setFillColor(WATERMARK)
    c.setFont("NotoSC-Bold", 72)
    c.drawRightString(PAGE_W - 8, 28, "TOC")
    _footer(c, doc, right="Agenda")
    c.restoreState()


def section_bg(c, doc):
    ensure_fonts()
    c.saveState()
    c.setFillColor(BG)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.rect(0, 0, 3.2, PAGE_H, fill=1, stroke=0)
    # dots
    c.circle(PAGE_W - 18, PAGE_H - 14, 2.2, fill=1, stroke=0)
    c.circle(PAGE_W - 10, PAGE_H - 14, 2.2, fill=1, stroke=0)
    # baseline with blue segment
    c.setStrokeColor(LINE)
    c.setLineWidth(2)
    c.line(16, 36, PAGE_W - 16, 36)
    c.setStrokeColor(BLUE)
    c.line(16, 36, 70, 36)
    _footer(c, doc, right="Section")
    c.restoreState()


def make_doc(path, series, title, total_slides=100, meta=None):
    ensure_fonts()
    doc = BaseDocTemplate(
        path,
        pagesize=(PAGE_W, PAGE_H),
        leftMargin=ML,
        rightMargin=MR,
        topMargin=MT,
        bottomMargin=MB,
        title=title,
        author="Weblearns Academy",
    )
    doc.total_slides = total_slides
    doc.cookie_meta = meta or {"left": "Weblearns", "mid": "Cookie", "right": series}

    body = Frame(ML, MB, PAGE_W - ML - MR, PAGE_H - MT - MB, id="body")
    full = Frame(14, MB, PAGE_W - 28, PAGE_H - MT - MB, id="full")
    title_frame = Frame(14, 20, PAGE_W * 0.58, PAGE_H - 40, id="title")

    def chrome(c, d):
        content_chrome(c, d, getattr(d, "cookie_meta", None))

    doc.addPageTemplates(
        [
            PageTemplate(id="Title", frames=title_frame, onPage=title_bg),
            PageTemplate(id="Agenda", frames=full, onPage=agenda_bg),
            PageTemplate(id="Section", frames=full, onPage=section_bg),
            PageTemplate(id="Slide", frames=body, onPage=chrome),
        ]
    )
    return doc


def bullets(s, items, style="bullet"):
    out = []
    for item in items:
        out.append(
            Paragraph(
                f"<font color='#356AE6'><b>–</b></font>&nbsp;&nbsp;{item}",
                s[style],
            )
        )
    return out


def numbered(s, items):
    out = []
    for i, item in enumerate(items, 1):
        out.append(Paragraph(f"<font color='#356AE6'><b>{i}.</b></font>  {item}", s["bullet"]))
    return out


def code_block(s, text, width=None):
    pre = Preformatted(text.strip("\n"), s["code"])
    w = width or (PAGE_W - ML - MR)
    t = Table([[pre]], colWidths=[w])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), CODE_BG),
                ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return t


def block(s, title, body, kind="plain", width=None):
    if kind == "alert":
        head_bg, body_bg, title_color = ALERT_HEAD, ALERT_BG, ALERT
    elif kind == "example":
        head_bg, body_bg, title_color = EXAMPLE_HEAD, EXAMPLE_BG, EXAMPLE_FG
    else:
        head_bg, body_bg, title_color = PLAIN_HEAD, PLAIN_BG, BLUE

    title_style = ParagraphStyle(
        "bt", parent=s["block_title"], textColor=title_color, fontSize=7.5
    )
    head = Paragraph(title, title_style)
    content = Paragraph(body, s["block_body"])
    w = width or ((PAGE_W - ML - MR - 8) / 2)
    t = Table([[head], [content]], colWidths=[w])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), head_bg),
                ("BACKGROUND", (0, 1), (-1, 1), body_bg),
                ("BOX", (0, 0), (-1, -1), 0.4, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return t


def cards(s, items, widths=None):
    n = len(items)
    avail = PAGE_W - ML - MR
    if not widths:
        widths = [avail / n] * n
    cols = []
    for i, (title, body) in enumerate(items):
        inner = Table(
            [[Paragraph(title.upper(), s["card_title"])], [Paragraph(body, s["card_body"])]],
            colWidths=[widths[i] - 4],
        )
        inner.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), SOFT),
                    ("BOX", (0, 0), (-1, -1), 0.4, LINE),
                    ("LINEABOVE", (0, 0), (-1, 0), 2, BLUE),
                    ("LEFTPADDING", (0, 0), (-1, -1), 5),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]
            )
        )
        cols.append(inner)
    row = Table([cols], colWidths=widths)
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 1), ("RIGHTPADDING", (0, 0), (-1, -1), 1)]))
    return row


def tags_row(s, labels):
    pills = []
    for label in labels:
        t = Table([[Paragraph(label, s["tag"])]], colWidths=[58])
        t.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), BLUE_CHIP),
                    ("TOPPADDING", (0, 0), (-1, -1), 2),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                    ("LEFTPADDING", (0, 0), (-1, -1), 4),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ]
            )
        )
        pills.append(t)
    return Table([pills], colWidths=[62] * len(labels))


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
                ("GRID", (0, 0), (-1, -1), 0.3, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return t


def header_row(s, number, title, subtitle=None):
    """Cookie content header: blue number + title (+ optional subtitle) + rule."""
    elems = []
    # Keep ID on one line (L01, DB01, VS12, ...)
    num_style = ParagraphStyle(
        "sec_num_fit",
        parent=s["sec_num"],
        fontSize=14 if len(str(number)) > 3 else 16,
        leading=16,
    )
    left = Paragraph(str(number), num_style)
    title_w = PAGE_W - ML - MR - 36
    if subtitle:
        right = Table(
            [[Paragraph(title, s["h"])], [Paragraph(subtitle, s["subtitle"])]],
            colWidths=[title_w],
        )
        right.setStyle(
            TableStyle(
                [
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                    ("TOPPADDING", (0, 0), (-1, -1), 0),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                ]
            )
        )
    else:
        right = Paragraph(title, s["h"])
    row = Table([[left, right]], colWidths=[34, title_w])
    row.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
            ]
        )
    )
    elems.append(row)
    rule = Table([[""]], colWidths=[PAGE_W - ML - MR], rowHeights=[0.7])
    rule.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LINE),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    elems.append(Spacer(1, 2))
    elems.append(rule)
    elems.append(Spacer(1, 3))
    return elems


def blue_rule(width=36):
    t = Table([[""]], colWidths=[width], rowHeights=[2.2])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), BLUE)]))
    return t


def two_col(left_flowables, right_flowables, gap=6):
    avail = PAGE_W - ML - MR
    lw = (avail - gap) / 2
    left = Table([[f] for f in left_flowables], colWidths=[lw])
    right = Table([[f] for f in right_flowables], colWidths=[lw])
    left.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 1)]))
    right.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 1)]))
    row = Table([[left, right]], colWidths=[lw, lw])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0)]))
    return row


class Deck:
    def __init__(self, path, series, title, subtitle, author_lines=None, total_estimate=120, section_name="Training"):
        self.doc = make_doc(
            path,
            series,
            title,
            total_slides=total_estimate,
            meta={"left": "Weblearns", "mid": "Cookie", "right": section_name},
        )
        self.s = slide_styles()
        self.story = []
        self.series = series
        self.title = title
        self.subtitle = subtitle
        self.section_name = section_name
        self.author_lines = author_lines or [
            "Weblearns Academy",
            "Odoo Full-Stack Developer Program",
            "Senior Developer Lecture Materials",
        ]
        self._frame_num = 0

    def title_slide(self):
        self.story.append(NextPageTemplate("Title"))
        self.story.append(Paragraph("A SMALL THEME FOR MODERN SLIDES", self.s["brand"]))
        self.story.append(Paragraph(self.title, self.s["title_main"]))
        self.story.append(Paragraph(self.subtitle, self.s["title_sub"]))
        self.story.append(Spacer(1, 2))
        self.story.append(blue_rule(40))
        self.story.append(Spacer(1, 8))
        for i, line in enumerate(self.author_lines):
            style = self.s["meta_line"] if i < 2 else self.s["meta_muted"]
            self.story.append(Paragraph(line, style))

    def agenda_slide(self, items):
        self.story.append(NextPageTemplate("Agenda"))
        self.story.append(PageBreak())
        self.story.append(Spacer(1, 8))
        self.story.append(Paragraph("ROADMAP", self.s["eyebrow"]))
        self.story.append(Paragraph("Agenda", self.s["h"]))
        self.story.append(Spacer(1, 8))
        for i, item in enumerate(items, start=1):
            row = Table(
                [[Paragraph(str(i), self.s["agenda_num"]), Paragraph(item, self.s["agenda_item"])]],
                colWidths=[16, 280],
            )
            row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
            self.story.append(row)

    def section(self, number, title, subtitle=""):
        self.story.append(NextPageTemplate("Section"))
        self.story.append(PageBreak())
        self.story.append(Spacer(1, 70))
        row = Table(
            [[Paragraph(str(number), self.s["section_num"]), Paragraph(title, self.s["section_title"])]],
            colWidths=[40, 320],
        )
        row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
        self.story.append(row)
        if subtitle:
            self.story.append(Spacer(1, 6))
            self.story.append(Paragraph(subtitle, self.s["title_sub"]))

    def slide(self, number, title, builder, subtitle=None):
        self.story.append(NextPageTemplate("Slide"))
        self.story.append(PageBreak())
        for el in header_row(self.s, number, title, subtitle):
            self.story.append(el)
        builder(self.story, self.s)

    def closing(self, line1="Practice the labs", line2="Then continue to the next module"):
        self.story.append(NextPageTemplate("Title"))
        self.story.append(PageBreak())
        self.story.append(Paragraph("NEXT STEP", self.s["brand"]))
        self.story.append(Paragraph(line1, self.s["title_main"]))
        self.story.append(Paragraph(line2, self.s["title_sub"]))
        self.story.append(Spacer(1, 2))
        self.story.append(blue_rule(40))
        self.story.append(Spacer(1, 8))
        self.story.append(Paragraph(self.series, self.s["meta_line"]))

    def build(self):
        # Overflow can create pages beyond explicit PageBreaks; pad the counter.
        breaks = sum(1 for x in self.story if isinstance(x, PageBreak)) + 1
        self.doc.total_slides = max(int(breaks * 1.4) + 5, breaks + 8)
        self.doc.build(self.story)
        return self.doc.filename

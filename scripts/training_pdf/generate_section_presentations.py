#!/usr/bin/env python3
"""Generate concise Merit Advisory lecture decks (one topic per slide)."""

from __future__ import annotations

import os
import sys
from datetime import datetime

from reportlab.platypus import Paragraph, Spacer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from training_pdf.lib.slide_builder import (  # noqa: E402
    Deck,
    ML,
    MR,
    bullets,
    code_block,
    two_col,
)
from training_pdf.lib.styles import PAGE_W  # noqa: E402
from training_pdf.content.slides_linux import SLIDES as LINUX  # noqa: E402
from training_pdf.content.slides_python import SLIDES as PYTHON  # noqa: E402
from training_pdf.content.slides_postgres import SLIDES as POSTGRES  # noqa: E402
from training_pdf.content.slides_odoo_core import SLIDES as ODOO  # noqa: E402
from training_pdf.content.slides_views_security import SLIDES as VIEWS  # noqa: E402
from training_pdf.content.slides_owl_pos import SLIDES as OWL  # noqa: E402
from training_pdf.content.slides_infra import SLIDES as INFRA  # noqa: E402

OUT_DIR = os.path.join(os.path.dirname(ROOT), "training_materials", "presentations")


DECKS = [
    {
        "file": "01_Linux_CLI_Mastery.pdf",
        "series": "01 · Linux",
        "section_name": "Linux",
        "title": "Linux OS & CLI Mastery",
        "subtitle": "Essential terminal commands for Odoo developers",
        "eyebrow": "Linux fundamentals for Odoo work",
        "slides": LINUX,
    },
    {
        "file": "02_Python_for_Odoo.pdf",
        "series": "02 · Python",
        "section_name": "Python",
        "title": "Python for Odoo Developers",
        "subtitle": "Core Python concepts used every day in Odoo",
        "eyebrow": "Python essentials for Odoo development",
        "slides": PYTHON,
    },
    {
        "file": "03_PostgreSQL_Database.pdf",
        "series": "03 · Database",
        "section_name": "Database",
        "title": "PostgreSQL for Odoo",
        "subtitle": "SQL, roles, indexes, and backup basics",
        "eyebrow": "PostgreSQL essentials for Odoo databases",
        "slides": POSTGRES,
    },
    {
        "file": "04_Odoo_Core_Development.pdf",
        "series": "04 · Odoo Core",
        "section_name": "Odoo Core",
        "title": "Odoo Core Development",
        "subtitle": "Install, modules, fields, and ORM basics",
        "eyebrow": "Odoo backend development essentials",
        "slides": ODOO,
    },
    {
        "file": "05_Views_Security_QWeb.pdf",
        "series": "05 · Views & Security",
        "section_name": "Views & Security",
        "title": "Views, Security & QWeb",
        "subtitle": "UI views, access rights, and report basics",
        "eyebrow": "Odoo views, security, and QWeb reports",
        "slides": VIEWS,
    },
    {
        "file": "06_OWL_POS_APIs.pdf",
        "series": "06 · OWL / POS / API",
        "section_name": "OWL / POS / API",
        "title": "OWL, POS & External APIs",
        "subtitle": "Frontend components, POS tweaks, and XML-RPC",
        "eyebrow": "OWL, Point of Sale, and integrations",
        "slides": OWL,
    },
    {
        "file": "07_Infrastructure_DevOps.pdf",
        "series": "07 · Infrastructure",
        "section_name": "Infrastructure",
        "title": "Infrastructure & DevOps",
        "subtitle": "Docker, VPS, Nginx, SSL, and workers",
        "eyebrow": "Deploy and operate Odoo in production",
        "slides": INFRA,
    },
]


def normalize_sections(raw_sections, chunk_size=7):
    """Regroup 1-topic sections into presentable Section 1..N blocks."""
    sizes = [len(s.get("topics") or []) for s in raw_sections]
    mostly_atomic = sizes and (sum(1 for n in sizes if n <= 1) >= max(1, int(0.6 * len(sizes))))
    if not mostly_atomic:
        # Keep provided grouping; renumber sequentially
        out = []
        for i, sec in enumerate(raw_sections, start=1):
            out.append(
                {
                    "section": i,
                    "title": sec.get("title") or f"Section {i}",
                    "topics": sec.get("topics") or [],
                }
            )
        return out

    topics = []
    for sec in raw_sections:
        topics.extend(sec.get("topics") or [])

    out = []
    for i in range(0, len(topics), chunk_size):
        chunk = topics[i : i + chunk_size]
        n = len(out) + 1
        # Title from first topic, shortened
        first = chunk[0]["title"]
        last = chunk[-1]["title"]
        title = first.split(" - ")[0].split(" — ")[0]
        if len(chunk) > 1:
            title = f"{title} to {last.split(' - ')[0].split(' — ')[0]}"
        out.append({"section": n, "title": title, "topics": chunk})
    return out


def topic_slide(deck: Deck, section_no: int, topic_index: int, topic: dict):
    """One clear beginner slide: short bullets + two examples."""
    number = f"{section_no}.{topic_index}"
    title = topic["title"]
    points = topic.get("points") or []
    examples = topic.get("examples") or []

    def builder(story, s):
        # Left: concise teaching points
        left = bullets(s, points[:4])
        # Right: two examples stacked
        right = []
        for ex in examples[:2]:
            right.append(Paragraph(ex.get("label") or "Example", s["example_label"]))
            code = (ex.get("code") or "").strip()
            # Keep examples short for readability
            lines = code.splitlines()
            if len(lines) > 6:
                code = "\n".join(lines[:6]) + "\n# ..."
            right.append(code_block(s, code, width=(PAGE_W - ML - MR - 8) / 2))
            right.append(Spacer(1, 3))
        if not right:
            right = [Paragraph("Follow along in your terminal.", s["body"])]
        story.append(two_col(left, right))

    deck.slide(number, title, builder)


def build_deck(spec):
    sections = normalize_sections(spec["slides"])
    path = os.path.join(OUT_DIR, spec["file"])
    topic_count = sum(len(s["topics"]) for s in sections)
    estimate = topic_count + len(sections) + 4

    deck = Deck(
        path,
        spec["series"],
        spec["title"],
        spec["subtitle"],
        author_lines=[
            "Merit Advisory",
            "Odoo Full-Stack Developer Program",
            "Beginner-friendly lecture materials",
            datetime.now().strftime("%B %Y"),
        ],
        total_estimate=estimate,
        section_name=spec["section_name"],
        eyebrow=spec.get("eyebrow") or spec["subtitle"],
    )

    deck.title_slide()

    # Improved agenda from actual sections
    agenda_items = []
    for sec in sections:
        n_topics = len(sec["topics"])
        agenda_items.append(
            (f"Section {sec['section']}: {sec['title']}", f"{n_topics} topics")
        )
    deck.agenda_slide(agenda_items, title="Agenda", eyebrow="What we will cover")

    for sec in sections:
        deck.section(
            sec["section"],
            f"Section {sec['section']}",
            sec["title"],
        )
        for idx, topic in enumerate(sec["topics"], start=1):
            topic_slide(deck, sec["section"], idx, topic)

    deck.closing("Try the examples on your machine", "Then open the next module deck")
    return deck.build()


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for spec in DECKS:
        path = build_deck(spec)
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()

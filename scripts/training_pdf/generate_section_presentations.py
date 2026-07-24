#!/usr/bin/env python3
"""Generate Cookie-Beamer-styled teaching decks per curriculum section."""

from __future__ import annotations

import os
import sys
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, Spacer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../scripts
sys.path.insert(0, ROOT)

from training_pdf.lib.slide_builder import (  # noqa: E402
    Deck,
    bullets,
    callout,
    cards,
    code_block,
    simple_table,
    tags_row,
)
from training_pdf.content.linux_lessons import LESSONS as LINUX  # noqa: E402
from training_pdf.content.python_lessons import LESSONS as PYTHON  # noqa: E402
from training_pdf.content.postgres_lessons import LESSONS as POSTGRES  # noqa: E402
from training_pdf.content.odoo_core_lessons import LESSONS as ODOO  # noqa: E402
from training_pdf.content.odoo_views_security_lessons import LESSONS as VIEWS  # noqa: E402
from training_pdf.content.owl_pos_api_lessons import LESSONS as OWL  # noqa: E402
from training_pdf.content.infra_lessons import LESSONS as INFRA  # noqa: E402

OUT_DIR = os.path.join(os.path.dirname(ROOT), "training_materials", "presentations")

DECKS = [
    {
        "file": "01_Linux_CLI_Mastery.pdf",
        "series": "Section 01 · Linux",
        "title": "Linux OS & CLI Mastery",
        "subtitle": "Modern lecture slides for Odoo server fluency",
        "lessons": LINUX,
        "agenda": [
            "Design the mental model: kernel, shell, services",
            "Navigate and manage files with precision",
            "Operate users, processes, systemd, and logs",
            "Secure SSH, firewall, and production layout",
        ],
        "tags": ["Ubuntu LTS", "CLI", "systemd", "SSH"],
    },
    {
        "file": "02_Python_for_Odoo.pdf",
        "series": "Section 02 · Python",
        "title": "Python for Odoo Developers",
        "subtitle": "Language foundations mapped to Odoo engineering work",
        "lessons": PYTHON,
        "agenda": [
            "Core syntax, types, and collections",
            "Control flow and clean functions",
            "OOP, functional tools, and errors",
            "Tooling: venv, pip, and debugging",
        ],
        "tags": ["Python 3", "OOP", "venv", "PEP 8"],
    },
    {
        "file": "03_PostgreSQL_Database.pdf",
        "series": "Section 03 · Database",
        "title": "PostgreSQL for Odoo",
        "subtitle": "SQL fluency, roles, indexes, and backup discipline",
        "lessons": POSTGRES,
        "agenda": [
            "Install, roles, grants, and configuration",
            "DDL, CRUD, joins, and aggregations",
            "Indexes, EXPLAIN, and lock awareness",
            "Dump, restore, and Odoo DB habits",
        ],
        "tags": ["PostgreSQL", "SQL", "Indexes", "Backup"],
    },
    {
        "file": "04_Odoo_Core_Development.pdf",
        "series": "Section 04 · Odoo Core",
        "title": "Odoo Core Development",
        "subtitle": "Install, modules, fields, ORM, and environments",
        "lessons": ODOO,
        "agenda": [
            "Install, CLI, and configuration",
            "Modules, manifests, and addons paths",
            "Field design and relational models",
            "ORM overrides and recordset APIs",
        ],
        "tags": ["Odoo 17", "ORM", "Fields", "CLI"],
    },
    {
        "file": "05_Views_Security_QWeb.pdf",
        "series": "Section 05 · Views & Security",
        "title": "Views, Security & QWeb",
        "subtitle": "Business UX, ACLs, data loading, and PDF reports",
        "lessons": VIEWS,
        "agenda": [
            "List, form, search, and kanban patterns",
            "Groups, access rights, and record rules",
            "XML/CSV data and view inheritance",
            "QWeb reports and automation hooks",
        ],
        "tags": ["Views", "Security", "XML", "QWeb"],
    },
    {
        "file": "06_OWL_POS_APIs.pdf",
        "series": "Section 06 · OWL / POS / API",
        "title": "OWL, POS & External APIs",
        "subtitle": "Reactive frontend, POS customization, XML-RPC",
        "lessons": OWL,
        "agenda": [
            "OWL components, state, and templates",
            "Patching, rpc, and custom widgets",
            "POS buttons, popups, and translations",
            "XML-RPC authentication and CRUD",
        ],
        "tags": ["OWL", "POS", "RPC", "XML-RPC"],
    },
    {
        "file": "07_Infrastructure_DevOps.pdf",
        "series": "Section 07 · Infrastructure",
        "title": "Infrastructure & DevOps",
        "subtitle": "Docker, VPS, Nginx/SSL, workers, and monitoring",
        "lessons": INFRA,
        "agenda": [
            "Containers and Compose for Odoo",
            "Hardened VPS and Nginx reverse proxy",
            "systemd, backups, and TLS",
            "Workers, indexes, and observability",
        ],
        "tags": ["Docker", "Nginx", "SSL", "Workers"],
    },
]


def chunk_text(paragraphs, max_chars=560):
    chunks, buf, size = [], [], 0
    for p in paragraphs:
        if size + len(p) > max_chars and buf:
            chunks.append(buf)
            buf, size = [p], len(p)
        else:
            buf.append(p)
            size += len(p)
    if buf:
        chunks.append(buf)
    return chunks or [[]]


def add_lesson_slides(deck: Deck, lesson: dict):
    lid = lesson["id"]
    title = lesson["title"]

    def objectives(story, s):
        story.extend(bullets(s, lesson.get("objectives") or ["Understand the topic"]))
        if lesson.get("lab"):
            story.append(Spacer(1, 0.3 * cm))
            story.append(callout(s, lesson["lab"], title="Lab target"))

    deck.slide(f"{lid} · Objectives", title, objectives)

    for i, paras in enumerate(chunk_text(lesson.get("explanation") or [], 600), start=1):
        def make_builder(ps):
            def builder(story, s):
                for p in ps:
                    story.append(Paragraph(p, s["body"]))
            return builder

        heading = title if i == 1 else f"{title} (continued)"
        deck.slide(f"{lid} · Teaching {i}", heading, make_builder(paras))

    kps = lesson.get("key_points") or []
    if kps:
        def keypoints(story, s):
            story.extend(bullets(s, kps))
        deck.slide(f"{lid} · Key points", "What to remember", keypoints)

    for idx, ex in enumerate(lesson.get("examples") or [], start=1):
        def make_ex(e, n):
            def builder(story, s):
                story.append(Paragraph(e.get("title") or f"Example {n}", s["example_label"]))
                if e.get("explain"):
                    story.append(Paragraph(e["explain"], s["body"]))
                if e.get("code"):
                    code = e["code"]
                    lines = code.splitlines()
                    if len(lines) > 14:
                        code = "\n".join(lines[:14]) + "\n# ... truncated for slide"
                    story.append(code_block(s, code))
            return builder
        deck.slide(f"{lid} · Example {idx}", ex.get("title") or title, make_ex(ex, idx))

    mistakes = lesson.get("common_mistakes") or []
    if mistakes:
        def mistakes_slide(story, s):
            story.extend(bullets(s, mistakes))
            story.append(Spacer(1, 0.25 * cm))
            story.append(
                callout(
                    s,
                    "Validate fixes in a disposable database before production.",
                    title="Caution",
                    warn=True,
                )
            )
        deck.slide(f"{lid} · Pitfalls", "Common mistakes", mistakes_slide)

    for extra in lesson.get("slide_extras") or []:
        kind = extra.get("kind")
        etitle = extra.get("title") or "Deep dive"

        def make_extra(ex=extra, k=kind):
            def builder(story, s):
                if k == "bullets":
                    story.extend(bullets(s, ex.get("items") or []))
                elif k == "code" and ex.get("code"):
                    story.append(code_block(s, ex["code"]))
                elif k == "callout":
                    story.append(callout(s, ex.get("text") or "", title=ex.get("title") or "Note"))
                elif k == "table" and ex.get("headers") and ex.get("rows"):
                    widths = [(26 * cm) / len(ex["headers"])] * len(ex["headers"])
                    story.append(simple_table(s, ex["headers"], ex["rows"], widths))
                else:
                    story.extend(bullets(s, ex.get("items") or [ex.get("text") or ""]))
            return builder

        deck.slide(f"{lid} · Extra", etitle, make_extra())


def build_deck(spec):
    path = os.path.join(OUT_DIR, spec["file"])
    estimate = max(80, len(spec["lessons"]) * 7)
    deck = Deck(
        path,
        spec["series"],
        spec["title"],
        spec["subtitle"],
        author_lines=[
            "Weblearns Academy",
            "Odoo Full-Stack Developer Program",
            "Senior Developer Lecture Materials",
            datetime_line(),
        ],
        total_estimate=estimate,
    )
    deck.title_slide()
    deck.agenda_slide(spec["agenda"])

    # Design system / method slide
    def method(story, s):
        story.append(
            cards(
                s,
                [
                    ("Pattern", "Objectives → teaching → examples → pitfalls → lab"),
                    ("Live coding", "Type commands with learners; freeze a reference commit"),
                    ("Safety", "Use disposable DBs; never demo sudo shortcuts in production"),
                ],
                [8.5 * cm, 8.5 * cm, 8.5 * cm],
            )
        )
        story.append(Spacer(1, 0.45 * cm))
        story.append(tags_row(s, spec.get("tags") or ["Training", "Odoo", "Labs"]))

    deck.slide("Method", "How this deck is taught", method)

    lessons = spec["lessons"]
    block = 0
    for i, lesson in enumerate(lessons):
        if i % 5 == 0:
            block += 1
            end = min(i + 5, len(lessons))
            deck.section(
                block,
                f"{lessons[i]['id']} – {lessons[end - 1]['id']}",
                f"{spec['title']} · teaching block {block}",
            )
        add_lesson_slides(deck, lesson)

    def summary(story, s):
        titles = [f"<b>{l['id']}</b>  {l['title']}" for l in lessons[:6]]
        more = len(lessons) - len(titles)
        items = titles + ([f"... and {more} more lessons in this deck"] if more > 0 else [])
        story.extend(bullets(s, items))
        story.append(Spacer(1, 0.3 * cm))
        story.append(callout(s, "Complete outstanding labs before starting the next section."))
        story.append(Spacer(1, 0.35 * cm))
        story.append(tags_row(s, spec.get("tags") or ["Done", "Labs", "Next"]))

    deck.slide("Wrap-up", "You should now be able to…", summary)
    deck.closing("Complete the section labs", "Open the next presentation deck")
    return deck.build()


def datetime_line():
    from datetime import datetime
    return datetime.now().strftime("%B %Y")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for spec in DECKS:
        path = build_deck(spec)
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()

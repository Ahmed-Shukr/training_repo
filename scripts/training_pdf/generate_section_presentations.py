#!/usr/bin/env python3
"""Generate separate professional teaching presentation decks per curriculum section."""

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
        "subtitle": "Senior lecture materials with commands, hardening, and Odoo server habits",
        "lessons": LINUX,
        "agenda": [
            ("Navigate", "Filesystem fluency and safe file operations"),
            ("Operate", "Users, processes, systemd, logs, packages"),
            ("Secure", "SSH, UFW, permissions, production layout"),
            ("Automate", "cron, env, troubleshooting checklists"),
        ],
    },
    {
        "file": "02_Python_for_Odoo.pdf",
        "series": "Section 02 · Python",
        "title": "Python for Odoo Developers",
        "subtitle": "Language fundamentals through OOP, FP, tooling—mapped to Odoo work",
        "lessons": PYTHON,
        "agenda": [
            ("Core", "Types, strings, collections, control flow"),
            ("Functions", "Scope, clean APIs, errors"),
            ("OOP/FP", "Classes, inheritance, decorators, generators"),
            ("Tooling", "venv, pip, debugging for Odoo"),
        ],
    },
    {
        "file": "03_PostgreSQL_Database.pdf",
        "series": "Section 03 · Database",
        "title": "PostgreSQL Administration & SQL",
        "subtitle": "Roles, SQL fluency, indexes, EXPLAIN, backups for Odoo databases",
        "lessons": POSTGRES,
        "agenda": [
            ("Setup", "Install, roles, grants, config files"),
            ("SQL", "DDL, CRUD, joins, aggregations"),
            ("Performance", "Indexes, EXPLAIN, locks"),
            ("Ops", "Dump/restore and Odoo DB habits"),
        ],
    },
    {
        "file": "04_Odoo_Core_Development.pdf",
        "series": "Section 04 · Odoo Core",
        "title": "Odoo Core Development",
        "subtitle": "Install, modules, fields, ORM methods, environments, special commands",
        "lessons": ODOO,
        "agenda": [
            ("Platform", "Install, CLI, configuration, IDE"),
            ("Modules", "Scaffold, manifest, addons paths"),
            ("Fields", "Scalar, relational, compute, binary"),
            ("ORM", "Overrides, search APIs, recordset helpers"),
        ],
    },
    {
        "file": "05_Views_Security_QWeb.pdf",
        "series": "Section 05 · Views & Security",
        "title": "Views, Security, Data & QWeb",
        "subtitle": "UX views, ACLs/rules, XML/CSV data, inheritance, reports, automation",
        "lessons": VIEWS,
        "agenda": [
            ("Views", "List, form, search, kanban, analytics"),
            ("Security", "Groups, ACLs, record rules, Odoo 19"),
            ("Data", "XML/CSV loading and inheritance"),
            ("QWeb", "PDF reports, sequences, server actions"),
        ],
    },
    {
        "file": "06_OWL_POS_APIs.pdf",
        "series": "Section 06 · OWL / POS / API",
        "title": "OWL Frontend, POS & APIs",
        "subtitle": "Reactive OWL, POS customization, XML-RPC integrations",
        "lessons": OWL,
        "agenda": [
            ("OWL", "Components, state, templates, patch, rpc"),
            ("POS", "Buttons, popups, translations, order utils"),
            ("API", "XML-RPC auth and CRUD"),
            ("Practice", "Postman workflows and labs"),
        ],
    },
    {
        "file": "07_Infrastructure_DevOps.pdf",
        "series": "Section 07 · Infrastructure",
        "title": "Infrastructure, Docker & Performance",
        "subtitle": "Containers, VPS, Nginx/SSL, systemd, workers, monitoring",
        "lessons": INFRA,
        "agenda": [
            ("Docker", "Images, Compose, volumes, upgrades"),
            ("VPS", "Hardening, Nginx, longpolling, Certbot"),
            ("Runtime", "systemd and backup automation"),
            ("Scale", "Workers, indexes, Redis, observability"),
        ],
    },
]


def chunk_text(paragraphs, max_chars=520):
    """Group paragraphs into slide-sized chunks."""
    chunks = []
    buf = []
    size = 0
    for p in paragraphs:
        if size + len(p) > max_chars and buf:
            chunks.append(buf)
            buf = [p]
            size = len(p)
        else:
            buf.append(p)
            size += len(p)
    if buf:
        chunks.append(buf)
    return chunks or [[]]


def add_lesson_slides(deck: Deck, lesson: dict):
    lid = lesson["id"]
    title = lesson["title"]

    # 1) Objectives
    def objectives(story, s):
        story.extend(bullets(s, lesson.get("objectives") or ["Understand the topic"]))
        if lesson.get("lab"):
            story.append(Spacer(1, 0.25 * cm))
            story.append(callout(s, lesson["lab"], title="Lab target"))

    deck.slide(f"{lid} · OBJECTIVES", title, objectives)

    # 2+) Explanation chunks
    for i, paras in enumerate(chunk_text(lesson.get("explanation") or [], 580), start=1):
        def make_builder(ps):
            def builder(story, s):
                for p in ps:
                    story.append(Paragraph(p, s["body"]))
            return builder
        deck.slide(f"{lid} · TEACHING {i}", title if i == 1 else f"{title} (continued)", make_builder(paras))

    # Key points
    kps = lesson.get("key_points") or []
    if kps:
        def keypoints(story, s):
            story.extend(bullets(s, kps))
        deck.slide(f"{lid} · KEY POINTS", "What to remember", keypoints)

    # Examples
    for idx, ex in enumerate(lesson.get("examples") or [], start=1):
        def make_ex(e, n):
            def builder(story, s):
                story.append(Paragraph(e.get("title") or f"Example {n}", s["example_label"]))
                if e.get("explain"):
                    story.append(Paragraph(e["explain"], s["body"]))
                if e.get("code"):
                    # Truncate extremely long code for slide readability
                    code = e["code"]
                    lines = code.splitlines()
                    if len(lines) > 16:
                        code = "\n".join(lines[:16]) + "\n# ... truncated for slide"
                    story.append(code_block(s, code))
            return builder
        deck.slide(f"{lid} · EXAMPLE {idx}", ex.get("title") or title, make_ex(ex, idx))

    # Mistakes
    mistakes = lesson.get("common_mistakes") or []
    if mistakes:
        def mistakes_slide(story, s):
            story.extend(bullets(s, mistakes))
            story.append(Spacer(1, 0.2 * cm))
            story.append(callout(s, "Validate fixes in a disposable database before production.", warn=True))
        deck.slide(f"{lid} · PITFALLS", "Common mistakes", mistakes_slide)

    # slide extras
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
                    widths = [(26.5 * cm) / len(ex["headers"]) ] * len(ex["headers"])
                    story.append(simple_table(s, ex["headers"], ex["rows"], widths))
                else:
                    story.extend(bullets(s, ex.get("items") or [ex.get("text") or ""]))
            return builder

        deck.slide(f"{lid} · EXTRA", etitle, make_extra())


def build_deck(spec):
    path = os.path.join(OUT_DIR, spec["file"])
    deck = Deck(path, spec["series"], spec["title"], spec["subtitle"])
    deck.title_slide()

    # Agenda
    agenda = spec["agenda"]

    def agenda_builder(story, s):
        story.append(cards(s, agenda, [6.7 * cm] * len(agenda)))
        story.append(Spacer(1, 0.35 * cm))
        story.append(
            Paragraph(
                f"{len(spec['lessons'])} lessons · explanations · examples · labs",
                s["small"],
            )
        )

    deck.slide("AGENDA", "What this section teaches", agenda_builder)

    # How to use
    def how_to(story, s):
        story.extend(
            bullets(
                s,
                [
                    "Each lesson starts with objectives, then teaching narrative",
                    "Code/command slides are meant to be typed live or in labs",
                    "Pitfall slides capture production failure modes",
                    "Use the matching documentation part for full prose depth",
                ],
            )
        )
        story.append(Spacer(1, 0.25 * cm))
        story.append(
            callout(
                s,
                "These are lecture materials—pause for learner typing time after every example.",
                title="Facilitation",
            )
        )

    deck.slide("METHOD", "How to teach and learn this deck", how_to)

    # Group lessons into chapter section dividers every ~5 lessons
    lessons = spec["lessons"]
    for i, lesson in enumerate(lessons):
        if i % 5 == 0:
            end = min(i + 5, len(lessons))
            first = lessons[i]["id"]
            last = lessons[end - 1]["id"]
            deck.section(
                f"LESSONS {first}–{last}",
                spec["title"],
                f"Teaching block {i // 5 + 1}",
            )
        add_lesson_slides(deck, lesson)

    # Section summary
    def summary(story, s):
        titles = [f"{l['id']} {l['title']}" for l in lessons[:8]]
        more = len(lessons) - len(titles)
        items = titles + ([f"... and {more} more lessons in this deck"] if more > 0 else [])
        story.extend(bullets(s, items))
        story.append(Spacer(1, 0.2 * cm))
        story.append(callout(s, "Complete outstanding labs before starting the next section."))

    deck.slide("SECTION WRAP", "You should now be able to…", summary)
    deck.closing("Complete the section labs", "Then open the next presentation deck")
    return deck.build()


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    written = []
    for spec in DECKS:
        path = build_deck(spec)
        written.append(path)
        print(f"Wrote {path}")
    return written


if __name__ == "__main__":
    main()

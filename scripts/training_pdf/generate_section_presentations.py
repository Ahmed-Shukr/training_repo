#!/usr/bin/env python3
"""Generate Cookie-Beamer exact-size dense teaching decks."""

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
    block,
    bullets,
    cards,
    code_block,
    numbered,
    simple_table,
    tags_row,
    two_col,
)
from training_pdf.lib.styles import PAGE_W  # noqa: E402
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
        "section_name": "Linux",
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
        "section_name": "Python",
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
        "section_name": "Database",
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
        "section_name": "Odoo Core",
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
        "section_name": "Views & Security",
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
        "section_name": "OWL / POS / API",
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
        "section_name": "Infrastructure",
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


def _clip(text, n=420):
    text = (text or "").strip()
    if len(text) <= n:
        return text
    return text[: n - 1].rsplit(" ", 1)[0] + "…"


def _code_trim(code, max_lines=11):
    lines = (code or "").strip("\n").splitlines()
    if len(lines) > max_lines:
        return "\n".join(lines[:max_lines]) + "\n# ..."
    return "\n".join(lines)


def add_lesson_slides(deck: Deck, lesson: dict, frame_prefix: str):
    """Dense Cookie frames: pack related content; avoid sparse slides."""
    lid = lesson["id"]
    title = lesson["title"]
    number = lid.replace("L", "").replace("P", "").replace("DB", "").replace("O", "").replace("VS", "").replace("W", "").replace("I", "")
    # Keep readable section number like 1.1 / L01
    num_label = lid

    objectives = lesson.get("objectives") or []
    keypoints = lesson.get("key_points") or []
    explanation = lesson.get("explanation") or []
    examples = lesson.get("examples") or []
    mistakes = lesson.get("common_mistakes") or []
    lab = lesson.get("lab") or ""

    # Frame A: Objectives | Key points (two columns) + compact lab
    def frame_overview(story, s):
        left = [Paragraph("<b>Objectives</b>", s["card_title"])] + bullets(
            s, [_clip(o, 95) for o in objectives[:4]]
        )
        right = [Paragraph("<b>Key points</b>", s["card_title"])] + bullets(
            s, [_clip(k, 95) for k in keypoints[:5]]
        )
        story.append(two_col(left, right))
        if lab:
            story.append(Spacer(1, 3))
            story.append(
                block(s, "Lab target", _clip(lab, 220), kind="example", width=PAGE_W - ML - MR)
            )

    deck.slide(num_label, title, frame_overview, subtitle="Objectives, key points, and lab target")

    # Frame B: Teaching packed into ONE frame (no orphan overflow pages)
    def frame_teach(story, s):
        chunks = []
        for p in explanation[:3]:
            chunks.append(Paragraph(_clip(p, 480), s["body"]))
        if len(explanation) > 3:
            chunks.append(Paragraph("<b>Also remember</b>", s["card_title"]))
            chunks.extend(bullets(s, [_clip(p, 120) for p in explanation[3:5]]))
        # KeepTogether prevents a lonely overflow frame
        from reportlab.platypus import KeepTogether
        story.append(KeepTogether(chunks))

    if explanation:
        deck.slide(num_label, title, frame_teach, subtitle="Teaching notes")

    # Frame C: Example code + pitfalls as Cookie blocks
    def frame_practice(story, s):
        ex = examples[0] if examples else None
        left_bits = []
        if ex:
            left_bits.append(Paragraph(ex.get("title") or "Worked example", s["example_label"]))
            if ex.get("explain"):
                left_bits.append(Paragraph(_clip(ex["explain"], 180), s["body"]))
            if ex.get("code"):
                left_bits.append(code_block(s, _code_trim(ex["code"], 10), width=(PAGE_W - ML - MR - 8) / 2))
        else:
            left_bits.append(Paragraph("No code sample for this lesson — use the lab.", s["body"]))

        right_bits = []
        if mistakes:
            right_bits.append(
                block(
                    s,
                    "Common mistakes",
                    "<br/>".join(f"• {_clip(m, 90)}" for m in mistakes[:4]),
                    kind="alert",
                    width=(PAGE_W - ML - MR - 8) / 2,
                )
            )
        if len(examples) > 1 and examples[1].get("code"):
            right_bits.append(Spacer(1, 3))
            right_bits.append(Paragraph(examples[1].get("title") or "More", s["example_label"]))
            right_bits.append(code_block(s, _code_trim(examples[1]["code"], 7), width=(PAGE_W - ML - MR - 8) / 2))

        story.append(two_col(left_bits, right_bits or [Paragraph(" ", s["body"])]))

    if examples or mistakes:
        deck.slide(num_label, title, frame_practice, subtitle="Example and pitfalls")

    # Optional extras compacted into one frame
    extras = lesson.get("slide_extras") or []
    if extras:
        def frame_extra(story, s):
            cols = []
            for ex in extras[:3]:
                kind = ex.get("kind")
                title_e = ex.get("title") or "Note"
                if kind == "code" and ex.get("code"):
                    cols.append(
                        block(s, title_e, f"<font face='NotoMonoSC' size='6'>{_clip(ex['code'].replace(chr(10), ' / '), 160)}</font>", kind="plain")
                    )
                elif kind == "callout":
                    cols.append(block(s, title_e, _clip(ex.get("text") or "", 180), kind="plain"))
                else:
                    items = ex.get("items") or [ex.get("text") or ""]
                    cols.append(block(s, title_e, "<br/>".join(f"• {_clip(i, 70)}" for i in items[:4]), kind="plain"))
            if len(cols) == 1:
                story.append(cols[0])
            elif len(cols) == 2:
                story.append(two_col([cols[0]], [cols[1]]))
            else:
                avail = PAGE_W - ML - MR
                w = avail / 3
                from reportlab.platypus import Table, TableStyle
                row = Table([cols], colWidths=[w] * 3)
                row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
                story.append(row)

        deck.slide(num_label, title, frame_extra, subtitle="Extra patterns")


def build_deck(spec):
    path = os.path.join(OUT_DIR, spec["file"])
    estimate = max(40, len(spec["lessons"]) * 3 + 8)
    deck = Deck(
        path,
        spec["series"],
        spec["title"],
        spec["subtitle"],
        author_lines=[
            "Weblearns Academy",
            "weblearns@training.local",
            "Odoo Full-Stack Developer Program",
            f"Lecture materials / {datetime.now().strftime('%B %Y')}",
        ],
        total_estimate=estimate,
        section_name=spec.get("section_name", "Training"),
    )
    deck.title_slide()
    deck.agenda_slide(spec["agenda"])

    def method(story, s):
        story.append(
            cards(
                s,
                [
                    ("Awesome-style frame", "Number rails, angled title art, and section slides are built in."),
                    ("Metropolis defaults", "Progress bars, block styles, and fonts are set from theme options."),
                    ("Dense teaching", "Two-column frames pack objectives, examples, and pitfalls."),
                ],
            )
        )
        story.append(Spacer(1, 6))
        story.append(tags_row(s, spec.get("tags") or ["Training", "Odoo", "Labs"]))

    deck.slide("1", "A theme for modern talks", method, subtitle="How this deck is taught")

    lessons = spec["lessons"]
    block_i = 0
    for i, lesson in enumerate(lessons):
        if i % 5 == 0:
            block_i += 1
            end = min(i + 5, len(lessons))
            deck.section(
                block_i,
                f"{lessons[i]['id']} – {lessons[end - 1]['id']}",
                f"{spec['title']} · teaching block {block_i}",
            )
        add_lesson_slides(deck, lesson, frame_prefix=str(block_i))

    def summary(story, s):
        left = bullets(s, [f"<b>{l['id']}</b>  {l['title']}" for l in lessons[:8]])
        right = bullets(
            s,
            [
                "Complete every lab before the next section",
                "Keep a command/error journal",
                "Prefer disposable databases for experiments",
                "Re-read pitfalls before production changes",
            ],
        )
        story.append(two_col(left, right))
        story.append(Spacer(1, 5))
        story.append(tags_row(s, spec.get("tags") or ["Done", "Labs", "Next"]))

    deck.slide("Σ", "You should now be able to…", summary, subtitle="Section wrap-up")
    deck.closing("Complete the section labs", "Open the next presentation deck")
    return deck.build()


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for spec in DECKS:
        path = build_deck(spec)
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()

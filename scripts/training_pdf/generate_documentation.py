#!/usr/bin/env python3
"""Generate the full ~150+ page Odoo Full-Stack Training Documentation PDF."""

from __future__ import annotations

import os
import sys
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../scripts
sys.path.insert(0, ROOT)

from training_pdf.lib.doc_builder import (  # noqa: E402
    MARGIN,
    PAGE_H,
    PAGE_W,
    banner,
    bullets,
    callout,
    code_block,
    header_footer,
    hr,
    simple_table,
)
from training_pdf.lib.styles import NAVY, TEAL, TEAL_LIGHT, MUTED, SLATE, doc_styles  # noqa: E402
from training_pdf.content.linux_lessons import LESSONS as LINUX  # noqa: E402
from training_pdf.content.python_lessons import LESSONS as PYTHON  # noqa: E402
from training_pdf.content.postgres_lessons import LESSONS as POSTGRES  # noqa: E402
from training_pdf.content.odoo_core_lessons import LESSONS as ODOO  # noqa: E402
from training_pdf.content.odoo_views_security_lessons import LESSONS as VIEWS  # noqa: E402
from training_pdf.content.owl_pos_api_lessons import LESSONS as OWL  # noqa: E402
from training_pdf.content.infra_lessons import LESSONS as INFRA  # noqa: E402

OUTPUT = os.path.join(
    os.path.dirname(ROOT),
    "training_materials",
    "Odoo_FullStack_Training_Documentation.pdf",
)

PARTS = [
    ("Part A", "Program Framework", None, "overview"),
    ("Part B", "Linux Operating System & CLI Mastery", LINUX, "linux"),
    ("Part C", "Python Programming for Odoo Developers", PYTHON, "python"),
    ("Part D", "PostgreSQL Database Administration", POSTGRES, "postgres"),
    ("Part E", "Odoo Core Development (Models, Fields, ORM)", ODOO, "odoo"),
    ("Part F", "Views, Security, Data & QWeb", VIEWS, "odoo_views"),
    ("Part G", "OWL Frontend, POS & External APIs", OWL, "owl"),
    ("Part H", "Infrastructure, Docker, VPS & Performance", INFRA, "infra"),
]


def cover_page(c, doc):
    c.saveState()
    c.setFillColor(NAVY)
    c.rect(0, 0, 3.0 * cm, PAGE_H, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(3.0 * cm, 0, 0.32 * cm, PAGE_H, fill=1, stroke=0)
    c.setFillColor(TEAL_LIGHT)
    c.rect(3.32 * cm, PAGE_H - 4.2 * cm, PAGE_W - 3.32 * cm, 4.2 * cm, fill=1, stroke=0)

    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(4.3 * cm, PAGE_H - 2.0 * cm, "COMPLETE TRAINING DOCUMENTATION")

    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 24)
    y = PAGE_H - 6.5 * cm
    for line in ["Odoo Full-Stack", "Developer Program", "Documentation"]:
        c.drawString(4.3 * cm, y, line)
        y -= 0.95 * cm

    c.setFillColor(SLATE)
    c.setFont("Helvetica", 11)
    c.drawString(4.3 * cm, y - 0.2 * cm, "Detailed explanations, plans, examples, and labs")

    box_y = 5.8 * cm
    c.setFillColor(TEAL_LIGHT)
    c.roundRect(4.3 * cm, box_y, 13.2 * cm, 5.8 * cm, 5, fill=1, stroke=0)
    info = [
        ("Scope", "Linux · Python · PostgreSQL · Odoo · OWL · Infra"),
        ("Depth", "Lesson-by-lesson teaching documentation"),
        ("Target Length", "~150+ pages of full-page content"),
        ("Versions", "Odoo 17 core · Odoo 18/19 deltas"),
        ("Edition", datetime.now().strftime("%B %Y")),
        ("Companion", "Per-section presentation decks"),
    ]
    iy = box_y + 5.1 * cm
    for label, value in info:
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(TEAL)
        c.drawString(4.8 * cm, iy, label)
        c.setFont("Helvetica", 9)
        c.setFillColor(SLATE)
        c.drawString(8.5 * cm, iy, value)
        iy -= 0.75 * cm

    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawString(4.3 * cm, 2.0 * cm, "Weblearns Academy  |  Senior-developer lecture documentation")
    c.restoreState()


def add_overview(story, styles):
    story.append(banner(styles, "A", "Program Framework & How to Use This Document"))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Purpose", styles["h2"]))
    story.append(
        Paragraph(
            "This document is the complete written curriculum for the Odoo Full-Stack Developer "
            "Program. Unlike a short syllabus, every major topic is explained in teaching depth: "
            "why it matters, how seniors apply it, concrete examples, common mistakes, and a lab. "
            "Use it as the source of truth for self-study, instructor delivery, and review before "
            "capstone work.",
            styles["body"],
        )
    )
    story.append(Paragraph("Document Structure", styles["h2"]))
    story.append(
        Paragraph(
            "Parts B through H map one-to-one with the separate presentation decks. Study a "
            "documentation part, then reinforce with that section's slide deck. Each lesson follows "
            "the same pedagogical pattern so you always know what to expect.",
            styles["body"],
        )
    )
    story.append(
        simple_table(
            styles,
            ["Part", "Domain", "Presentation Deck"],
            [
                ["B", "Linux & CLI", "01_Linux_CLI_Mastery.pdf"],
                ["C", "Python for Odoo", "02_Python_for_Odoo.pdf"],
                ["D", "PostgreSQL", "03_PostgreSQL_Database.pdf"],
                ["E", "Odoo Core (ORM/Fields)", "04_Odoo_Core_Development.pdf"],
                ["F", "Views, Security, QWeb", "05_Views_Security_QWeb.pdf"],
                ["G", "OWL, POS, APIs", "06_OWL_POS_APIs.pdf"],
                ["H", "Infra & Performance", "07_Infrastructure_DevOps.pdf"],
            ],
            [2.2 * cm, 6.5 * cm, 7.7 * cm],
        )
    )
    story.append(Paragraph("How Each Lesson Is Organized", styles["h2"]))
    story.extend(
        bullets(
            styles,
            [
                "Objectives — what you can do after the lesson",
                "Explanation — senior-level narrative of concepts and trade-offs",
                "Key points — compressed checklist for revision",
                "Worked examples — commands, Python, XML, SQL, or configs",
                "Common mistakes — failure modes seen in real projects",
                "Lab — hands-on practice that produces an artifact",
            ],
        )
    )
    story.append(Spacer(1, 6))
    story.append(
        callout(
            styles,
            "Do not skip Foundations (Linux/Python/PostgreSQL). Most Odoo production incidents "
            "are diagnosed with OS, language, and database skills—not only ORM knowledge.",
            title="Delivery principle",
        )
    )
    story.append(Paragraph("Recommended Study Path", styles["h2"]))
    story.append(
        Paragraph(
            "Week-by-week professional track (12–16 weeks): Weeks 1–4 foundations; weeks 5–7 Odoo "
            "install/modules/fields/ORM; weeks 8–9 views and security; weeks 10–11 OWL/POS/APIs/"
            "QWeb; week 12 infrastructure and capstone defense. Intensive bootcamps compress each "
            "week into 2–3 full days while keeping the same sequence.",
            styles["body"],
        )
    )
    story.append(Paragraph("Assessment Model", styles["h2"]))
    story.append(
        simple_table(
            styles,
            ["Component", "Weight", "Evidence"],
            [
                ["Lesson labs", "40%", "Working commands/code + notes"],
                ["Knowledge checks", "15%", "Short quizzes per part"],
                ["Mini-projects", "20%", "Integrated feature slices"],
                ["Capstone", "25%", "Secured, documented, demoable module"],
            ],
            [4.5 * cm, 2.5 * cm, 9.4 * cm],
        )
    )
    story.append(PageBreak())

    # Program plan pages
    story.append(banner(styles, "A2", "Capability Map & Capstone Overview"))
    story.append(Spacer(1, 8))
    story.append(Paragraph("North-Star Graduate Capabilities", styles["h2"]))
    story.extend(
        bullets(
            styles,
            [
                "Provision and harden an Ubuntu host suitable for Odoo workloads",
                "Write idiomatic Python suitable for models, wizards, and connectors",
                "Administer PostgreSQL for development and production backup/restore",
                "Install Odoo, author odoo.conf, and operate CLI install/upgrade/shell safely",
                "Design models/fields and override ORM methods without breaking invariants",
                "Build list/form/search/kanban UX and migrate attrs-style view logic",
                "Implement groups, ACLs, and record rules with least privilege",
                "Extend OWL components and POS screens; integrate via XML-RPC",
                "Deploy with Docker or systemd+Nginx+SSL and size workers sensibly",
            ],
        )
    )
    story.append(Paragraph("Capstone Options", styles["h2"]))
    story.append(
        Paragraph(
            "<b>A — Academic Institute Manager:</b> students, courses, enrollments, fees, role-based "
            "security, QWeb confirmation PDF, email on confirmation.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "<b>B — Retail POS Helper:</b> OWL POS button + popup + RPC-persisted cashier note, "
            "manager ACL menu, optional XML-RPC export.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "<b>C — Ops Excellence Pack:</b> production layout, systemd, Nginx/longpolling/Certbot, "
            "backup/restore rehearsal, worker sizing worksheet.",
            styles["body"],
        )
    )
    story.append(Spacer(1, 6))
    story.append(
        callout(
            styles,
            "Capstones are graded on architecture, correctness, security, UX, operability, and "
            "documentation—not on visual decoration.",
            title="Rubric focus",
        )
    )
    story.append(PageBreak())


def render_lesson(story, styles, lesson, part_code):
    lid = lesson["id"]
    title = lesson["title"]
    story.append(banner(styles, lid, title))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Learning Objectives", styles["h3"]))
    story.extend(bullets(styles, lesson.get("objectives", [])))

    story.append(Paragraph("Explanation", styles["h3"]))
    for para in lesson.get("explanation", []):
        story.append(Paragraph(para, styles["body"]))

    kps = lesson.get("key_points") or []
    if kps:
        story.append(Paragraph("Key Points", styles["h3"]))
        story.extend(bullets(styles, kps))

    for ex in lesson.get("examples") or []:
        story.append(Paragraph(ex.get("title", "Example"), styles["h3"]))
        if ex.get("explain"):
            story.append(Paragraph(ex["explain"], styles["body"]))
        if ex.get("code"):
            story.append(code_block(styles, ex["code"]))

    mistakes = lesson.get("common_mistakes") or []
    if mistakes:
        story.append(Paragraph("Common Mistakes", styles["h3"]))
        story.extend(bullets(styles, mistakes))

    if lesson.get("lab"):
        story.append(Spacer(1, 3))
        story.append(callout(styles, lesson["lab"], title="Lab / Practice"))

    story.append(Spacer(1, 8))
    story.append(hr())


def build():
    styles = doc_styles()
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

    doc = BaseDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=1.7 * cm,
        bottomMargin=1.6 * cm,
        title="Odoo Full-Stack Training Documentation",
        author="Weblearns Academy",
    )
    frame = Frame(MARGIN, 1.45 * cm, PAGE_W - 2 * MARGIN, PAGE_H - 3.0 * cm, id="normal")
    cover_frame = Frame(0, 0, PAGE_W, PAGE_H, id="cover")
    doc.addPageTemplates(
        [
            PageTemplate(id="Cover", frames=cover_frame, onPage=cover_page),
            PageTemplate(id="Body", frames=frame, onPage=header_footer),
        ]
    )

    story = []
    story.append(NextPageTemplate("Body"))
    story.append(PageBreak())

    # TOC
    story.append(Paragraph("Table of Contents", styles["h1"]))
    story.append(hr())
    for part_code, part_title, lessons, _sec in PARTS:
        story.append(Paragraph(f"{part_code} — {part_title}", styles["toc_part"]))
        if lessons:
            for lesson in lessons:
                story.append(
                    Paragraph(f"{lesson['id']}  {lesson['title']}", styles["toc_item"])
                )
        else:
            story.append(Paragraph("Program framework, path, assessment, capstones", styles["toc_item"]))
    story.append(PageBreak())

    add_overview(story, styles)

    for part_code, part_title, lessons, _sec in PARTS:
        if not lessons:
            continue
        story.append(banner(styles, part_code, part_title))
        story.append(Spacer(1, 8))
        story.append(
            Paragraph(
                f"This part contains {len(lessons)} detailed lessons. Work in order. Complete each "
                f"lab before moving forward when the lab unlocks the next dependency.",
                styles["body"],
            )
        )
        story.append(
            callout(
                styles,
                f"Companion deck: see training_materials/presentations/ for the {part_title} slides.",
                title="Presentation",
            )
        )
        story.append(PageBreak())
        for idx, lesson in enumerate(lessons):
            render_lesson(story, styles, lesson, part_code)
            if idx < len(lessons) - 1:
                story.append(Spacer(1, 8))
                story.append(hr())
                story.append(Spacer(1, 6))
        story.append(PageBreak())

    # Closing
    story.append(banner(styles, "Z", "Curriculum Closure"))
    story.append(Spacer(1, 8))
    story.append(
        Paragraph(
            "You now have the full written body of the Odoo Full-Stack Developer Program. Continue "
            "with the section presentation decks for lecture pacing, then execute a capstone under "
            "the rubric in Part A. Keep a personal lab journal: commands run, errors seen, and "
            "fixes applied—this journal becomes your operational runbook.",
            styles["body"],
        )
    )
    story.append(Paragraph("Document Control", styles["h2"]))
    story.append(
        simple_table(
            styles,
            ["Field", "Value"],
            [
                ["Title", "Odoo Full-Stack Developer Training Documentation"],
                ["Edition", datetime.now().strftime("%Y.%m")],
                ["Lesson count", str(sum(len(p[2] or []) for p in PARTS))],
                ["Classification", "Complete teaching documentation"],
            ],
            [4.5 * cm, 11.9 * cm],
        )
    )

    doc.build(story)
    return OUTPUT


if __name__ == "__main__":
    path = build()
    print(f"Wrote {path}")

#!/usr/bin/env python3
"""Generate a professional Odoo Full-Stack Developer Training Plan PDF (30+ pages)."""

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    ListFlowable,
    ListItem,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import os

OUTPUT = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "training_materials",
    "Odoo_FullStack_Developer_Training_Plan.pdf",
)

# Brand palette — professional teal/navy (not purple/cream AI defaults)
NAVY = colors.HexColor("#0B2B3C")
TEAL = colors.HexColor("#0E6B6B")
TEAL_LIGHT = colors.HexColor("#E6F3F3")
ACCENT = colors.HexColor("#C45C26")
SLATE = colors.HexColor("#334155")
MUTED = colors.HexColor("#64748B")
LINE = colors.HexColor("#CBD5E1")
WHITE = colors.white
SOFT_BG = colors.HexColor("#F8FAFC")
CODE_BG = colors.HexColor("#F1F5F9")

PAGE_W, PAGE_H = A4
MARGIN = 1.8 * cm


def make_styles():
    base = getSampleStyleSheet()
    styles = {
        "cover_brand": ParagraphStyle(
            "cover_brand",
            fontName="Helvetica-Bold",
            fontSize=14,
            textColor=TEAL,
            alignment=TA_CENTER,
            spaceAfter=8,
            tracking=1,
        ),
        "cover_title": ParagraphStyle(
            "cover_title",
            fontName="Helvetica-Bold",
            fontSize=28,
            textColor=NAVY,
            alignment=TA_CENTER,
            leading=34,
            spaceAfter=12,
        ),
        "cover_sub": ParagraphStyle(
            "cover_sub",
            fontName="Helvetica",
            fontSize=12,
            textColor=SLATE,
            alignment=TA_CENTER,
            leading=18,
            spaceAfter=6,
        ),
        "h1": ParagraphStyle(
            "h1",
            fontName="Helvetica-Bold",
            fontSize=18,
            textColor=NAVY,
            spaceBefore=6,
            spaceAfter=10,
            leading=22,
        ),
        "h2": ParagraphStyle(
            "h2",
            fontName="Helvetica-Bold",
            fontSize=13,
            textColor=TEAL,
            spaceBefore=12,
            spaceAfter=6,
            leading=17,
        ),
        "h3": ParagraphStyle(
            "h3",
            fontName="Helvetica-Bold",
            fontSize=11,
            textColor=NAVY,
            spaceBefore=8,
            spaceAfter=4,
            leading=14,
        ),
        "body": ParagraphStyle(
            "body",
            fontName="Helvetica",
            fontSize=9.5,
            textColor=SLATE,
            alignment=TA_JUSTIFY,
            leading=13.5,
            spaceAfter=6,
        ),
        "body_left": ParagraphStyle(
            "body_left",
            fontName="Helvetica",
            fontSize=9.5,
            textColor=SLATE,
            alignment=TA_LEFT,
            leading=13.5,
            spaceAfter=4,
        ),
        "bullet": ParagraphStyle(
            "bullet",
            fontName="Helvetica",
            fontSize=9,
            textColor=SLATE,
            leading=12.5,
            leftIndent=4,
        ),
        "toc_item": ParagraphStyle(
            "toc_item",
            fontName="Helvetica",
            fontSize=10,
            textColor=SLATE,
            leading=16,
        ),
        "toc_part": ParagraphStyle(
            "toc_part",
            fontName="Helvetica-Bold",
            fontSize=11,
            textColor=NAVY,
            spaceBefore=8,
            spaceAfter=2,
            leading=14,
        ),
        "meta": ParagraphStyle(
            "meta",
            fontName="Helvetica",
            fontSize=8.5,
            textColor=MUTED,
            leading=11,
        ),
        "caption": ParagraphStyle(
            "caption",
            fontName="Helvetica-Oblique",
            fontSize=8,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceBefore=2,
            spaceAfter=8,
        ),
        "callout": ParagraphStyle(
            "callout",
            fontName="Helvetica",
            fontSize=9,
            textColor=NAVY,
            leading=12.5,
            alignment=TA_LEFT,
        ),
        "table_header": ParagraphStyle(
            "table_header",
            fontName="Helvetica-Bold",
            fontSize=8.5,
            textColor=WHITE,
            leading=11,
        ),
        "table_cell": ParagraphStyle(
            "table_cell",
            fontName="Helvetica",
            fontSize=8,
            textColor=SLATE,
            leading=11,
        ),
        "footer": ParagraphStyle(
            "footer",
            fontName="Helvetica",
            fontSize=8,
            textColor=MUTED,
        ),
        "code": ParagraphStyle(
            "code",
            fontName="Courier",
            fontSize=8,
            textColor=NAVY,
            leading=11,
            backColor=CODE_BG,
        ),
        "module_title": ParagraphStyle(
            "module_title",
            fontName="Helvetica-Bold",
            fontSize=12,
            textColor=WHITE,
            leading=15,
        ),
        "session_label": ParagraphStyle(
            "session_label",
            fontName="Helvetica-Bold",
            fontSize=9,
            textColor=ACCENT,
            spaceBefore=4,
            spaceAfter=2,
        ),
    }
    return styles


def header_footer(canvas_obj, doc):
    canvas_obj.saveState()
    # Top accent line
    canvas_obj.setStrokeColor(TEAL)
    canvas_obj.setLineWidth(2)
    canvas_obj.line(MARGIN, PAGE_H - 1.1 * cm, PAGE_W - MARGIN, PAGE_H - 1.1 * cm)
    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.setFillColor(MUTED)
    canvas_obj.drawString(MARGIN, PAGE_H - 0.9 * cm, "Odoo Full-Stack Developer Training Plan")
    canvas_obj.drawRightString(PAGE_W - MARGIN, PAGE_H - 0.9 * cm, "Confidential Training Material")

    # Bottom
    canvas_obj.setStrokeColor(LINE)
    canvas_obj.setLineWidth(0.6)
    canvas_obj.line(MARGIN, 1.2 * cm, PAGE_W - MARGIN, 1.2 * cm)
    canvas_obj.setFillColor(MUTED)
    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.drawString(MARGIN, 0.75 * cm, "Weblearns Academy  |  Odoo 17 / 18 / 19 Track")
    canvas_obj.drawRightString(PAGE_W - MARGIN, 0.75 * cm, f"Page {doc.page}")
    canvas_obj.restoreState()


def cover_page(canvas_obj, doc):
    canvas_obj.saveState()
    # Full left brand panel
    canvas_obj.setFillColor(NAVY)
    canvas_obj.rect(0, 0, 3.2 * cm, PAGE_H, fill=1, stroke=0)
    canvas_obj.setFillColor(TEAL)
    canvas_obj.rect(3.2 * cm, 0, 0.35 * cm, PAGE_H, fill=1, stroke=0)

    # Top band
    canvas_obj.setFillColor(TEAL_LIGHT)
    canvas_obj.rect(3.55 * cm, PAGE_H - 4.5 * cm, PAGE_W - 3.55 * cm, 4.5 * cm, fill=1, stroke=0)

    canvas_obj.setFillColor(TEAL)
    canvas_obj.setFont("Helvetica-Bold", 11)
    canvas_obj.drawString(4.5 * cm, PAGE_H - 2.2 * cm, "PROFESSIONAL TRAINING CURRICULUM")

    canvas_obj.setFillColor(NAVY)
    canvas_obj.setFont("Helvetica-Bold", 26)
    y = PAGE_H - 7.2 * cm
    for line in ["Odoo Full-Stack", "Developer Program", "Training Plan"]:
        canvas_obj.drawString(4.5 * cm, y, line)
        y -= 1.0 * cm

    canvas_obj.setFillColor(SLATE)
    canvas_obj.setFont("Helvetica", 11)
    canvas_obj.drawString(4.5 * cm, y - 0.4 * cm, "From Linux & Python Foundations to Production Odoo Deployment")

    # Info box
    box_y = 6.5 * cm
    canvas_obj.setFillColor(SOFT_BG)
    canvas_obj.roundRect(4.5 * cm, box_y, 13 * cm, 5.2 * cm, 6, fill=1, stroke=0)
    canvas_obj.setStrokeColor(TEAL)
    canvas_obj.setLineWidth(1.5)
    canvas_obj.line(4.5 * cm, box_y + 5.2 * cm, 17.5 * cm, box_y + 5.2 * cm)

    info = [
        ("Version Focus", "Odoo 17 · Odoo 18 · Odoo 19"),
        ("Audience", "Aspiring & Intermediate Odoo Developers"),
        ("Format", "Instructor-led + Labs + Capstone Projects"),
        ("Document Type", "Master Training Plan & Syllabus"),
        ("Edition", datetime.now().strftime("%B %Y")),
        ("Minimum Duration", "120+ guided learning hours"),
    ]
    iy = box_y + 4.5 * cm
    for label, value in info:
        canvas_obj.setFont("Helvetica-Bold", 9)
        canvas_obj.setFillColor(TEAL)
        canvas_obj.drawString(5.0 * cm, iy, label)
        canvas_obj.setFont("Helvetica", 9)
        canvas_obj.setFillColor(SLATE)
        canvas_obj.drawString(9.2 * cm, iy, value)
        iy -= 0.7 * cm

    canvas_obj.setFillColor(MUTED)
    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.drawString(4.5 * cm, 2.2 * cm, "Includes: Backend ORM · Views · Security · OWL · POS · APIs · DevOps · VPS")
    canvas_obj.drawString(4.5 * cm, 1.6 * cm, "Companion document: Odoo Full-Stack Training Presentation.pdf")
    canvas_obj.restoreState()


def section_banner(styles, code, title):
    data = [[Paragraph(f"<b>{code}</b>  &nbsp;&nbsp;{title}", styles["module_title"])]]
    t = Table(data, colWidths=[PAGE_W - 2 * MARGIN])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), TEAL),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    return t


def callout_box(styles, text, title="Learning Outcome"):
    content = Paragraph(f"<b>{title}:</b> {text}", styles["callout"])
    t = Table([[content]], colWidths=[PAGE_W - 2 * MARGIN])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), TEAL_LIGHT),
                ("BOX", (0, 0), (-1, -1), 0.8, TEAL),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return t


def simple_table(styles, headers, rows, col_widths=None):
    header_row = [Paragraph(h, styles["table_header"]) for h in headers]
    data = [header_row]
    for row in rows:
        data.append([Paragraph(str(c), styles["table_cell"]) for c in row])
    if not col_widths:
        w = (PAGE_W - 2 * MARGIN) / len(headers)
        col_widths = [w] * len(headers)
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("BACKGROUND", (0, 1), (-1, -1), WHITE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, SOFT_BG]),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    t.setStyle(TableStyle(style_cmds))
    return t


def bullets(styles, items):
    flow = []
    for item in items:
        flow.append(Paragraph(f"•  {item}", styles["bullet"]))
    return flow


def topic_block(styles, title, topics, outcomes=None, lab=None):
    elems = [Paragraph(title, styles["h3"])]
    elems.extend(bullets(styles, topics))
    if outcomes:
        elems.append(Spacer(1, 4))
        elems.append(callout_box(styles, outcomes))
    if lab:
        elems.append(Paragraph(f"<b>Lab:</b> {lab}", styles["meta"]))
    elems.append(Spacer(1, 6))
    return KeepTogether(elems)


def build():
    styles = make_styles()
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

    doc = BaseDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm,
        title="Odoo Full-Stack Developer Training Plan",
        author="Weblearns Academy",
        subject="Professional Odoo 17/18/19 Training Curriculum",
    )

    frame = Frame(MARGIN, 1.6 * cm, PAGE_W - 2 * MARGIN, PAGE_H - 3.2 * cm, id="normal")
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

    # ========== TOC ==========
    story.append(Paragraph("Table of Contents", styles["h1"]))
    story.append(
        HRFlowable(width="100%", thickness=1, color=TEAL, spaceAfter=10)
    )
    toc = [
        ("Part A — Program Overview", [
            "1. Executive Summary & Program Vision",
            "2. Who This Program Is For",
            "3. Learning Journey Map",
            "4. Program Structure & Duration Model",
            "5. Assessment, Labs & Capstone Projects",
        ]),
        ("Part B — Foundation Tracks", [
            "6. Module F1 — Linux OS & CLI Mastery",
            "7. Module F2 — Python Programming for Odoo",
            "8. Module F3 — PostgreSQL Administration",
        ]),
        ("Part C — Odoo Core Development", [
            "9. Module O1 — Installation, CLI & Configuration",
            "10. Module O2 — Custom Modules & Manifest",
            "11. Module O3 — Fields & Model Design",
            "12. Module O4 — ORM Methods Deep Dive",
            "13. Module O5 — Views (List, Form, Search, Kanban…)",
            "14. Module O6 — Security Architecture",
            "15. Module O7 — Data Loading (XML / CSV)",
            "16. Module O8 — View Inheritance & Migration Tips",
        ]),
        ("Part D — Advanced Odoo", [
            "17. Module A1 — QWeb Reports & Documents",
            "18. Module A2 — OWL Frontend Framework",
            "19. Module A3 — POS Customization (OWL)",
            "20. Module A4 — External APIs (XML-RPC)",
            "21. Module A5 — Email Templates & Automation",
            "22. Module A6 — Server Actions & Workflows",
        ]),
        ("Part E — DevOps & Production", [
            "23. Module D1 — Docker & Containerization",
            "24. Module D2 — VPS, Nginx & SSL Deployment",
            "25. Module D3 — Performance & Worker Tuning",
            "26. Module D4 — CI/CD & Monitoring Basics",
        ]),
        ("Part F — Delivery Framework", [
            "27. Recommended Weekly Schedule",
            "28. Capstone Project Briefs",
            "29. Instructor Delivery Checklist",
            "30. Appendices — Cheat Sheets & Glossary",
        ]),
    ]
    for part, items in toc:
        story.append(Paragraph(part, styles["toc_part"]))
        for item in items:
            story.append(Paragraph(item, styles["toc_item"]))
    story.append(PageBreak())

    # ========== 1 Executive Summary ==========
    story.append(section_banner(styles, "01", "Executive Summary & Program Vision"))
    story.append(Spacer(1, 10))
    story.append(
        Paragraph(
            "This Training Plan defines a complete, production-oriented pathway for becoming a "
            "confident Odoo Full-Stack Developer. It unifies operating-system fluency, Python mastery, "
            "PostgreSQL administration, Odoo backend/ORM development, modern OWL frontend work, "
            "Point of Sale customization, integration APIs, and real-world DevOps deployment.",
            styles["body"],
        )
    )
    story.append(
        Paragraph(
            "The curriculum is intentionally sequenced: learners first earn the platform skills that "
            "Odoo depends on (Linux, Python, PostgreSQL), then progress through Odoo 17 development "
            "fundamentals, continue into Odoo 18/19 security and privilege model changes, and finish "
            "with containerization, reverse-proxy hardening, and performance architecture.",
            styles["body"],
        )
    )
    story.append(Paragraph("Program Pillars", styles["h2"]))
    story.append(
        simple_table(
            styles,
            ["Pillar", "Focus", "Outcome"],
            [
                ["Foundations", "Linux · Python · PostgreSQL", "Reliable server & coding baseline"],
                ["Odoo Backend", "Models · Fields · ORM · Views · Security", "Ship maintainable business modules"],
                ["Odoo Frontend", "OWL · Widgets · POS · RPC", "Extend the web client professionally"],
                ["Integration", "XML-RPC · Email · Server Actions", "Connect Odoo to external systems"],
                ["Operations", "Docker · Nginx · SSL · Workers", "Deploy and tune production instances"],
            ],
            [3.2 * cm, 7.2 * cm, 6.0 * cm],
        )
    )
    story.append(Spacer(1, 10))
    story.append(
        callout_box(
            styles,
            "Graduates can install Odoo, develop custom modules end-to-end, secure data with groups "
            "and record rules, customize OWL/POS, expose integrations, and operate a hardened VPS deployment.",
            "North-Star Outcome",
        )
    )
    story.append(PageBreak())

    # ========== 2 Audience ==========
    story.append(section_banner(styles, "02", "Who This Program Is For"))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Primary Audiences", styles["h2"]))
    story.extend(
        bullets(
            styles,
            [
                "Junior developers transitioning into Odoo customization and module development",
                "ERP consultants who need stronger technical implementation skills",
                "Python developers entering the Odoo ecosystem (17 → 19)",
                "System administrators expanding into application-layer Odoo work",
                "Technical leads designing internal Odoo enablement academies",
            ],
        )
    )
    story.append(Paragraph("Prerequisites", styles["h2"]))
    story.append(
        simple_table(
            styles,
            ["Level", "Requirement", "Notes"],
            [
                ["Required", "Basic computer literacy", "Comfort with files, browsers, accounts"],
                ["Recommended", "Any prior programming exposure", "Python preferred but not mandatory"],
                ["Recommended", "Familiarity with Ubuntu desktop/server", "Covered in Module F1 if missing"],
                ["Helpful", "Business process awareness", "Sales, inventory, HR, accounting concepts"],
            ],
            [3.2 * cm, 6.5 * cm, 6.7 * cm],
        )
    )
    story.append(Paragraph("Competency Targets (Bloom Levels)", styles["h2"]))
    story.extend(
        bullets(
            styles,
            [
                "Remember & Understand — CLI, ORM vocabulary, security components, view types",
                "Apply — Scaffold modules, define fields, build views, write record rules",
                "Analyze — Diagnose worker limits, slow SQL, inheritance conflicts, ACL gaps",
                "Create — Deliver a multi-module business app with reports, security, and deployment",
            ],
        )
    )
    story.append(PageBreak())

    # ========== 3 Journey Map ==========
    story.append(section_banner(styles, "03", "Learning Journey Map"))
    story.append(Spacer(1, 10))
    story.append(
        Paragraph(
            "The journey is organized as six progressive phases. Each phase unlocks the next; "
            "skipping foundations is discouraged because Odoo debugging frequently requires Linux, "
            "Python, and PostgreSQL literacy.",
            styles["body"],
        )
    )
    story.append(
        simple_table(
            styles,
            ["Phase", "Modules", "Theme", "Exit Gate"],
            [
                ["1 Foundations", "F1–F3", "OS, language, database", "CLI + Python + SQL labs passed"],
                ["2 Odoo Core", "O1–O4", "Install, modules, fields, ORM", "Custom module with CRUD logic"],
                ["3 UX & Security", "O5–O8", "Views, ACLs, data files", "Secured app with list/form/search"],
                ["4 Advanced", "A1–A6", "QWeb, OWL, POS, APIs", "Report + OWL/POS + XML-RPC demo"],
                ["5 Ops", "D1–D4", "Docker, VPS, performance", "HTTPS stack with workers tuned"],
                ["6 Capstone", "Projects", "End-to-end delivery", "Reviewed production-ready module"],
            ],
            [2.8 * cm, 2.4 * cm, 5.2 * cm, 6.0 * cm],
        )
    )
    story.append(Spacer(1, 12))
    story.append(Paragraph("Version Coverage Strategy", styles["h2"]))
    story.append(
        Paragraph(
            "Core development patterns are taught primarily on <b>Odoo 17</b> for stability and breadth of "
            "community tutorials, then explicitly mapped to <b>Odoo 18</b> and <b>Odoo 19</b> differences—"
            "especially the privilege model, attrs migration (invisible/readonly/required), and updated "
            "security practices. Installation labs include Ubuntu 22.04 (Odoo 17) and Ubuntu 24.04 (Odoo 19).",
            styles["body"],
        )
    )
    story.append(PageBreak())

    # ========== 4 Structure ==========
    story.append(section_banner(styles, "04", "Program Structure & Duration Model"))
    story.append(Spacer(1, 10))
    story.append(
        Paragraph(
            "Two delivery models are supported. Instructors may compress or expand based on cohort seniority.",
            styles["body"],
        )
    )
    story.append(
        simple_table(
            styles,
            ["Model", "Cadence", "Total Hours", "Best For"],
            [
                ["Intensive Bootcamp", "Full-time, 6–8 weeks", "140–160 hrs", "Career switchers / dedicated cohorts"],
                ["Professional Track", "Part-time, 12–16 weeks", "120–140 hrs", "Working professionals"],
            ],
            [4.0 * cm, 4.5 * cm, 3.2 * cm, 4.7 * cm],
        )
    )
    story.append(Paragraph("Hour Allocation by Domain", styles["h2"]))
    story.append(
        simple_table(
            styles,
            ["Domain", "Guided Hours", "Lab Hours", "Share"],
            [
                ["Linux & CLI", "8", "6", "≈10%"],
                ["Python", "16", "12", "≈20%"],
                ["PostgreSQL", "8", "6", "≈10%"],
                ["Odoo Backend & Views", "28", "22", "≈35%"],
                ["OWL / POS / APIs / QWeb", "14", "12", "≈18%"],
                ["DevOps / Deploy / Perf", "10", "8", "≈12%"],
                ["Capstone & Review", "6", "10", "≈10%"],
            ],
            [5.5 * cm, 3.5 * cm, 3.5 * cm, 3.9 * cm],
        )
    )
    story.append(Spacer(1, 8))
    story.append(
        Paragraph(
            "Note: Shares are approximate and intentionally overlap during integrated labs "
            "(for example, a security lab also reinforces views and ORM).",
            styles["meta"],
        )
    )
    story.append(PageBreak())

    # ========== 5 Assessment ==========
    story.append(section_banner(styles, "05", "Assessment, Labs & Capstone Projects"))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Assessment Mix", styles["h2"]))
    story.append(
        simple_table(
            styles,
            ["Component", "Weight", "Evidence"],
            [
                ["Module Labs", "40%", "Working code pushed to learner repo + screenshots"],
                ["Knowledge Checks", "15%", "Short quizzes on ORM, security, CLI, SQL"],
                ["Integrated Mini-Projects", "20%", "Student Manager, Inventory tweak, POS button"],
                ["Final Capstone", "25%", "Deployed module with docs, ACLs, report, README"],
            ],
            [5.0 * cm, 2.5 * cm, 8.9 * cm],
        )
    )
    story.append(Paragraph("Quality Rubric (Capstone)", styles["h2"]))
    story.extend(
        bullets(
            styles,
            [
                "Architecture — clear models, sensible relations, no unnecessary complexity",
                "Correctness — CRUD, computed fields, constraints, and views behave as specified",
                "Security — groups, access rights, and record rules intentionally designed",
                "UX — list/form/search/kanban usable; decorations and statusbar where relevant",
                "Ops — installable via addons path; optional Docker Compose or systemd notes",
                "Documentation — manifest, README, and short demo script for reviewers",
            ],
        )
    )
    story.append(PageBreak())

    # ========== F1 Linux ==========
    story.append(section_banner(styles, "F1", "Linux Operating System & CLI Mastery"))
    story.append(Spacer(1, 8))
    story.append(
        callout_box(
            styles,
            "Operate an Ubuntu server confidently: navigate the filesystem, manage users/services, "
            "inspect logs, secure SSH, and automate routine tasks with cron and apt.",
        )
    )
    story.append(Paragraph("Session Plan", styles["h2"]))
    story.append(
        topic_block(
            styles,
            "Session 1 — OS Fundamentals & Navigation",
            [
                "LINUX — OS Fundamentals & CLI Setup",
                "System Architecture & Kernel Basics",
                "Essential Terminal Navigation (pwd, cd, ls, tree)",
                "File Manipulation (cp, mv, rm, mkdir, touch)",
            ],
            lab="Create a project tree under /opt/training and practice safe recursive operations.",
        )
    )
    story.append(
        topic_block(
            styles,
            "Session 2 — Permissions, Users & Processes",
            [
                "Linux File Permissions (chmod, chown, chgrp)",
                "Managing Users, Groups, and Sudo Privileges",
                "Process Management (top, htop, ps, kill, pkill)",
                "System V & Systemd Services (systemctl start/stop/status/enable)",
            ],
            lab="Create an odoo system user concept dry-run; manage a sample systemd unit.",
        )
    )
    story.append(
        topic_block(
            styles,
            "Session 3 — Logs, Networking, SSH & Automation",
            [
                "Monitoring System Logs (journalctl, tail)",
                "Text Editors in CLI (Nano vs Vim)",
                "Networking Fundamentals (ip, ping, ss)",
                "SSH Key Generation, Configuration, and Hardening",
                "Environment Variables and .bashrc Configuration",
                "CRON Jobs and Task Automation",
                "Package Management with APT",
                "Disk Usage Monitoring (df, du, free)",
                "Linux Firewall Setup using UFW",
            ],
            outcomes="Learner can harden SSH basics, enable UFW thoughtfully, and schedule a log-rotation-style cron.",
        )
    )
    story.append(PageBreak())

    # ========== F2 Python ==========
    story.append(section_banner(styles, "F2", "Python Programming for Odoo Developers"))
    story.append(Spacer(1, 8))
    story.append(
        callout_box(
            styles,
            "Write clean, idiomatic Python sufficient for Odoo models, ORM overrides, wizards, "
            "and small utilities—including OOP, errors, modules, and virtual environments.",
        )
    )
    story.append(Paragraph("Track Overview", styles["h2"]))
    story.append(
        Paragraph(
            "This module follows a practical Python syllabus mapped to Odoo needs. Learners who are "
            "already strong in Python may place out via a diagnostic exam and join Odoo modules earlier.",
            styles["body"],
        )
    )
    story.append(
        simple_table(
            styles,
            ["Block", "Topics", "Odoo Relevance"],
            [
                [
                    "Core Syntax",
                    "Interpreter, data types, numbers, strings, booleans, operators",
                    "Reading Odoo source & writing field logic",
                ],
                [
                    "Collections",
                    "Lists, dicts, tuples, sets, unpacking, comprehensions",
                    "Recordsets, mapped/filtered patterns",
                ],
                [
                    "Control Flow",
                    "Conditionals, loops, ternary, short-circuiting",
                    "Constraints, onchange-style logic, wizards",
                ],
                [
                    "Functions",
                    "Args/kwargs, scope, decorators, walrus, clean code",
                    "Model methods, api decorators mindset",
                ],
                [
                    "OOP",
                    "Classes, inheritance, MRO, dunders, polymorphism",
                    "Model inheritance & method overrides",
                ],
                [
                    "FP Toolkit",
                    "map/filter/zip/reduce, lambdas, generators",
                    "Data transforms in reports & connectors",
                ],
                [
                    "Tooling",
                    "venv, pip, PEP8, VS Code/PyCharm, debugging",
                    "Daily Odoo development workflow",
                ],
            ],
            [2.8 * cm, 7.5 * cm, 6.1 * cm],
        )
    )
    story.append(Spacer(1, 8))
    story.append(Paragraph("Selected Lesson Sequence (Condensed)", styles["h2"]))
    story.extend(
        bullets(
            styles,
            [
                "What is a programming language? · Python Interpreter · First program · Python 2 vs 3",
                "Variables, expressions, augmented assignment, strings, formatting, immutability",
                "Lists/matrices/methods · Dictionaries · Tuples · Sets · None",
                "Conditionals, truthy/falsey, logical operators, is vs ==",
                "for/while, range, enumerate, break/continue/pass · GUI mini-exercise",
                "Functions deep dive · Scope · global/nonlocal · Exam checkpoint",
                "OOP series through multiple inheritance & MRO",
                "Functional programming, decorators, errors, generators, modules/packages",
                "PyPI, pip, virtualenv · Useful stdlib · Debugging fundamentals",
            ],
        )
    )
    story.append(
        Paragraph(
            "<b>Lab Cap:</b> Build a CLI contact manager using classes, file persistence, and exception handling.",
            styles["meta"],
        )
    )
    story.append(PageBreak())

    # ========== F3 PostgreSQL ==========
    story.append(section_banner(styles, "F3", "PostgreSQL Database Administration & Querying"))
    story.append(Spacer(1, 8))
    story.append(
        callout_box(
            styles,
            "Install and operate PostgreSQL for Odoo: users/roles, SQL fluency, indexes, "
            "EXPLAIN, backups, and configuration files used in real deployments.",
        )
    )
    story.append(
        topic_block(
            styles,
            "Sessions & Topics",
            [
                "Installing PostgreSQL on Ubuntu LTS · psql CLI · Users & roles · Grants",
                "PostgreSQL data types · DDL (CREATE/ALTER/DROP) · PK/FK/constraints",
                "CRUD · WHERE/LIKE/ILIKE/IN/BETWEEN · Joins (INNER/LEFT/RIGHT/FULL)",
                "Aggregations (GROUP BY/HAVING/COUNT/SUM/AVG)",
                "Indexes & optimization (B-Tree, GIN, composite) · EXPLAIN ANALYZE",
                "Backup/export with pg_dump · Restore with pg_restore/psql",
                "postgresql.conf & pg_hba.conf · Locks, connections, terminating stuck queries",
            ],
            lab="Create an odoo DB role, sample schema, indexed queries, and a dump/restore drill.",
            outcomes="Learner can diagnose slow queries and safely back up/restore an Odoo-like database.",
        )
    )
    story.append(Paragraph("Odoo-Specific SQL Habits", styles["h2"]))
    story.extend(
        bullets(
            styles,
            [
                "Always prefer ORM for business logic; use SQL for diagnosis and DBA tasks",
                "Inspect ir_model_data / ir_model_access when debugging security & XML IDs",
                "Use pg_stat_statements later in performance module for production slow-query analysis",
            ],
        )
    )
    story.append(PageBreak())

    # ========== O1 Installation ==========
    story.append(section_banner(styles, "O1", "Odoo Installation, CLI & Configuration"))
    story.append(Spacer(1, 8))
    story.append(
        callout_box(
            styles,
            "Install Odoo 17 on Ubuntu 22.04 (and preview Odoo 19 on Ubuntu 24.04), start odoo-bin, "
            "author a configuration file, and operate core CLI workflows safely.",
        )
    )
    story.append(Paragraph("Tutorial Units Covered", styles["h2"]))
    story.extend(
        bullets(
            styles,
            [
                "Odoo 17 Installation on Ubuntu 22.04 LTS Tutorial",
                "How to start Odoo from terminal | odoo-bin",
                "Introduction to Odoo 17 CLI Commands",
                "How to Create a Configuration File for Odoo 17",
                "Exploring Common URLs in Odoo Database Manager",
                "How to Disable Database Manager / Selector URL (Security)",
                "Mastering Odoo 17 Database CLI Commands",
                "Configuring Odoo 17 in PyCharm Tutorial",
                "Basic CLI Commands · Install/Upgrade Modules via CLI",
                "SHELL CLI · Master password reset · Prevent HTTP call in CLI",
                "Odoo Useful URLs · Log files · Custom logs · Logger CLI (Web/SQL logs)",
                "Upgrade Code CLI Command | Module Migration",
                "Odoo 19 Installation on Ubuntu 24.04 LTS (Latest track)",
            ],
        )
    )
    story.append(Paragraph("Hands-on Checklist", styles["h2"]))
    story.append(
        simple_table(
            styles,
            ["Task", "Acceptance Criteria"],
            [
                ["Install dependencies & Odoo source", "odoo-bin --help works; server starts on 8069"],
                ["Create odoo.conf", "db_host/user/password, addons_path, logfile set"],
                ["Secure DB manager", "list_db=False validated; master password documented"],
                ["IDE run config", "PyCharm/VS Code launches with same conf"],
                ["Logging", "Custom logger writes to file; SQL debug toggled intentionally"],
            ],
            [6.5 * cm, 9.9 * cm],
        )
    )
    story.append(PageBreak())

    # ========== O2 Modules ==========
    story.append(section_banner(styles, "O2", "Custom Modules, Manifest & Addons Paths"))
    story.append(Spacer(1, 8))
    story.append(
        callout_box(
            styles,
            "Scaffold a module, configure manifests and dependencies, manage multi-addons paths "
            "(including App Store layouts), and auto-install modules in controlled environments.",
        )
    )
    story.extend(
        bullets(
            styles,
            [
                "Create module using SCAFFOLD command (Odoo 17)",
                "Adding Custom Paths · Odoo App Store · Multi Addons Path",
                "Understanding the manifest File in Odoo 17",
                "Adding Dependencies in Odoo 17 Manifest File",
                "How to create a custom module in Odoo 17",
                "Automatically Installing Modules in Odoo 17",
                "How _name and _table model attributes work",
                "Auto Create Fields In Model",
                "How to add multiple addons using addons-path",
            ],
        )
    )
    story.append(Paragraph("Manifest Quality Standards", styles["h2"]))
    story.extend(
        bullets(
            styles,
            [
                "name, version, category, summary, description, author, license filled deliberately",
                "depends lists only required modules; avoid hidden transitive assumptions",
                "data/demo XML ordered to respect foreign-key and XML-ID dependencies",
                "installable/application flags match whether the module is an app or technical library",
            ],
        )
    )
    story.append(
        Paragraph(
            "<b>Lab:</b> Scaffold <font face='Courier'>wl_student</font>, wire addons_path, install via UI and CLI.",
            styles["meta"],
        )
    )
    story.append(PageBreak())

    # ========== O3 Fields ==========
    story.append(section_banner(styles, "O3", "Fields & Model Design"))
    story.append(Spacer(1, 8))
    story.append(
        callout_box(
            styles,
            "Select the correct field types for business data—including relational, computed, "
            "monetary, binary/image—and understand when related/reference fields are appropriate.",
        )
    )
    story.append(Paragraph("Field Catalog (Teach + Practice Each)", styles["h2"]))
    story.append(
        simple_table(
            styles,
            ["Category", "Fields"],
            [
                ["Scalar", "Char · Text/Textarea · Html · Boolean · Selection · Integer · Float · Json"],
                ["Temporal", "Date · Datetime"],
                ["Relational", "Many2one · One2many · Many2many · Reference · Related"],
                ["Advanced", "Compute · Monetary · Binary (upload) · Image"],
            ],
            [3.5 * cm, 12.9 * cm],
        )
    )
    story.append(Paragraph("Design Guidelines", styles["h2"]))
    story.extend(
        bullets(
            styles,
            [
                "Prefer Many2one + One2many over duplicated Char references",
                "Use Selection for closed vocabularies; Many2one when users must extend values",
                "Monetary fields require currency_id discipline",
                "Computed fields: define depends carefully; decide store=True only when needed",
                "Binary/Image: consider attachment storage and access rules",
            ],
        )
    )
    story.append(
        Paragraph(
            "<b>Lab:</b> Extend student module with personal data, enrollment lines (O2M), tags (M2M), "
            "photo, computed age, and monetary fee fields.",
            styles["meta"],
        )
    )
    story.append(PageBreak())

    # ========== O4 ORM ==========
    story.append(section_banner(styles, "O4", "ORM Methods Deep Dive"))
    story.append(Spacer(1, 8))
    story.append(
        callout_box(
            styles,
            "Master default ORM methods, overrides (create/write/copy/unlink), search domains, "
            "recordset helpers, and modern fetch APIs used in Odoo 17+.",
        )
    )
    story.append(Paragraph("A. Lifecycle Overrides", styles["h2"]))
    story.extend(
        bullets(
            styles,
            [
                "Understanding Default ORM Methods in Odoo",
                "Override create · write · copy (duplicate) · unlink (remove)",
                "Add a Custom Method · exists() to verify records",
            ],
        )
    )
    story.append(Paragraph("B. Query & Read APIs", styles["h2"]))
    story.extend(
        bullets(
            styles,
            [
                "search() · search domain operators · search_count()",
                "read · read_group · search_read · search_fetch",
                "name_create · default_get · _name_search · get_view() (fields_view_get legacy map)",
                "fields_get · get_metadata",
            ],
        )
    )
    story.append(Paragraph("C. Recordset Helpers", styles["h2"]))
    story.extend(
        bullets(
            styles,
            [
                "ensure_one() · filtered() · mapped() · sorted() · grouped()",
            ],
        )
    )
    story.append(Paragraph("D. Environment & Special Commands", styles["h2"]))
    story.extend(
        bullets(
            styles,
            [
                "Odoo Environment / self.env · Modify environment variables patterns",
                "Special commands overview and practice: "
                "[0,0,vals] create · [1,id,vals] update · [2,id] delete · [3,id] unlink · "
                "[4,id] link · [5] clear · [6,0,ids] set",
                "Active field · Archive/Unarchive · Soft vs Hard Delete",
            ],
        )
    )
    story.append(
        callout_box(
            styles,
            "Never bypass ACLs casually with sudo(); document every elevated operation and prefer "
            "explicit security design.",
            "Safety Rule",
        )
    )
    story.append(PageBreak())

    # ========== O5 Views ==========
    story.append(section_banner(styles, "O5", "Views — List, Form, Search, Kanban & More"))
    story.append(Spacer(1, 8))
    story.append(
        callout_box(
            styles,
            "Build polished business UX with list/form/search/kanban/graph/pivot/cohort/gantt "
            "patterns and modern Odoo 17+ view attributes.",
        )
    )
    story.append(Paragraph("List View Mastery", styles["h2"]))
    story.extend(
        bullets(
            styles,
            [
                "Create list view · Editable list · Mass editing · Decorations",
                "Button to open form · Sort By & Limit · Hide/show fields · Sum/Average",
                "Field width / hide label · Group By · Headers & buttons",
                "Field-level decoration · Disable buttons · Drag-drop handle widget",
            ],
        )
    )
    story.append(Paragraph("Search & Form", styles["h2"]))
    story.extend(
        bullets(
            styles,
            [
                "Create Search View · Search Panel · Dynamic Datetime Filter · Default Filter",
                "Form customization · Sheet/Header/Group/Newline/Separator tags",
                "Notebook pages · Button containers · Statusbar · Dynamic statusbar",
            ],
        )
    )
    story.append(Paragraph("Kanban & Analytical Views", styles["h2"]))
    story.extend(
        bullets(
            styles,
            [
                "Kanban create · Drag & drop · Images on cards · Progressbar widget",
                "Graph (bar/pie/line) · Pivot · Cohort · Gantt",
            ],
        )
    )
    story.append(Paragraph("View Attribute Migration Tips (Odoo 17+)", styles["h2"]))
    story.extend(
        bullets(
            styles,
            [
                "What is attrs in views — migration away from legacy attrs dictionaries",
                "Readonly · Invisible · Required attributes in views (modern expressions)",
            ],
        )
    )
    story.append(PageBreak())

    # ========== O6 Security ==========
    story.append(section_banner(styles, "O6", "Security Architecture (Groups, ACLs, Rules)"))
    story.append(Spacer(1, 8))
    story.append(
        callout_box(
            styles,
            "Design least-privilege security using categories, groups, access rights, record rules, "
            "and Odoo 19 privilege-model awareness.",
        )
    )
    story.append(Paragraph("Six Essential Components (Framework Lecture)", styles["h2"]))
    story.append(
        Paragraph(
            "Deliver the complete security guide covering users, groups, access rights, record rules, "
            "field/view restrictions, and menu/action visibility—then implement each on the student module.",
            styles["body"],
        )
    )
    story.append(
        simple_table(
            styles,
            ["Unit", "Learning Focus"],
            [
                ["Groups & Categories", "Create groups · parent/child · custom category · combobox style"],
                ["Implied Groups", "implied_ids inheritance patterns with real examples"],
                ["Access Rights", "CSV and XML definitions of ir.model.access"],
                ["Record Rules", "Why required · student/teacher/admin scenario · inheritance"],
                ["Application Points", "Views, fields, window actions, menus"],
                ["Odoo 19 Delta", "New privilege model · migration notes · groups on fields/views/actions"],
            ],
            [4.2 * cm, 12.2 * cm],
        )
    )
    story.append(Spacer(1, 8))
    story.append(
        Paragraph(
            "<b>Lab:</b> Implement Admin / Teacher / Student roles with record rules isolating private notes "
            "while allowing shared course visibility.",
            styles["meta"],
        )
    )
    story.append(PageBreak())

    # ========== O7 Data ==========
    story.append(section_banner(styles, "O7", "Data Loading — XML & CSV"))
    story.append(Spacer(1, 8))
    story.append(
        callout_box(
            styles,
            "Load deterministic demo/production data via XML and CSV, including relational fields, "
            "binaries/images, and eval attributes.",
        )
    )
    story.extend(
        bullets(
            styles,
            [
                "Intro: record creates using XML or CSV",
                "Create records with XML · eval attribute · add images",
                "Many2one / Many2many / One2many in XML",
                "Binary fields in XML",
                "CSV records · Many2one in CSV · Many2many in CSV · images/binary in CSV",
                "Difference between XML and CSV data import",
            ],
        )
    )
    story.append(Paragraph("Instructor Emphasis", styles["h2"]))
    story.extend(
        bullets(
            styles,
            [
                "XML IDs are API contracts—name them stably",
                "Use noupdate carefully for editable master data vs locked system data",
                "Prefer XML for security/view/action definitions; CSV shines for bulk ACL rows and simple masters",
            ],
        )
    )
    story.append(PageBreak())

    # ========== O8 Inheritance ==========
    story.append(section_banner(styles, "O8", "View Inheritance & Extension Patterns"))
    story.append(Spacer(1, 8))
    story.append(
        callout_box(
            styles,
            "Extend existing Odoo views safely using inheritance, xpath, and position strategies "
            "without breaking upgrades.",
        )
    )
    story.extend(
        bullets(
            styles,
            [
                "View Inheritance overview — extend views basics",
                "Inheritance using field tag",
                "Inheritance using xpath",
                "Positions: after · before · inside · replace · attributes",
            ],
        )
    )
    story.append(Paragraph("Upgrade-Safe Practices", styles["h2"]))
    story.extend(
        bullets(
            styles,
            [
                "Prefer stable name/attrs anchors over brittle absolute xpaths when possible",
                "Keep inherited diffs small and documented",
                "Test against base module upgrades in a staging database",
            ],
        )
    )
    story.append(
        Paragraph(
            "<b>Also covered in this security/UX cluster:</b> URL actions (internal/external), "
            "ir.sequence auto-numbering patterns.",
            styles["meta"],
        )
    )
    story.append(PageBreak())

    # ========== A1 QWeb ==========
    story.append(section_banner(styles, "A1", "QWeb Reports & Document Layout"))
    story.append(Spacer(1, 8))
    story.append(
        callout_box(
            styles,
            "Design printable PDF reports with QWeb: directives, control flow, inheritance, "
            "paper formats, barcodes/QR, and static/dynamic images.",
        )
    )
    story.extend(
        bullets(
            styles,
            [
                "Introduction to QWeb report · Generate PDF reports",
                "t-field · t-esc · t-out usage",
                "Conditionals (if / elif / else) · Loops · predefined loop variables",
                "Define variables · Call templates · t-att · t-attf",
                "Inherit/extend QWeb templates",
                "Paper format / document layout · Custom report end-to-end",
                "Barcode & QR generation · Static images · Dynamic images",
            ],
        )
    )
    story.append(
        Paragraph(
            "<b>Lab:</b> Student ID card / enrollment confirmation PDF with logo, QR, and conditional watermark.",
            styles["meta"],
        )
    )
    story.append(PageBreak())

    # ========== A2 OWL ==========
    story.append(section_banner(styles, "A2", "Odoo Web Library (OWL) Framework"))
    story.append(Spacer(1, 8))
    story.append(
        callout_box(
            styles,
            "Build and extend reactive OWL components, templates, field widgets, and web client "
            "integrations using rpc services and the patch utility.",
        )
    )
    story.append(Paragraph("1) Architecture & Components", styles["h3"]))
    story.extend(
        bullets(
            styles,
            [
                "Introduction to OWL & reactive architecture",
                "Component structure & lifecycle hooks",
                "State management with useState and useRef",
                "Event handling and props passing",
            ],
        )
    )
    story.append(Paragraph("2) UI Templates & Custom Widgets", styles["h3"]))
    story.extend(
        bullets(
            styles,
            [
                "OWL QWeb XML templates & directives (t-if, t-foreach, t-model)",
                "Custom form field widgets (Odoo 17/18)",
                "Overriding existing JS components & views",
                "Patching standard OWL components with patch()",
            ],
        )
    )
    story.append(Paragraph("3) Service Layer & WebClient", styles["h3"]))
    story.extend(
        bullets(
            styles,
            [
                "Asynchronous RPC via Odoo rpc service",
                "Building custom views (Kanban/Dashboard) with OWL",
            ],
        )
    )
    story.append(PageBreak())

    # ========== A3 POS ==========
    story.append(section_banner(styles, "A3", "OWL POS Customization"))
    story.append(Spacer(1, 8))
    story.append(
        callout_box(
            styles,
            "Customize Point of Sale screens with OWL: buttons, click handlers, popups, "
            "translations, RPC data rendering, and order-line utilities.",
        )
    )
    story.extend(
        bullets(
            styles,
            [
                "Add custom button in POS (Odoo 16+ OWL patterns applicable forward)",
                "Create click events for POS buttons",
                "Hide buttons on POS screen",
                "Create a Popup in Odoo POS",
                "Translate strings in JavaScript files",
                "JavaScript RPC calls in POS · Render dynamic data via RPC",
                "Clear all order lines in POS",
            ],
        )
    )
    story.append(
        Paragraph(
            "<b>Lab:</b> Add a “Manager Note” button opening a popup, storing a note via RPC, "
            "with translated labels.",
            styles["meta"],
        )
    )
    story.append(PageBreak())

    # ========== A4 APIs ==========
    story.append(section_banner(styles, "A4", "External API — XML-RPC Integration"))
    story.append(Spacer(1, 8))
    story.append(
        callout_box(
            styles,
            "Authenticate and perform CRUD against Odoo from external systems using XML-RPC, "
            "including Postman-based verification workflows.",
        )
    )
    story.extend(
        bullets(
            styles,
            [
                "XML-RPC Integration Tutorial — connect external systems",
                "External API Authentication — secure login patterns",
                "Fetching/exporting data via XML-RPC",
                "CRUD operations: add, update, remove records",
                "Authentication in Postman · Add/update/delete via Postman",
            ],
        )
    )
    story.append(Paragraph("Security & Design Notes", styles["h2"]))
    story.extend(
        bullets(
            styles,
            [
                "Use dedicated integration users with minimal ACLs",
                "Prefer HTTPS endpoints; never embed production passwords in notebooks",
                "Idempotent external writes: plan XML IDs or external_id mapping strategies",
            ],
        )
    )
    story.append(PageBreak())

    # ========== A5 Email / A6 Server Actions ==========
    story.append(section_banner(styles, "A5–A6", "Email Templates, Automation & Server Actions"))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Email", styles["h2"]))
    story.extend(
        bullets(
            styles,
            [
                "How to create an Email Template",
                "How to send email from Odoo using an Email Template",
            ],
        )
    )
    story.append(Paragraph("Server Actions", styles["h2"]))
    story.extend(
        bullets(
            styles,
            [
                "What is a Server Action in Odoo? Full explanation with use cases",
                "Connect server actions to UI buttons and automated workflows",
                "Safe coding practices inside server action Python code",
            ],
        )
    )
    story.append(
        callout_box(
            styles,
            "Combine record rules + server actions + email templates to implement an enrollment "
            "approval notification flow without hard-coding UI-only logic.",
            "Integration Lab",
        )
    )
    story.append(PageBreak())

    # ========== D1 Docker ==========
    story.append(section_banner(styles, "D1", "Docker Containerization & Compose"))
    story.append(Spacer(1, 8))
    story.append(
        callout_box(
            styles,
            "Containerize Odoo development and staging stacks with Docker Engine, Compose, "
            "volumes, networking, and safe upgrade practices.",
        )
    )
    story.extend(
        bullets(
            styles,
            [
                "Containerization vs Virtualization",
                "Install Docker Engine & Docker Compose on Ubuntu",
                "Essential CLI: docker run/ps/exec/logs/rm",
                "Images, containers, Docker Hub",
                "Custom Dockerfiles for Odoo development",
                "Volumes for Postgres & addons persistence",
                "Docker networking · Compose YAML structure",
                "Multi-container environment (Odoo + PostgreSQL)",
                ".env files · Updating/upgrading without data loss",
                "Basic CI/CD concepts for Odoo modules (GitHub Actions)",
            ],
        )
    )
    story.append(
        Paragraph(
            "<b>Lab:</b> Compose file with odoo+db, mounted custom addons, named volumes, and documented upgrade steps.",
            styles["meta"],
        )
    )
    story.append(PageBreak())

    # ========== D2 VPS ==========
    story.append(section_banner(styles, "D2", "Production VPS, Nginx & SSL"))
    story.append(Spacer(1, 8))
    story.append(
        callout_box(
            styles,
            "Deploy Odoo on a VPS with hardened SSH, disciplined directory layout, Nginx reverse "
            "proxy, longpolling, Let's Encrypt SSL, systemd, and backup cron jobs.",
        )
    )
    story.append(
        simple_table(
            styles,
            ["Layer", "Topic / Tutorial Unit"],
            [
                ["VPS Provisioning", "Choosing VPS specs (AWS, DigitalOcean, Hetzner) & initial setup"],
                ["Server Security", "Hardening SSH — disable password auth & change default port"],
                ["Directory Layout", "/opt/odoo · /var/log/odoo · custom addons layout"],
                ["Reverse Proxy", "Install/configure Nginx as reverse proxy"],
                ["Port Routing", "Forward 80/443 → Odoo 8069"],
                ["WebSockets", "Nginx for Gevent/Longpolling (8072)"],
                ["SSL Security", "Let's Encrypt + Certbot automation"],
                ["Systemd Service", "odoo.service setup"],
                ["Backups", "DB + filestore backup scripts via cron"],
            ],
            [4.0 * cm, 12.4 * cm],
        )
    )
    story.append(PageBreak())

    # ========== D3 Performance ==========
    story.append(section_banner(styles, "D3", "Performance Tuning & Worker Architecture"))
    story.append(Spacer(1, 8))
    story.append(
        callout_box(
            styles,
            "Size workers correctly, set memory/time limits, tune PostgreSQL connections, "
            "and introduce caching/monitoring patterns for scale.",
        )
    )
    story.extend(
        bullets(
            styles,
            [
                "Odoo multiprocessing & worker architecture",
                "Calculating optimal workers from CPU cores and RAM",
                "limit_memory_hard / limit_memory_soft",
                "limit_time_cpu / limit_time_real",
                "PostgreSQL connection pooling & max_connections",
                "Longpolling / WebSocket handlers for scale",
                "Spotting missing indexes on custom models",
                "Slow queries with pg_stat_statements",
                "Redis for session storage/caching (distributed setups)",
                "Load balancing multiple Odoo instances behind Nginx",
                "Monitoring with Prometheus and Grafana (overview)",
            ],
        )
    )
    story.append(
        Paragraph(
            "<b>Lab:</b> Produce a capacity worksheet for a 4-vCPU / 8 GB VPS and apply conf changes with before/after notes.",
            styles["meta"],
        )
    )
    story.append(PageBreak())

    # ========== D4 CI/CD ==========
    story.append(section_banner(styles, "D4", "CI/CD & Monitoring Basics"))
    story.append(Spacer(1, 8))
    story.append(
        Paragraph(
            "Close the operations loop with lightweight automation: lint/test on pull requests, "
            "build checks for modules, and basic uptime/resource monitoring.",
            styles["body"],
        )
    )
    story.extend(
        bullets(
            styles,
            [
                "GitHub Actions workflow sketch for module CI (install, pylint-odoo optional, tests)",
                "Environment secrets management principles",
                "Smoke-test checklist after deploy (login, ACL sample, report print, longpolling)",
                "Prometheus/Grafana dashboards — what to watch first (CPU, RAM, DB connections, response time)",
            ],
        )
    )
    story.append(PageBreak())

    # ========== 27 Schedule ==========
    story.append(section_banner(styles, "27", "Recommended Weekly Schedule"))
    story.append(Spacer(1, 8))
    story.append(
        Paragraph(
            "Example 12-week Professional Track (≈10–12 hours/week). Intensive cohorts can map "
            "each week below to ~2–3 bootcamp days.",
            styles["body"],
        )
    )
    story.append(
        simple_table(
            styles,
            ["Week", "Focus", "Deliverable"],
            [
                ["1", "Linux CLI + SSH + systemd", "Hardened practice VM notes"],
                ["2", "Python core + collections + flow", "Exercises set A"],
                ["3", "Python OOP + modules + venv", "CLI app + diagnostic quiz"],
                ["4", "PostgreSQL + backups", "SQL lab workbook"],
                ["5", "Odoo install + conf + CLI", "Running local Odoo 17"],
                ["6", "Modules + fields", "wl_student scaffold with field set"],
                ["7", "ORM methods + special commands", "Overrides + domain drills"],
                ["8", "Views + inheritance attributes", "List/form/search/kanban pack"],
                ["9", "Security groups/ACLs/rules (+ Odoo 19 notes)", "Role-based demo DB"],
                ["10", "QWeb + XML/CSV data", "PDF report + demo data"],
                ["11", "OWL/POS + XML-RPC + email/actions", "Integration mini-project"],
                ["12", "Docker + VPS/Nginx/SSL + workers + capstone", "Deployed capstone defense"],
            ],
            [1.8 * cm, 7.5 * cm, 7.1 * cm],
        )
    )
    story.append(PageBreak())

    # ========== 28 Capstones ==========
    story.append(section_banner(styles, "28", "Capstone Project Briefs"))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Capstone A — Academic Institute Manager", styles["h2"]))
    story.extend(
        bullets(
            styles,
            [
                "Models: Student, Course, Enrollment, Attendance, Fee Payment",
                "Views: list/form/search/kanban/graph; statusbar on enrollment",
                "Security: Admin/Registrar/Teacher groups with record rules",
                "Report: Enrollment confirmation PDF with QR",
                "Automation: Email on enrollment confirmation (template)",
                "Ops bonus: Docker Compose or Nginx deployment notes",
            ],
        )
    )
    story.append(Paragraph("Capstone B — Retail POS Helper", styles["h2"]))
    story.extend(
        bullets(
            styles,
            [
                "POS button + popup + RPC persistence of cashier note",
                "Backend model storing notes linked to pos.order",
                "ACL for managers only on note analysis menu",
                "Optional XML-RPC script to export daily notes",
            ],
        )
    )
    story.append(Paragraph("Capstone C — Ops Excellence Pack", styles["h2"]))
    story.extend(
        bullets(
            styles,
            [
                "Production-like directory layout + systemd unit",
                "Nginx + longpolling + Certbot (or staging TLS)",
                "Backup cron + restore rehearsal document",
                "Worker sizing worksheet + pg_stat_statements sample",
            ],
        )
    )
    story.append(PageBreak())

    # ========== 29 Instructor checklist ==========
    story.append(section_banner(styles, "29", "Instructor Delivery Checklist"))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Before Cohort Start", styles["h2"]))
    story.extend(
        bullets(
            styles,
            [
                "Provision shared lab VM image (Ubuntu 22.04) and optional 24.04 preview image",
                "Prepare Odoo 17 source pin + sample odoo.conf + addons skeleton",
                "Validate PostgreSQL role scripts and Docker Compose demo",
                "Distribute this Training Plan + Presentation PDF",
            ],
        )
    )
    story.append(Paragraph("During Delivery", styles["h2"]))
    story.extend(
        bullets(
            styles,
            [
                "Start each module with outcomes and exit gate",
                "Live-code then freeze a reference commit for learners",
                "Enforce security discussions before fancy UX",
                "Keep a parking lot for Odoo 19 deltas; schedule explicit comparison session",
            ],
        )
    )
    story.append(Paragraph("After Delivery", styles["h2"]))
    story.extend(
        bullets(
            styles,
            [
                "Collect rubrics and archive capstone repos",
                "Update curriculum changelog (attrs, privilege model, CLI flags)",
                "Retrospective: which labs overran; adjust hour table",
            ],
        )
    )
    story.append(PageBreak())

    # ========== 30 Appendices ==========
    story.append(section_banner(styles, "30", "Appendices — Cheat Sheets & Glossary"))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Appendix A — Essential Odoo CLI Flags", styles["h2"]))
    story.append(
        simple_table(
            styles,
            ["Flag / Command", "Purpose"],
            [
                ["odoo-bin -c odoo.conf", "Start with configuration file"],
                ["-i module_name", "Install module"],
                ["-u module_name", "Upgrade module"],
                ["--db-filter=^db$", "Restrict DB listing/selection"],
                ["shell -d dbname", "Interactive ORM shell"],
                ["--stop-after-init", "Run init/ops then exit (CI friendly)"],
            ],
            [6.5 * cm, 9.9 * cm],
        )
    )
    story.append(Paragraph("Appendix B — Security Object Quick Map", styles["h2"]))
    story.append(
        simple_table(
            styles,
            ["Object", "Role"],
            [
                ["res.groups", "Permission bundles assigned to users"],
                ["ir.module.category", "Security category / app grouping"],
                ["ir.model.access", "CRUD permissions per model/group"],
                ["ir.rule", "Record-level domain restrictions"],
                ["groups on views/fields", "UI and field visibility controls"],
            ],
            [5.0 * cm, 11.4 * cm],
        )
    )
    story.append(PageBreak())

    story.append(Paragraph("Appendix C — Special Commands Reminder", styles["h2"]))
    story.append(
        simple_table(
            styles,
            ["Command", "Meaning"],
            [
                ["(0, 0, values)", "Create a new record on O2M/M2M"],
                ["(1, id, values)", "Update existing linked record"],
                ["(2, id)", "Remove and delete record"],
                ["(3, id)", "Unlink / remove relation without deleting"],
                ["(4, id)", "Link existing record"],
                ["(5,)", "Unlink all (clear)"],
                ["(6, 0, ids)", "Replace set with given ids"],
            ],
            [4.5 * cm, 11.9 * cm],
        )
    )
    story.append(Paragraph("Appendix D — Glossary (Selected)", styles["h2"]))
    story.extend(
        bullets(
            styles,
            [
                "<b>Addon / Module</b> — installable unit with manifest and code",
                "<b>Recordset</b> — ORM collection of records supporting mapped/filtered/sorted",
                "<b>XML ID</b> — external identifier in ir.model_data",
                "<b>Longpolling</b> — bus/websocket-style notifications channel (8072)",
                "<b>Worker</b> — multiprocess HTTP worker serving concurrent requests",
                "<b>OWL</b> — Odoo Web Library reactive UI framework",
                "<b>QWeb</b> — templating engine for reports and web client XML",
                "<b>Privilege (Odoo 19)</b> — evolved security concept beyond classic-only groups",
            ],
        )
    )
    story.append(PageBreak())

    # Closing page
    story.append(Paragraph("Curriculum Closure & Next Steps", styles["h1"]))
    story.append(
        HRFlowable(width="100%", thickness=1, color=TEAL, spaceAfter=10)
    )
    story.append(
        Paragraph(
            "This Training Plan is the master syllabus for the Odoo Full-Stack Developer Program. "
            "Use it with the companion Presentation PDF for kickoffs, stakeholder reviews, and "
            "week-one orientation. Instructors should treat version deltas (especially Odoo 19 "
            "security) as living addenda.",
            styles["body"],
        )
    )
    story.append(Paragraph("Recommended Companion Assets", styles["h2"]))
    story.extend(
        bullets(
            styles,
            [
                "Odoo_FullStack_Training_Presentation.pdf — slide deck for facilitation",
                "Lab repository template with wl_student skeleton",
                "Docker Compose starter + Nginx conf samples",
                "Capstone rubric spreadsheet",
            ],
        )
    )
    story.append(Spacer(1, 12))
    story.append(
        callout_box(
            styles,
            "Ship competence, not just content coverage. Every module ends with a working artifact "
            "that could survive a code review in a real Odoo project.",
            "Program Principle",
        )
    )
    story.append(Spacer(1, 20))
    story.append(Paragraph("Document control", styles["h3"]))
    story.append(
        simple_table(
            styles,
            ["Field", "Value"],
            [
                ["Document Title", "Odoo Full-Stack Developer Training Plan"],
                ["Edition", datetime.now().strftime("%Y.%m")],
                ["Primary Versions", "Odoo 17 (core) · Odoo 18/19 (delta track)"],
                ["Classification", "Training Curriculum — Professional"],
                ["Page Target", "30+ pages (this edition)"],
            ],
            [4.5 * cm, 11.9 * cm],
        )
    )

    doc.build(story)
    return OUTPUT


if __name__ == "__main__":
    path = build()
    print(f"Wrote {path}")

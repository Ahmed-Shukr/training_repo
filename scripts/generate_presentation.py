#!/usr/bin/env python3
"""Generate a professional Odoo Full-Stack Training Presentation PDF (landscape slides)."""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    NextPageTemplate,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)
from datetime import datetime
import os

OUTPUT = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "training_materials",
    "Odoo_FullStack_Training_Presentation.pdf",
)

NAVY = colors.HexColor("#0B2B3C")
TEAL = colors.HexColor("#0E6B6B")
TEAL_LIGHT = colors.HexColor("#E6F3F3")
SLATE = colors.HexColor("#334155")
MUTED = colors.HexColor("#64748B")
LINE = colors.HexColor("#CBD5E1")
WHITE = colors.white
SOFT = colors.HexColor("#F8FAFC")
TEAL_SOFT = colors.HexColor("#7DCBCB")

PAGE_W, PAGE_H = landscape(A4)


def styles():
    return {
        "eyebrow": ParagraphStyle(
            "eyebrow", fontName="Helvetica-Bold", fontSize=11, textColor=TEAL, spaceAfter=6
        ),
        "h": ParagraphStyle(
            "h", fontName="Helvetica-Bold", fontSize=22, textColor=NAVY, leading=26, spaceAfter=12
        ),
        "bullet": ParagraphStyle(
            "bullet",
            fontName="Helvetica",
            fontSize=13,
            textColor=SLATE,
            leading=19,
            leftIndent=2,
            spaceAfter=3,
        ),
        "small": ParagraphStyle(
            "small", fontName="Helvetica", fontSize=11, textColor=MUTED, leading=15
        ),
        "card_title": ParagraphStyle(
            "card_title",
            fontName="Helvetica-Bold",
            fontSize=12,
            textColor=NAVY,
            leading=15,
            spaceAfter=4,
        ),
        "card_body": ParagraphStyle(
            "card_body", fontName="Helvetica", fontSize=10.5, textColor=SLATE, leading=14
        ),
        "white_title": ParagraphStyle(
            "white_title",
            fontName="Helvetica-Bold",
            fontSize=26,
            textColor=WHITE,
            leading=32,
            alignment=1,
        ),
        "white_sub": ParagraphStyle(
            "white_sub",
            fontName="Helvetica",
            fontSize=13,
            textColor=colors.HexColor("#D1E8E8"),
            leading=18,
            alignment=1,
        ),
        "brand": ParagraphStyle(
            "brand",
            fontName="Helvetica-Bold",
            fontSize=14,
            textColor=TEAL_SOFT,
            alignment=1,
            spaceAfter=8,
        ),
        "table_h": ParagraphStyle(
            "table_h", fontName="Helvetica-Bold", fontSize=11, textColor=WHITE, leading=14
        ),
        "table_c": ParagraphStyle(
            "table_c", fontName="Helvetica", fontSize=10.5, textColor=SLATE, leading=14
        ),
        "big_num": ParagraphStyle(
            "big_num", fontName="Helvetica-Bold", fontSize=20, textColor=TEAL, alignment=1
        ),
        "num_label": ParagraphStyle(
            "num_label", fontName="Helvetica", fontSize=10, textColor=SLATE, alignment=1, leading=13
        ),
    }


def slide_chrome(c, doc):
    c.saveState()
    c.setFillColor(TEAL)
    c.rect(0, 0, 0.45 * cm, PAGE_H, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.rect(0, PAGE_H - 1.05 * cm, PAGE_W, 1.05 * cm, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica", 9)
    c.drawString(0.9 * cm, PAGE_H - 0.65 * cm, "Weblearns Academy")
    c.drawRightString(PAGE_W - 0.9 * cm, PAGE_H - 0.65 * cm, "Odoo Full-Stack Training")
    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    c.line(0.9 * cm, 0.85 * cm, PAGE_W - 0.9 * cm, 0.85 * cm)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 8)
    c.drawString(0.9 * cm, 0.45 * cm, "Professional Training Presentation")
    c.drawRightString(PAGE_W - 0.9 * cm, 0.45 * cm, f"{doc.page}")
    c.restoreState()


def title_slide_bg(c, doc):
    c.saveState()
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(TEAL)
    c.rect(0, 0, PAGE_W, 1.4 * cm, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#123A4C"))
    c.circle(PAGE_W - 2 * cm, PAGE_H - 2 * cm, 6 * cm, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#9FB3BD"))
    c.setFont("Helvetica", 8)
    c.drawCentredString(PAGE_W / 2, 0.55 * cm, datetime.now().strftime("%B %Y"))
    c.restoreState()


def section_slide_bg(c, doc):
    c.saveState()
    c.setFillColor(TEAL)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(NAVY)
    c.rect(0, 0, PAGE_W * 0.38, PAGE_H, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont("Helvetica", 9)
    c.drawString(1 * cm, 0.6 * cm, f"Section divider  ·  {doc.page}")
    c.restoreState()


def bullets(s, items):
    return [Paragraph(f"▸  {item}", s["bullet"]) for item in items]


def cards_row(s, items, widths=None):
    n = len(items)
    if not widths:
        total = PAGE_W - 2.2 * cm
        widths = [total / n] * n
    col_tables = []
    for i, (title, body) in enumerate(items):
        t = Table(
            [[Paragraph(title, s["card_title"])], [Paragraph(body, s["card_body"])]],
            colWidths=[widths[i] - 0.35 * cm],
        )
        t.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), SOFT),
                    ("BOX", (0, 0), (-1, -1), 0.8, TEAL),
                    ("LEFTPADDING", (0, 0), (-1, -1), 10),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                    ("TOPPADDING", (0, 0), (-1, -1), 8),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ]
            )
        )
        col_tables.append(t)
    row = Table([col_tables], colWidths=widths)
    row.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
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
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return t


def build():
    s = styles()
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)

    doc = BaseDocTemplate(
        OUTPUT,
        pagesize=landscape(A4),
        leftMargin=1.0 * cm,
        rightMargin=1.0 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.3 * cm,
        title="Odoo Full-Stack Training Presentation",
        author="Weblearns Academy",
    )

    frame = Frame(1.0 * cm, 1.2 * cm, PAGE_W - 2.0 * cm, PAGE_H - 2.6 * cm, id="body")
    full = Frame(0, 0, PAGE_W, PAGE_H, id="full")
    doc.addPageTemplates(
        [
            PageTemplate(id="Title", frames=full, onPage=title_slide_bg),
            PageTemplate(id="Section", frames=full, onPage=section_slide_bg),
            PageTemplate(id="Slide", frames=frame, onPage=slide_chrome),
        ]
    )

    story = []

    def add_slide(builder):
        story.append(NextPageTemplate("Slide"))
        story.append(PageBreak())
        builder()

    def add_section(code, title, subtitle):
        story.append(NextPageTemplate("Section"))
        story.append(PageBreak())
        story.append(Spacer(1, 4.5 * cm))
        story.append(Paragraph(code, s["white_sub"]))
        story.append(Spacer(1, 0.3 * cm))
        story.append(Paragraph(title, s["white_title"]))
        story.append(Spacer(1, 0.4 * cm))
        story.append(Paragraph(subtitle, s["white_sub"]))

    # Title
    story.append(NextPageTemplate("Title"))
    story.append(Spacer(1, 5.2 * cm))
    story.append(Paragraph("ODOO FULL-STACK DEVELOPER PROGRAM", s["brand"]))
    story.append(Paragraph("Training Presentation", s["white_title"]))
    story.append(Spacer(1, 0.4 * cm))
    story.append(
        Paragraph("Linux · Python · PostgreSQL · Odoo 17/18/19 · OWL · DevOps", s["white_sub"])
    )
    story.append(Spacer(1, 1.2 * cm))
    story.append(
        Paragraph("Companion to the Master Training Plan  ·  Professional Edition", s["white_sub"])
    )

    add_slide(
        lambda: (
            story.append(Paragraph("AGENDA", s["eyebrow"])),
            story.append(Paragraph("What We Will Cover", s["h"])),
            story.append(
                cards_row(
                    s,
                    [
                        ("01 Foundations", "Linux CLI, Python for Odoo, PostgreSQL administration"),
                        ("02 Odoo Core", "Install, modules, fields, ORM, views, security, data"),
                        ("03 Advanced", "QWeb, OWL, POS, XML-RPC, email & server actions"),
                        ("04 Production", "Docker, VPS/Nginx/SSL, workers, CI/CD & monitoring"),
                    ],
                    [6.8 * cm] * 4,
                )
            ),
        )
    )

    add_slide(
        lambda: (
            story.append(Paragraph("PROGRAM VISION", s["eyebrow"])),
            story.append(Paragraph("From First Terminal Command to Production Odoo", s["h"])),
            story.extend(
                bullets(
                    s,
                    [
                        "Build developers who can ship maintainable Odoo business modules",
                        "Teach security and operations with the same rigor as features",
                        "Cover Odoo 17 deeply, then map Odoo 18/19 deltas intentionally",
                        "End with deployable artifacts—not only slide knowledge",
                    ],
                )
            ),
        )
    )

    add_slide(
        lambda: (
            story.append(Paragraph("OUTCOMES", s["eyebrow"])),
            story.append(Paragraph("Graduates Can…", s["h"])),
            story.append(
                cards_row(
                    s,
                    [
                        (
                            "Develop",
                            "Scaffold modules, design models/fields, override ORM safely, craft views",
                        ),
                        ("Secure", "Groups, ACLs, record rules, Odoo 19 privilege awareness"),
                        (
                            "Extend",
                            "QWeb PDFs, OWL widgets, POS customizations, XML-RPC integrations",
                        ),
                        ("Operate", "Docker Compose, Nginx/SSL, systemd, worker sizing, backups"),
                    ],
                )
            ),
        )
    )

    add_slide(
        lambda: (
            story.append(Paragraph("LEARNING JOURNEY", s["eyebrow"])),
            story.append(Paragraph("Six Progressive Phases", s["h"])),
            story.append(
                simple_table(
                    s,
                    ["Phase", "Modules", "Exit Gate"],
                    [
                        ["1 Foundations", "F1–F3", "CLI + Python + SQL labs passed"],
                        ["2 Odoo Core", "O1–O4", "Custom module with CRUD logic"],
                        ["3 UX & Security", "O5–O8", "Secured app with list/form/search"],
                        ["4 Advanced", "A1–A6", "Report + OWL/POS + XML-RPC demo"],
                        ["5 Operations", "D1–D4", "HTTPS stack with workers tuned"],
                        ["6 Capstone", "Projects", "Reviewed production-ready delivery"],
                    ],
                    [5.5 * cm, 5.5 * cm, 16 * cm],
                )
            ),
        )
    )

    add_section("PART ONE", "Foundations", "Linux  ·  Python  ·  PostgreSQL")

    add_slide(
        lambda: (
            story.append(Paragraph("MODULE F1", s["eyebrow"])),
            story.append(Paragraph("Linux OS & CLI Mastery", s["h"])),
            story.append(
                cards_row(
                    s,
                    [
                        ("Navigate & Manage", "pwd/cd/ls/tree · cp/mv/rm · permissions · users/sudo"),
                        ("Operate Services", "systemctl · journalctl · processes · apt packages"),
                        ("Secure & Automate", "SSH hardening · UFW · cron · env/.bashrc · disk checks"),
                    ],
                    [9 * cm] * 3,
                )
            ),
            story.append(Spacer(1, 0.5 * cm)),
            story.append(
                Paragraph("Lab: project tree under /opt/training + sample systemd unit", s["small"])
            ),
        )
    )

    add_slide(
        lambda: (
            story.append(Paragraph("MODULE F2", s["eyebrow"])),
            story.append(Paragraph("Python for Odoo Developers", s["h"])),
            story.extend(
                bullets(
                    s,
                    [
                        "Core syntax → collections → control flow → functions",
                        "OOP (inheritance, MRO, dunders) mapped to Odoo model thinking",
                        "Functional tools, decorators, errors, generators, packages",
                        "Tooling: venv, pip, PEP8, VS Code/PyCharm, debugging",
                    ],
                )
            ),
            story.append(Spacer(1, 0.3 * cm)),
            story.append(
                Paragraph("Lab Cap: CLI contact manager with classes + persistence", s["small"])
            ),
        )
    )

    add_slide(
        lambda: (
            story.append(Paragraph("MODULE F3", s["eyebrow"])),
            story.append(Paragraph("PostgreSQL Administration", s["h"])),
            story.append(
                cards_row(
                    s,
                    [
                        ("Setup", "Install on Ubuntu LTS · psql · roles · grants · pg_hba/conf"),
                        ("SQL Fluency", "DDL · CRUD · joins · aggregations · constraints"),
                        ("Ops", "Indexes · EXPLAIN · pg_dump/restore · locks & sessions"),
                    ],
                    [9 * cm] * 3,
                )
            ),
        )
    )

    add_section(
        "PART TWO",
        "Odoo Core Development",
        "Install → Modules → Fields → ORM → Views → Security",
    )

    add_slide(
        lambda: (
            story.append(Paragraph("MODULE O1", s["eyebrow"])),
            story.append(Paragraph("Installation, CLI & Configuration", s["h"])),
            story.extend(
                bullets(
                    s,
                    [
                        "Odoo 17 on Ubuntu 22.04 · Odoo 19 preview on Ubuntu 24.04",
                        "odoo-bin startup · configuration file · PyCharm run configs",
                        "Database manager URLs · disable DB selector · master password",
                        "Install/upgrade modules via CLI · shell · logs · migration upgrade code",
                    ],
                )
            ),
        )
    )

    add_slide(
        lambda: (
            story.append(Paragraph("MODULE O2", s["eyebrow"])),
            story.append(Paragraph("Modules, Manifest & Addons Paths", s["h"])),
            story.append(
                cards_row(
                    s,
                    [
                        ("Scaffold", "Create modules with scaffold; understand _name/_table"),
                        ("Manifest", "Metadata, depends, data/demo ordering, application flag"),
                        ("Paths", "Multi addons-path · App Store layouts · auto-install patterns"),
                    ],
                    [9 * cm] * 3,
                )
            ),
        )
    )

    add_slide(
        lambda: (
            story.append(Paragraph("MODULE O3", s["eyebrow"])),
            story.append(Paragraph("Fields & Model Design", s["h"])),
            story.append(
                simple_table(
                    s,
                    ["Category", "Field Types Practiced"],
                    [
                        [
                            "Scalar",
                            "Char · Text · Html · Boolean · Selection · Integer · Float · Json",
                        ],
                        ["Temporal", "Date · Datetime"],
                        ["Relational", "Many2one · One2many · Many2many · Reference · Related"],
                        ["Advanced", "Compute · Monetary · Binary · Image"],
                    ],
                    [5 * cm, 22 * cm],
                )
            ),
        )
    )

    add_slide(
        lambda: (
            story.append(Paragraph("MODULE O4", s["eyebrow"])),
            story.append(Paragraph("ORM Methods Deep Dive", s["h"])),
            story.append(
                cards_row(
                    s,
                    [
                        ("Lifecycle", "create · write · copy · unlink · custom methods · exists"),
                        (
                            "Query APIs",
                            "search/domains · read* · name_create · default_get · search_fetch",
                        ),
                        ("Recordsets", "ensure_one · filtered · mapped · sorted · grouped"),
                        ("Special Cmds", "[0]..[6] relational commands · active/archive patterns"),
                    ],
                )
            ),
        )
    )

    add_slide(
        lambda: (
            story.append(Paragraph("MODULE O5", s["eyebrow"])),
            story.append(Paragraph("Views for Real Business UX", s["h"])),
            story.extend(
                bullets(
                    s,
                    [
                        "List: editable, decorations, mass edit, headers/buttons, aggregates, handle widget",
                        "Search: panel, dynamic datetime filters, default filters",
                        "Form: sheet/header/group/notebook/buttons/statusbar",
                        "Kanban + Graph/Pivot/Cohort/Gantt · attrs → invisible/readonly/required migration",
                    ],
                )
            ),
        )
    )

    add_slide(
        lambda: (
            story.append(Paragraph("MODULE O6", s["eyebrow"])),
            story.append(Paragraph("Security — The Non-Negotiable Layer", s["h"])),
            story.append(
                cards_row(
                    s,
                    [
                        ("Groups", "Categories · parent/child · implied_ids · combobox layouts"),
                        ("Access", "ir.model.access via CSV and XML"),
                        ("Record Rules", "Teacher/Student/Admin scenarios · inheritance"),
                        ("Odoo 19", "Privilege model changes · groups on fields/views/actions"),
                    ],
                )
            ),
        )
    )

    add_slide(
        lambda: (
            story.append(Paragraph("MODULES O7–O8", s["eyebrow"])),
            story.append(Paragraph("Data Loading & View Inheritance", s["h"])),
            story.append(
                cards_row(
                    s,
                    [
                        (
                            "XML & CSV Data",
                            "Records, eval, images, M2O/M2M/O2M, binaries; when to choose XML vs CSV",
                        ),
                        (
                            "Inheritance",
                            "field tag · xpath · positions after/before/inside/replace/attributes",
                        ),
                        (
                            "Extras",
                            "URL actions · ir.sequence auto-numbering · upgrade-safe xpath habits",
                        ),
                    ],
                    [9 * cm] * 3,
                )
            ),
        )
    )

    add_section("PART THREE", "Advanced Odoo", "QWeb · OWL · POS · APIs · Automation")

    add_slide(
        lambda: (
            story.append(Paragraph("MODULE A1", s["eyebrow"])),
            story.append(Paragraph("QWeb PDF Reports", s["h"])),
            story.extend(
                bullets(
                    s,
                    [
                        "t-field / t-esc / t-out · conditionals · loops · variables · t-att/t-attf",
                        "Template inheritance · paper formats · barcodes/QR · static & dynamic images",
                        "Lab: enrollment confirmation / student ID PDF",
                    ],
                )
            ),
        )
    )

    add_slide(
        lambda: (
            story.append(Paragraph("MODULE A2", s["eyebrow"])),
            story.append(Paragraph("OWL Framework", s["h"])),
            story.append(
                cards_row(
                    s,
                    [
                        ("Components", "Lifecycle · useState/useRef · events · props"),
                        ("Templates", "t-if · t-foreach · t-model · custom field widgets"),
                        ("Integration", "patch() · rpc service · custom Kanban/Dashboard views"),
                    ],
                    [9 * cm] * 3,
                )
            ),
        )
    )

    add_slide(
        lambda: (
            story.append(Paragraph("MODULE A3", s["eyebrow"])),
            story.append(Paragraph("POS Customization with OWL", s["h"])),
            story.extend(
                bullets(
                    s,
                    [
                        "Custom buttons · click handlers · hide standard controls",
                        "Popups · JS translations · RPC fetch/render · clear order lines",
                        "Lab: Manager Note popup persisted on pos.order",
                    ],
                )
            ),
        )
    )

    add_slide(
        lambda: (
            story.append(Paragraph("MODULES A4–A6", s["eyebrow"])),
            story.append(Paragraph("Integrations & Automation", s["h"])),
            story.append(
                cards_row(
                    s,
                    [
                        (
                            "XML-RPC",
                            "Auth · export · CRUD · Postman verification · least-privilege users",
                        ),
                        ("Email", "Templates · send flows tied to business events"),
                        ("Server Actions", "Use cases · UI triggers · safe Python practices"),
                    ],
                    [9 * cm] * 3,
                )
            ),
        )
    )

    add_section("PART FOUR", "DevOps & Production", "Docker · VPS · Nginx · Performance · CI/CD")

    add_slide(
        lambda: (
            story.append(Paragraph("MODULE D1", s["eyebrow"])),
            story.append(Paragraph("Docker & Compose for Odoo", s["h"])),
            story.extend(
                bullets(
                    s,
                    [
                        "Images/containers/volumes/networks · custom Dockerfiles",
                        "Compose: Odoo + PostgreSQL · .env · upgrade without data loss",
                        "CI/CD primer with GitHub Actions for module checks",
                    ],
                )
            ),
        )
    )

    add_slide(
        lambda: (
            story.append(Paragraph("MODULE D2", s["eyebrow"])),
            story.append(Paragraph("VPS Deployment Blueprint", s["h"])),
            story.append(
                simple_table(
                    s,
                    ["Layer", "Action"],
                    [
                        ["Security", "SSH hardening · UFW · least privilege odoo user"],
                        ["Layout", "/opt/odoo · logs · custom addons"],
                        ["Proxy/TLS", "Nginx 80/443 → 8069 · longpolling 8072 · Certbot"],
                        ["Runtime", "systemd odoo.service · cron DB+filestore backups"],
                    ],
                    [5 * cm, 22 * cm],
                )
            ),
        )
    )

    add_slide(
        lambda: (
            story.append(Paragraph("MODULE D3", s["eyebrow"])),
            story.append(Paragraph("Workers & Performance", s["h"])),
            story.append(
                cards_row(
                    s,
                    [
                        ("Sizing", "Workers from CPU/RAM · memory & time limits"),
                        ("Data Layer", "max_connections · missing indexes · pg_stat_statements"),
                        (
                            "Scale Out",
                            "Longpolling · Redis sessions · Nginx LB · Prometheus/Grafana",
                        ),
                    ],
                    [9 * cm] * 3,
                )
            ),
        )
    )

    stats = Table(
        [
            [
                Paragraph("120+", s["big_num"]),
                Paragraph("12–16", s["big_num"]),
                Paragraph("6–8", s["big_num"]),
                Paragraph("3", s["big_num"]),
            ],
            [
                Paragraph("Guided learning hours", s["num_label"]),
                Paragraph("Weeks professional track", s["num_label"]),
                Paragraph("Weeks intensive bootcamp", s["num_label"]),
                Paragraph("Capstone project choices", s["num_label"]),
            ],
        ],
        colWidths=[6.75 * cm] * 4,
    )
    stats.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), TEAL_LIGHT),
                ("BOX", (0, 0), (-1, -1), 1, TEAL),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, LINE),
                ("TOPPADDING", (0, 0), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )

    add_slide(
        lambda: (
            story.append(Paragraph("DELIVERY MODEL", s["eyebrow"])),
            story.append(Paragraph("Time & Format Options", s["h"])),
            story.append(stats),
        )
    )

    add_slide(
        lambda: (
            story.append(Paragraph("CAPSTONES", s["eyebrow"])),
            story.append(Paragraph("Choose a Path to Demonstrate Mastery", s["h"])),
            story.append(
                cards_row(
                    s,
                    [
                        (
                            "A · Institute Manager",
                            "Students, courses, enrollment, fees, security roles, QWeb PDF, email automation",
                        ),
                        (
                            "B · Retail POS Helper",
                            "OWL POS button/popup/RPC note on orders + manager ACL + optional XML-RPC export",
                        ),
                        (
                            "C · Ops Excellence",
                            "systemd + Nginx/TLS + backups + worker worksheet + restore rehearsal",
                        ),
                    ],
                    [9 * cm] * 3,
                )
            ),
        )
    )

    add_slide(
        lambda: (
            story.append(Paragraph("ASSESSMENT", s["eyebrow"])),
            story.append(Paragraph("How Competence Is Measured", s["h"])),
            story.append(
                simple_table(
                    s,
                    ["Component", "Weight", "Evidence"],
                    [
                        ["Module Labs", "40%", "Working code + screenshots"],
                        ["Knowledge Checks", "15%", "ORM · security · CLI · SQL quizzes"],
                        ["Mini-Projects", "20%", "Integrated feature slices"],
                        ["Final Capstone", "25%", "Deployable module + docs + demo"],
                    ],
                    [7 * cm, 4 * cm, 16 * cm],
                )
            ),
        )
    )

    add_slide(
        lambda: (
            story.append(Paragraph("12-WEEK SNAPSHOT", s["eyebrow"])),
            story.append(Paragraph("Professional Track at a Glance", s["h"])),
            story.append(
                simple_table(
                    s,
                    ["Weeks", "Focus"],
                    [
                        ["1–4", "Linux · Python · PostgreSQL foundations"],
                        ["5–7", "Odoo install · modules · fields · ORM"],
                        ["8–9", "Views · inheritance · security (+ Odoo 19 notes)"],
                        ["10–11", "QWeb · OWL/POS · XML-RPC · email/actions"],
                        ["12", "Docker · VPS/Nginx · workers · capstone defense"],
                    ],
                    [4.5 * cm, 22.5 * cm],
                )
            ),
        )
    )

    add_slide(
        lambda: (
            story.append(Paragraph("FACILITATION PRINCIPLES", s["eyebrow"])),
            story.append(Paragraph("How We Teach", s["h"])),
            story.extend(
                bullets(
                    s,
                    [
                        "Outcomes first — every session names an exit gate",
                        "Security before spectacle — ACLs precede fancy widgets",
                        "Version honesty — Odoo 17 core, Odoo 19 deltas called out explicitly",
                        "Artifacts over attendance — labs must run on a reviewer’s machine",
                    ],
                )
            ),
        )
    )

    story.append(NextPageTemplate("Title"))
    story.append(PageBreak())
    story.append(Spacer(1, 4.2 * cm))
    story.append(Paragraph("NEXT STEP", s["white_sub"]))
    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph("Open the Training Plan", s["white_title"]))
    story.append(Paragraph("and Start Module F1", s["white_title"]))
    story.append(Spacer(1, 0.6 * cm))
    story.append(
        Paragraph("Document: Odoo_FullStack_Developer_Training_Plan.pdf", s["white_sub"])
    )
    story.append(Spacer(1, 1.0 * cm))
    story.append(
        Paragraph("Weblearns Academy  ·  Odoo Full-Stack Developer Program", s["white_sub"])
    )

    doc.build(story)
    return OUTPUT


if __name__ == "__main__":
    path = build()
    print(f"Wrote {path}")

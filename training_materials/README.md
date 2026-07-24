# Odoo Full-Stack Developer Training Materials

Complete teaching documentation and per-section lecture presentations for the
Odoo Full-Stack Developer Program (Linux, Python, PostgreSQL, Odoo 17/18/19,
OWL/POS, Infrastructure).

## 1. Full Training Documentation (~300 pages of detailed content)

| File | Description |
|------|-------------|
| [`Odoo_FullStack_Training_Documentation.pdf`](Odoo_FullStack_Training_Documentation.pdf) | Full-page lesson documentation: objectives, explanations, examples, mistakes, labs |

Covers 160 lessons across Foundations → Odoo Core → Views/Security/QWeb → OWL/POS/APIs → Infrastructure.

## 2. Section Presentation Decks (Cookie-style lecture materials)

Modern Beamer-inspired theme: Inter typography, blue accent rail, diagonal
title art, TOC watermark agenda, numbered section dividers, progress bar,
and pill tags.

Located in [`presentations/`](presentations/):

| Deck | Focus | Slides (approx.) |
|------|-------|------------------|
| `01_Linux_CLI_Mastery.pdf` | Linux OS & CLI | ~173 |
| `02_Python_for_Odoo.pdf` | Python for Odoo | ~224 |
| `03_PostgreSQL_Database.pdf` | PostgreSQL & SQL | ~122 |
| `04_Odoo_Core_Development.pdf` | Install, modules, fields, ORM | ~196 |
| `05_Views_Security_QWeb.pdf` | Views, security, data, QWeb | ~265 |
| `06_OWL_POS_APIs.pdf` | OWL, POS, XML-RPC | ~191 |
| `07_Infrastructure_DevOps.pdf` | Docker, VPS, Nginx, workers | ~190 |

**Total: ~1,360 teaching slides** with explanations, examples, pitfalls, and labs.

## Regenerate

```bash
pip install reportlab
python3 scripts/training_pdf/generate_documentation.py
python3 scripts/training_pdf/generate_section_presentations.py
```

Lesson source content lives in `scripts/training_pdf/content/`.

## Legacy short syllabus PDFs

Earlier short syllabus/overview PDFs may still exist in this folder for reference.
Prefer the Documentation + section decks above for teaching delivery.

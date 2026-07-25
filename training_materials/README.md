# Odoo Full-Stack Developer Training Materials

Complete teaching documentation and per-section lecture presentations for the
Odoo Full-Stack Developer Program (Linux, Python, PostgreSQL, Odoo 17/18/19,
OWL/POS, Infrastructure).

## 1. Full Training Documentation (~300 pages of detailed content)

| File | Description |
|------|-------------|
| [`Odoo_FullStack_Training_Documentation.pdf`](Odoo_FullStack_Training_Documentation.pdf) | Full-page lesson documentation: objectives, explanations, examples, mistakes, labs |

Covers 160 lessons across Foundations → Odoo Core → Views/Security/QWeb → OWL/POS/APIs → Infrastructure.

## 2. Section Presentation Decks (Merit Advisory · Cookie template)

Exact Cookie Beamer page size with concise beginner-friendly lecture slides:
- **Branding:** Merit Advisory
- **One topic per slide** (e.g. `pwd`, `cd`, Char field)
- Short professional bullets
- Terminal/result images (or code snapshots under the matching bullet)
- Teaching diagrams for topics like Linux permissions
- Agenda by Section 1..N (no TOC watermark, no objectives/method filler)

Located in [`presentations/`](presentations/):

| Deck | Focus | Slides |
|------|-------|--------|
| `01_Linux_CLI_Mastery.pdf` | Linux OS & CLI | ~65 |
| `02_Python_for_Odoo.pdf` | Python for Odoo | ~58 |
| `03_PostgreSQL_Database.pdf` | PostgreSQL & SQL | ~41 |
| `04_Odoo_Core_Development.pdf` | Install, modules, fields, ORM | ~60 |
| `05_Views_Security_QWeb.pdf` | Views, security, data, QWeb | ~54 |
| `06_OWL_POS_APIs.pdf` | OWL, POS, XML-RPC | ~39 |
| `07_Infrastructure_DevOps.pdf` | Docker, VPS, Nginx, workers | ~38 |

**Total: ~355 concise teaching slides**

Atomic slide source content: `scripts/training_pdf/content/slides_*.py`

## Regenerate

```bash
pip install reportlab pillow pypdf
python3 scripts/training_pdf/assets_gen/generate_slide_images.py
python3 scripts/training_pdf/generate_section_presentations.py
python3 scripts/training_pdf/generate_documentation.py   # optional full docs
```

Lesson source content lives in `scripts/training_pdf/content/`.
Slide image assets live in `training_materials/slide_assets/`.

## Legacy short syllabus PDFs

Earlier short syllabus/overview PDFs may still exist in this folder for reference.
Prefer the Documentation + section decks above for teaching delivery.

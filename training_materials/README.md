# Odoo Full-Stack Developer Training Materials

Complete teaching documentation and per-section lecture presentations for the
Odoo Full-Stack Developer Program (Linux, Python, PostgreSQL, Odoo 17/18/19,
OWL/POS, Infrastructure).

## 1. Full Training Documentation (~300 pages of detailed content)

| File | Description |
|------|-------------|
| [`Odoo_FullStack_Training_Documentation.pdf`](Odoo_FullStack_Training_Documentation.pdf) | Full-page lesson documentation: objectives, explanations, examples, mistakes, labs |

Covers 160 lessons across Foundations → Odoo Core → Views/Security/QWeb → OWL/POS/APIs → Infrastructure.

## 2. Section Presentation Decks (Cookie Beamer template)

Exact template match from the shared Cookie Beamer PDF:
- **Page size:** 453.54 × 255.12 pt (Beamer 16:9) — not A4
- **Fonts:** Noto Sans SemiCondensed + Noto Sans Mono SemiCondensed
- **Chrome:** blue accent, progress bar + dot, footer labels, blue `N / Total` counter
- **Layouts:** dense two-column frames, example/alert blocks, pill tags

Located in [`presentations/`](presentations/):

| Deck | Focus | Slides |
|------|-------|--------|
| `01_Linux_CLI_Mastery.pdf` | Linux OS & CLI | ~68 |
| `02_Python_for_Odoo.pdf` | Python for Odoo | ~103 |
| `03_PostgreSQL_Database.pdf` | PostgreSQL & SQL | ~64 |
| `04_Odoo_Core_Development.pdf` | Install, modules, fields, ORM | ~103 |
| `05_Views_Security_QWeb.pdf` | Views, security, data, QWeb | ~114 |
| `06_OWL_POS_APIs.pdf` | OWL, POS, XML-RPC | ~74 |
| `07_Infrastructure_DevOps.pdf` | Docker, VPS, Nginx, workers | ~74 |

**Total: ~600 teaching slides** packed to reduce empty whitespace.

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

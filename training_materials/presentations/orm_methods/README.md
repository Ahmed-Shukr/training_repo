# Odoo ORM Methods Presentation (BJT Beamer)

Beamer deck for **Odoo 17 Development Tutorials** by Ahmed Muhumed, built with the **bjt** class.

## Build

```bash
cd training_materials/presentations/orm_methods
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

Requires a TeX Live install with Beamer, Metropolis, Bookman, and Forest.

## Structure

- `main.tex` — bjt preamble, title/outline, and section inputs
- `sections/` — Introduction, `create()`, and every remaining ORM method
- `bjt.cls` + `bjt/` — Baijayanta Beamer theme (with local color / series-label tweaks)
- `orm_architecture.png` — architecture figure
- `backgrounds/wallpaper.jpg` — optional slide background used from Create onward

Compiled PDF is also copied to:

`training_materials/presentations/08_Odoo_ORM_Methods.pdf`

## Methods covered

`create`, `write`, `unlink`, `copy`, `exists`, `search`, `read`, `search_read`, `search_count`, `name_create`, `default_get`, `name_search`, `get_view`, `ensure_one`, `filtered`, `mapped`, `sorted`, `grouped`, `fields_get`, `get_metadata`

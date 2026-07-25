# Odoo ORM Methods Presentation

Beamer deck for **Odoo 17 Development Tutorials** by Ahmed Muhumed.

## Contents

1. Introduction to ORM Methods
2. `create()`
3. `write()`
4. `unlink()`
5. `copy()`
6. `exists()`
7. `search()`
8. `read()`
9. `search_read()`
10. `search_count()`
11. `name_create()`
12. `default_get()`
13. `name_search()`
14. `get_view()`
15. `ensure_one()`
16. `filtered()`
17. `mapped()`
18. `sorted()`
19. `grouped()`
20. `fields_get()`
21. `get_metadata()`

Each method is covered in the same teaching depth as `create()`: definition, method syntax, signature breakdown, return value, practical examples, and method-call notes.

## Build

```bash
cd training_materials/presentations/orm_methods
pdflatex -interaction=nonstopmode main.tex
```

The compiled PDF is also copied to:

`training_materials/presentations/08_Odoo_ORM_Methods.pdf`

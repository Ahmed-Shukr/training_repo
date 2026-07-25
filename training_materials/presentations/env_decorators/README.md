# Environment & Decorators Presentation (BJT)

Beamer deck for **Odoo 17 Development Tutorials** by Ahmed Muhumed.

## Topics
- `self.env` and environment components
- Accessing models, user/company, context
- `with_context`, `with_user`, `with_company`, `sudo()`, `env.ref`
- API decorators: `@api.model`, `@api.depends`, `@api.onchange`, `@api.constrains`, and more

## Build
```bash
cd training_materials/presentations/env_decorators
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

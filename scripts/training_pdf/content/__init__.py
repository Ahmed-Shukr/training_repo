"""Content modules for the Odoo training PDF generator."""

from .linux_lessons import LESSONS as LINUX_LESSONS
from .python_lessons import LESSONS as PYTHON_LESSONS

LESSONS = [*LINUX_LESSONS, *PYTHON_LESSONS]

__all__ = ["LESSONS", "LINUX_LESSONS", "PYTHON_LESSONS"]

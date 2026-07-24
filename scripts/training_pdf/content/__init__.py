from .linux_lessons import LESSONS as LINUX_LESSONS
from .python_lessons import LESSONS as PYTHON_LESSONS
from .postgres_lessons import LESSONS as POSTGRES_LESSONS
from .odoo_core_lessons import LESSONS as ODOO_CORE_LESSONS
from .odoo_views_security_lessons import LESSONS as ODOO_VIEWS_LESSONS
from .owl_pos_api_lessons import LESSONS as OWL_LESSONS
from .infra_lessons import LESSONS as INFRA_LESSONS

LESSONS = (
    LINUX_LESSONS
    + PYTHON_LESSONS
    + POSTGRES_LESSONS
    + ODOO_CORE_LESSONS
    + ODOO_VIEWS_LESSONS
    + OWL_LESSONS
    + INFRA_LESSONS
)

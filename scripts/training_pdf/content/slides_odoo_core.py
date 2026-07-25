"""Beginner-friendly Odoo core slide content."""

SLIDES = [
    {
        "section": 1,
        "title": "Odoo 17 Install Overview",
        "topics": [
            {
                "id": "ODOO-01",
                "title": "Odoo 17 Install Overview",
                "points": [
                    "Odoo needs Python, PostgreSQL, and system libraries.",
                    "A source install is useful for training.",
                    "Use a virtual environment for Python packages.",
                ],
                "examples": [
                    {
                        "label": "Clone source",
                        "code": "git clone --depth 1 --branch 17.0 https://github.com/odoo/odoo.git odoo17",
                    },
                    {
                        "label": "Install requirements",
                        "code": "python3 -m venv venv\nsource venv/bin/activate\npip install -r requirements.txt",
                    },
                ],
            }
        ],
    },
    {
        "section": 2,
        "title": "Start odoo-bin",
        "topics": [
            {
                "id": "ODOO-02",
                "title": "Start Odoo with odoo-bin",
                "points": [
                    "odoo-bin starts the Odoo server.",
                    "Run it from the source checkout.",
                    "Use explicit options while learning.",
                ],
                "examples": [
                    {
                        "label": "Start with config",
                        "code": "./odoo-bin -c /etc/odoo17.conf",
                    },
                    {
                        "label": "Start one database",
                        "code": "./odoo-bin -d odoo17_training --addons-path=addons",
                    },
                ],
            }
        ],
    },
    {
        "section": 3,
        "title": "odoo.conf Basics",
        "topics": [
            {
                "id": "ODOO-03",
                "title": "Understand odoo.conf Basics",
                "points": [
                    "The config file stores common startup options.",
                    "It keeps long commands readable.",
                    "Use one config per environment.",
                ],
                "examples": [
                    {
                        "label": "Minimal config",
                        "code": "[options]\naddons_path = /opt/odoo/odoo17/addons\ndb_host = 127.0.0.1",
                    },
                    {
                        "label": "Run with config",
                        "code": "./odoo-bin -c ./odoo17.conf",
                    },
                ],
            }
        ],
    },
    {
        "section": 4,
        "title": "Database Connection Options",
        "topics": [
            {
                "id": "ODOO-04",
                "title": "Set db_host, db_user, and db_password",
                "points": [
                    "These options tell Odoo how to reach PostgreSQL.",
                    "Use a dedicated PostgreSQL role.",
                    "Prefer explicit local host settings in training.",
                ],
                "examples": [
                    {
                        "label": "Config file values",
                        "code": "db_host = 127.0.0.1\ndb_user = odoo17\ndb_password = change-me",
                    },
                    {
                        "label": "CLI values",
                        "code": "./odoo-bin --db_host=127.0.0.1 --db_user=odoo17 --db_password=change-me",
                    },
                ],
            }
        ],
    },
    {
        "section": 5,
        "title": "addons_path",
        "topics": [
            {
                "id": "ODOO-05",
                "title": "Configure addons_path",
                "points": [
                    "addons_path tells Odoo where modules live.",
                    "Separate core and custom addons clearly.",
                    "Path order matters when names collide.",
                ],
                "examples": [
                    {
                        "label": "Config addons path",
                        "code": "addons_path = /opt/odoo/odoo17/addons,/opt/odoo/custom-addons",
                    },
                    {
                        "label": "CLI addons path",
                        "code": "./odoo-bin --addons-path=addons,../custom-addons -d training",
                    },
                ],
            }
        ],
    },
    {
        "section": 6,
        "title": "Log File",
        "topics": [
            {
                "id": "ODOO-06",
                "title": "Write Logs to a File",
                "points": [
                    "Logs show startup and runtime problems.",
                    "A logfile is easier to inspect later.",
                    "Keep permissions simple for the Odoo user.",
                ],
                "examples": [
                    {
                        "label": "Config logfile",
                        "code": "logfile = /var/log/odoo/odoo17.log",
                    },
                    {
                        "label": "View recent logs",
                        "code": "less /var/log/odoo/odoo17.log",
                    },
                ],
            }
        ],
    },
    {
        "section": 7,
        "title": "list_db False",
        "topics": [
            {
                "id": "ODOO-07",
                "title": "Hide the Database List",
                "points": [
                    "list_db controls the web database selector.",
                    "Set it false on shared or public servers.",
                    "It does not replace real access control.",
                ],
                "examples": [
                    {
                        "label": "Disable listing",
                        "code": "list_db = False",
                    },
                    {
                        "label": "Start with one database",
                        "code": "./odoo-bin -c odoo17.conf -d odoo17_prod",
                    },
                ],
            }
        ],
    },
    {
        "section": 8,
        "title": "Master Password",
        "topics": [
            {
                "id": "ODOO-08",
                "title": "Understand the Master Password",
                "points": [
                    "The master password protects database manager actions.",
                    "Use a strong value outside source control.",
                    "Do not confuse it with user passwords.",
                ],
                "examples": [
                    {
                        "label": "Config setting",
                        "code": "admin_passwd = replace-with-a-strong-secret",
                    },
                    {
                        "label": "Database manager use",
                        "code": "Open /web/database/manager\nEnter the master password for backup or restore actions",
                    },
                ],
            }
        ],
    },
    {
        "section": 9,
        "title": "Install Module with -i",
        "topics": [
            {
                "id": "ODOO-09",
                "title": "Install a Module with -i",
                "points": [
                    "-i installs a module into a database.",
                    "Use it when the module is not installed yet.",
                    "Combine with stop-after-init for scripts.",
                ],
                "examples": [
                    {
                        "label": "Install base CRM",
                        "code": "./odoo-bin -d training -i crm --stop-after-init",
                    },
                    {
                        "label": "Install custom module",
                        "code": "./odoo-bin -c odoo17.conf -d training -i estate --stop-after-init",
                    },
                ],
            }
        ],
    },
    {
        "section": 10,
        "title": "Upgrade Module with -u",
        "topics": [
            {
                "id": "ODOO-10",
                "title": "Upgrade a Module with -u",
                "points": [
                    "-u updates an installed module.",
                    "Use it after changing models, views, or data.",
                    "Back up important databases first.",
                ],
                "examples": [
                    {
                        "label": "Upgrade one module",
                        "code": "./odoo-bin -d training -u estate --stop-after-init",
                    },
                    {
                        "label": "Upgrade several modules",
                        "code": "./odoo-bin -c odoo17.conf -d training -u estate,sale --stop-after-init",
                    },
                ],
            }
        ],
    },
    {
        "section": 11,
        "title": "Open Odoo Shell",
        "topics": [
            {
                "id": "ODOO-11",
                "title": "Use shell -d",
                "points": [
                    "The Odoo shell opens an ORM-aware Python prompt.",
                    "Use -d to choose the database.",
                    "It is useful for safe inspection and small fixes.",
                ],
                "examples": [
                    {
                        "label": "Open shell",
                        "code": "./odoo-bin shell -d training",
                    },
                    {
                        "label": "Inspect a model",
                        "code": "env['res.partner'].search([], limit=3)",
                    },
                ],
            }
        ],
    },
    {
        "section": 12,
        "title": "Scaffold Module",
        "topics": [
            {
                "id": "ODOO-12",
                "title": "Scaffold a New Module",
                "points": [
                    "Scaffold creates a starter module folder.",
                    "It gives common files and directories.",
                    "Review generated files before editing.",
                ],
                "examples": [
                    {
                        "label": "Create module skeleton",
                        "code": "./odoo-bin scaffold estate ../custom-addons",
                    },
                    {
                        "label": "Generated path",
                        "code": "../custom-addons/estate/__manifest__.py\n../custom-addons/estate/models/models.py",
                    },
                ],
            }
        ],
    },
    {
        "section": 13,
        "title": "Manifest Basics",
        "topics": [
            {
                "id": "ODOO-13",
                "title": "Set Manifest name, version, and depends",
                "points": [
                    "The manifest describes the module.",
                    "depends controls module load order.",
                    "Keep the version meaningful for releases.",
                ],
                "examples": [
                    {
                        "label": "Basic manifest",
                        "code": "{\n    'name': 'Estate',\n    'version': '17.0.1.0.0',\n    'depends': ['base'],\n}",
                    },
                    {
                        "label": "Depend on sales",
                        "code": "{\n    'name': 'Estate Sale',\n    'depends': ['estate', 'sale'],\n}",
                    },
                ],
            }
        ],
    },
    {
        "section": 14,
        "title": "Module Folder Structure",
        "topics": [
            {
                "id": "ODOO-14",
                "title": "Recognize Module Folder Structure",
                "points": [
                    "Python models usually live in models.",
                    "XML views usually live in views.",
                    "Security files usually live in security.",
                ],
                "examples": [
                    {
                        "label": "Common folders",
                        "code": "estate/\n  __manifest__.py\n  models/\n  views/\n  security/",
                    },
                    {
                        "label": "Import models",
                        "code": "# estate/models/__init__.py\nfrom . import estate_property",
                    },
                ],
            }
        ],
    },
    {
        "section": 15,
        "title": "Model _name",
        "topics": [
            {
                "id": "ODOO-15",
                "title": "Define a Model with _name",
                "points": [
                    "_name gives the model its technical name.",
                    "Use dotted names such as estate.property.",
                    "The name is used by views, access rules, and code.",
                ],
                "examples": [
                    {
                        "label": "New model",
                        "code": "class EstateProperty(models.Model):\n    _name = 'estate.property'",
                    },
                    {
                        "label": "Use model name",
                        "code": "self.env['estate.property'].search([])",
                    },
                ],
            }
        ],
    },
    {
        "section": 16,
        "title": "Model _description",
        "topics": [
            {
                "id": "ODOO-16",
                "title": "Add a Model _description",
                "points": [
                    "_description gives a readable model label.",
                    "It helps logs and technical screens.",
                    "Keep it short and human friendly.",
                ],
                "examples": [
                    {
                        "label": "Description line",
                        "code": "class EstateProperty(models.Model):\n    _name = 'estate.property'\n    _description = 'Estate Property'",
                    },
                    {
                        "label": "Another description",
                        "code": "class EstateOffer(models.Model):\n    _name = 'estate.offer'\n    _description = 'Estate Offer'",
                    },
                ],
            }
        ],
    },
    {
        "section": 17,
        "title": "Char Field",
        "topics": [
            {
                "id": "ODOO-17",
                "title": "Use a Char Field",
                "points": [
                    "Char stores short text.",
                    "Use it for names, codes, and labels.",
                    "Add required=True when the value must exist.",
                ],
                "examples": [
                    {
                        "label": "Name field",
                        "code": "name = fields.Char(string='Name', required=True)",
                    },
                    {
                        "label": "Reference field",
                        "code": "reference = fields.Char(string='Reference', copy=False)",
                    },
                ],
            }
        ],
    },
    {
        "section": 18,
        "title": "Text Field",
        "topics": [
            {
                "id": "ODOO-18",
                "title": "Use a Text Field",
                "points": [
                    "Text stores longer text.",
                    "Use it for notes and descriptions.",
                    "It is not limited like short labels.",
                ],
                "examples": [
                    {
                        "label": "Description field",
                        "code": "description = fields.Text(string='Description')",
                    },
                    {
                        "label": "Internal notes",
                        "code": "note = fields.Text(string='Internal Notes')",
                    },
                ],
            }
        ],
    },
    {
        "section": 19,
        "title": "Boolean Field",
        "topics": [
            {
                "id": "ODOO-19",
                "title": "Use a Boolean Field",
                "points": [
                    "Boolean stores true or false.",
                    "Use it for flags and toggles.",
                    "Set a default when useful.",
                ],
                "examples": [
                    {
                        "label": "Active flag",
                        "code": "is_published = fields.Boolean(string='Published')",
                    },
                    {
                        "label": "Default true",
                        "code": "active = fields.Boolean(default=True)",
                    },
                ],
            }
        ],
    },
    {
        "section": 20,
        "title": "Selection Field",
        "topics": [
            {
                "id": "ODOO-20",
                "title": "Use a Selection Field",
                "points": [
                    "Selection stores one value from a fixed list.",
                    "Each option has a key and label.",
                    "Use it for simple states or categories.",
                ],
                "examples": [
                    {
                        "label": "State field",
                        "code": "state = fields.Selection([\n    ('new', 'New'),\n    ('done', 'Done'),\n], default='new')",
                    },
                    {
                        "label": "Priority field",
                        "code": "priority = fields.Selection([\n    ('0', 'Normal'),\n    ('1', 'High'),\n])",
                    },
                ],
            }
        ],
    },
    {
        "section": 21,
        "title": "Integer Field",
        "topics": [
            {
                "id": "ODOO-21",
                "title": "Use an Integer Field",
                "points": [
                    "Integer stores whole numbers.",
                    "Use it for counts and quantities.",
                    "It defaults to zero when empty.",
                ],
                "examples": [
                    {
                        "label": "Quantity field",
                        "code": "quantity = fields.Integer(string='Quantity')",
                    },
                    {
                        "label": "Bedrooms field",
                        "code": "bedrooms = fields.Integer(default=2)",
                    },
                ],
            }
        ],
    },
    {
        "section": 22,
        "title": "Float Field",
        "topics": [
            {
                "id": "ODOO-22",
                "title": "Use a Float Field",
                "points": [
                    "Float stores decimal numbers.",
                    "Use it for measurements and rates.",
                    "Use monetary fields for accounting amounts.",
                ],
                "examples": [
                    {
                        "label": "Area field",
                        "code": "living_area = fields.Float(string='Living Area')",
                    },
                    {
                        "label": "Percentage field",
                        "code": "commission_rate = fields.Float(string='Commission Rate')",
                    },
                ],
            }
        ],
    },
    {
        "section": 23,
        "title": "Date Field",
        "topics": [
            {
                "id": "ODOO-23",
                "title": "Use a Date Field",
                "points": [
                    "Date stores a calendar day.",
                    "Use it when time of day is not needed.",
                    "Odoo has helpers for today.",
                ],
                "examples": [
                    {
                        "label": "Simple date",
                        "code": "available_date = fields.Date(string='Available From')",
                    },
                    {
                        "label": "Default today",
                        "code": "date_order = fields.Date(default=fields.Date.today)",
                    },
                ],
            }
        ],
    },
    {
        "section": 24,
        "title": "Datetime Field",
        "topics": [
            {
                "id": "ODOO-24",
                "title": "Use a Datetime Field",
                "points": [
                    "Datetime stores date and time.",
                    "Use it for events and timestamps.",
                    "Odoo handles display with user timezone.",
                ],
                "examples": [
                    {
                        "label": "Meeting time",
                        "code": "meeting_at = fields.Datetime(string='Meeting Time')",
                    },
                    {
                        "label": "Default now",
                        "code": "created_marker = fields.Datetime(default=fields.Datetime.now)",
                    },
                ],
            }
        ],
    },
    {
        "section": 25,
        "title": "Many2one Field",
        "topics": [
            {
                "id": "ODOO-25",
                "title": "Use a Many2one Field",
                "points": [
                    "Many2one links this record to one other record.",
                    "It creates a database foreign key.",
                    "Use it for owner, partner, and category links.",
                ],
                "examples": [
                    {
                        "label": "Partner link",
                        "code": "partner_id = fields.Many2one('res.partner', string='Customer')",
                    },
                    {
                        "label": "Required salesperson",
                        "code": "user_id = fields.Many2one('res.users', required=True)",
                    },
                ],
            }
        ],
    },
    {
        "section": 26,
        "title": "One2many Field",
        "topics": [
            {
                "id": "ODOO-26",
                "title": "Use a One2many Field",
                "points": [
                    "One2many shows records pointing back to this record.",
                    "It needs the child model and inverse field.",
                    "It is commonly used for line items.",
                ],
                "examples": [
                    {
                        "label": "Order lines",
                        "code": "line_ids = fields.One2many('sale.order.line', 'order_id')",
                    },
                    {
                        "label": "Estate offers",
                        "code": "offer_ids = fields.One2many('estate.offer', 'property_id')",
                    },
                ],
            }
        ],
    },
    {
        "section": 27,
        "title": "Many2many Field",
        "topics": [
            {
                "id": "ODOO-27",
                "title": "Use a Many2many Field",
                "points": [
                    "Many2many links many records on both sides.",
                    "Odoo stores links in a relation table.",
                    "Use it for tags, followers, and allowed users.",
                ],
                "examples": [
                    {
                        "label": "Tag field",
                        "code": "tag_ids = fields.Many2many('estate.property.tag', string='Tags')",
                    },
                    {
                        "label": "Allowed users",
                        "code": "allowed_user_ids = fields.Many2many('res.users')",
                    },
                ],
            }
        ],
    },
    {
        "section": 28,
        "title": "Compute Field",
        "topics": [
            {
                "id": "ODOO-28",
                "title": "Create a Compute Field",
                "points": [
                    "A compute field gets its value from a method.",
                    "Use depends to declare trigger fields.",
                    "Store only when search or performance needs it.",
                ],
                "examples": [
                    {
                        "label": "Compute total",
                        "code": "total_area = fields.Float(compute='_compute_total_area')\n\n@api.depends('living_area', 'garden_area')\ndef _compute_total_area(self):\n    for record in self:\n        record.total_area = record.living_area + record.garden_area",
                    },
                    {
                        "label": "Stored compute",
                        "code": "best_price = fields.Float(compute='_compute_best_price', store=True)",
                    },
                ],
            }
        ],
    },
    {
        "section": 29,
        "title": "Related Field",
        "topics": [
            {
                "id": "ODOO-29",
                "title": "Create a Related Field",
                "points": [
                    "A related field follows a relationship path.",
                    "It avoids duplicating simple values.",
                    "Use store=True when filtering often.",
                ],
                "examples": [
                    {
                        "label": "Partner email",
                        "code": "partner_email = fields.Char(related='partner_id.email')",
                    },
                    {
                        "label": "Stored company",
                        "code": "company_id = fields.Many2one(related='user_id.company_id', store=True)",
                    },
                ],
            }
        ],
    },
    {
        "section": 30,
        "title": "Create Override",
        "topics": [
            {
                "id": "ODOO-30",
                "title": "Understand the create Override Idea",
                "points": [
                    "create runs when new records are made.",
                    "Call super to keep standard behavior.",
                    "Use it for validation or default adjustments.",
                ],
                "examples": [
                    {
                        "label": "Basic create override",
                        "code": "@api.model_create_multi\ndef create(self, vals_list):\n    records = super().create(vals_list)\n    return records",
                    },
                    {
                        "label": "Fill a missing value",
                        "code": "for vals in vals_list:\n    vals.setdefault('state', 'new')",
                    },
                ],
            }
        ],
    },
    {
        "section": 31,
        "title": "Write Override",
        "topics": [
            {
                "id": "ODOO-31",
                "title": "Understand the write Override Idea",
                "points": [
                    "write runs when existing records change.",
                    "Call super once for the normal update.",
                    "Be careful with recursion and side effects.",
                ],
                "examples": [
                    {
                        "label": "Basic write override",
                        "code": "def write(self, vals):\n    result = super().write(vals)\n    return result",
                    },
                    {
                        "label": "React to field change",
                        "code": "if 'state' in vals:\n    self.message_post(body='State changed')",
                    },
                ],
            }
        ],
    },
    {
        "section": 32,
        "title": "Unlink Idea",
        "topics": [
            {
                "id": "ODOO-32",
                "title": "Understand the unlink Idea",
                "points": [
                    "unlink runs when records are deleted.",
                    "Use it to block unsafe deletion.",
                    "Archive records when deletion is not appropriate.",
                ],
                "examples": [
                    {
                        "label": "Basic unlink override",
                        "code": "def unlink(self):\n    return super().unlink()",
                    },
                    {
                        "label": "Block deletion",
                        "code": "if any(record.state == 'done' for record in self):\n    raise UserError('Done records cannot be deleted.')",
                    },
                ],
            }
        ],
    },
    {
        "section": 33,
        "title": "search()",
        "topics": [
            {
                "id": "ODOO-33",
                "title": "Find Records with search()",
                "points": [
                    "search returns a recordset.",
                    "Pass a domain to filter records.",
                    "Use limit for small inspections.",
                ],
                "examples": [
                    {
                        "label": "Find customers",
                        "code": "customers = self.env['res.partner'].search([('customer_rank', '>', 0)])",
                    },
                    {
                        "label": "Find one record",
                        "code": "partner = self.env['res.partner'].search([('email', '=', email)], limit=1)",
                    },
                ],
            }
        ],
    },
    {
        "section": 34,
        "title": "Domain Syntax",
        "topics": [
            {
                "id": "ODOO-34",
                "title": "Build a domain = Filter",
                "points": [
                    "A domain is a list of filter conditions.",
                    "Each condition is field, operator, value.",
                    "Domains are used by search, views, and rules.",
                ],
                "examples": [
                    {
                        "label": "Simple domain",
                        "code": "domain = [('state', '=', 'sale')]",
                    },
                    {
                        "label": "Multiple conditions",
                        "code": "domain = [('amount_total', '>=', 1000), ('partner_id', '!=', False)]",
                    },
                ],
            }
        ],
    },
    {
        "section": 35,
        "title": "search_count",
        "topics": [
            {
                "id": "ODOO-35",
                "title": "Count Records with search_count",
                "points": [
                    "search_count returns an integer.",
                    "It is faster than loading records just to count.",
                    "Use the same domain style as search.",
                ],
                "examples": [
                    {
                        "label": "Count customers",
                        "code": "count = self.env['res.partner'].search_count([('customer_rank', '>', 0)])",
                    },
                    {
                        "label": "Count open tasks",
                        "code": "open_tasks = self.env['project.task'].search_count([('stage_id.fold', '=', False)])",
                    },
                ],
            }
        ],
    },
    {
        "section": 36,
        "title": "browse and exists",
        "topics": [
            {
                "id": "ODOO-36",
                "title": "Use browse() and exists()",
                "points": [
                    "browse creates a recordset from ids.",
                    "It does not guarantee records exist.",
                    "exists removes missing records from the set.",
                ],
                "examples": [
                    {
                        "label": "Browse by id",
                        "code": "partner = self.env['res.partner'].browse(42)",
                    },
                    {
                        "label": "Check existence",
                        "code": "partner = self.env['res.partner'].browse(42).exists()",
                    },
                ],
            }
        ],
    },
    {
        "section": 37,
        "title": "ensure_one",
        "topics": [
            {
                "id": "ODOO-37",
                "title": "Use ensure_one",
                "points": [
                    "ensure_one confirms the recordset has one record.",
                    "It raises an error for zero or many records.",
                    "Use it in methods designed for one record.",
                ],
                "examples": [
                    {
                        "label": "Single-record method",
                        "code": "def action_confirm(self):\n    self.ensure_one()\n    self.state = 'confirmed'",
                    },
                    {
                        "label": "Read one value",
                        "code": "self.ensure_one()\nreturn self.name",
                    },
                ],
            }
        ],
    },
    {
        "section": 38,
        "title": "mapped",
        "topics": [
            {
                "id": "ODOO-38",
                "title": "Use mapped",
                "points": [
                    "mapped extracts a field from each record.",
                    "It can follow relational paths.",
                    "It keeps recordset code compact.",
                ],
                "examples": [
                    {
                        "label": "Names list",
                        "code": "names = partners.mapped('name')",
                    },
                    {
                        "label": "Related records",
                        "code": "companies = partners.mapped('company_id')",
                    },
                ],
            }
        ],
    },
    {
        "section": 39,
        "title": "filtered",
        "topics": [
            {
                "id": "ODOO-39",
                "title": "Use filtered",
                "points": [
                    "filtered keeps records matching Python logic.",
                    "Use search domains when the database can filter.",
                    "Use filtered for already-loaded recordsets.",
                ],
                "examples": [
                    {
                        "label": "Keep active records",
                        "code": "active_partners = partners.filtered(lambda p: p.active)",
                    },
                    {
                        "label": "Keep high value orders",
                        "code": "large_orders = orders.filtered(lambda o: o.amount_total > 1000)",
                    },
                ],
            }
        ],
    },
    {
        "section": 40,
        "title": "Active and Archive",
        "topics": [
            {
                "id": "ODOO-40",
                "title": "Use active for Archive Behavior",
                "points": [
                    "The active field controls archive behavior.",
                    "Archived records are hidden from normal searches.",
                    "Archiving is safer than deleting business records.",
                ],
                "examples": [
                    {
                        "label": "Add active field",
                        "code": "active = fields.Boolean(default=True)",
                    },
                    {
                        "label": "Archive records",
                        "code": "records.action_archive()\nrecords.action_unarchive()",
                    },
                ],
            }
        ],
    },
    {
        "section": 41,
        "title": "env.user",
        "topics": [
            {
                "id": "ODOO-41",
                "title": "Read the Current User with env.user",
                "points": [
                    "env.user is the current Odoo user.",
                    "Use it for defaults and simple checks.",
                    "Respect access rules when reading user data.",
                ],
                "examples": [
                    {
                        "label": "Default salesperson",
                        "code": "user_id = fields.Many2one('res.users', default=lambda self: self.env.user)",
                    },
                    {
                        "label": "Check groups",
                        "code": "if self.env.user.has_group('sales_team.group_sale_manager'):\n    return True",
                    },
                ],
            }
        ],
    },
    {
        "section": 42,
        "title": "sudo Caution",
        "topics": [
            {
                "id": "ODOO-42",
                "title": "Use sudo with Caution",
                "points": [
                    "sudo bypasses normal access checks.",
                    "Use it only when the business case is clear.",
                    "Avoid exposing sudo data to the wrong user.",
                ],
                "examples": [
                    {
                        "label": "Controlled sudo read",
                        "code": "company = self.env['res.company'].sudo().browse(company_id)",
                    },
                    {
                        "label": "Prefer normal access",
                        "code": "partners = self.env['res.partner'].search(domain)",
                    },
                ],
            }
        ],
    },
    {
        "section": 43,
        "title": "Command 0",
        "topics": [
            {
                "id": "ODOO-43",
                "title": "Create Related Record with [0, 0, vals]",
                "points": [
                    "[0, 0, vals] creates a new related record.",
                    "Use it in One2many or Many2many updates.",
                    "vals contains the new record values.",
                ],
                "examples": [
                    {
                        "label": "Create order line",
                        "code": "order.write({'order_line': [(0, 0, {'name': 'Service', 'price_unit': 100})]})",
                    },
                    {
                        "label": "Create tag",
                        "code": "record.write({'tag_ids': [(0, 0, {'name': 'New Tag'})]})",
                    },
                ],
            }
        ],
    },
    {
        "section": 44,
        "title": "Command 1",
        "topics": [
            {
                "id": "ODOO-44",
                "title": "Update Related Record with [1, id, vals]",
                "points": [
                    "[1, id, vals] updates an existing related record.",
                    "The id is the related record id.",
                    "Use vals for fields to change.",
                ],
                "examples": [
                    {
                        "label": "Update line price",
                        "code": "order.write({'order_line': [(1, line_id, {'price_unit': 120})]})",
                    },
                    {
                        "label": "Update tag name",
                        "code": "record.write({'tag_ids': [(1, tag_id, {'name': 'Updated'})]})",
                    },
                ],
            }
        ],
    },
    {
        "section": 45,
        "title": "Command 2",
        "topics": [
            {
                "id": "ODOO-45",
                "title": "Delete Related Record with [2, id]",
                "points": [
                    "[2, id] removes and deletes the related record.",
                    "Use it carefully with business data.",
                    "It is different from only unlinking a relation.",
                ],
                "examples": [
                    {
                        "label": "Delete order line",
                        "code": "order.write({'order_line': [(2, line_id)]})",
                    },
                    {
                        "label": "Delete related tag",
                        "code": "record.write({'tag_ids': [(2, tag_id)]})",
                    },
                ],
            }
        ],
    },
    {
        "section": 46,
        "title": "Command 4",
        "topics": [
            {
                "id": "ODOO-46",
                "title": "Link Existing Record with [4, id]",
                "points": [
                    "[4, id] links an existing record.",
                    "It does not create or delete the linked record.",
                    "It is common for Many2many fields.",
                ],
                "examples": [
                    {
                        "label": "Add existing tag",
                        "code": "record.write({'tag_ids': [(4, tag_id)]})",
                    },
                    {
                        "label": "Add existing follower group",
                        "code": "record.write({'allowed_group_ids': [(4, group_id)]})",
                    },
                ],
            }
        ],
    },
    {
        "section": 47,
        "title": "Command 6",
        "topics": [
            {
                "id": "ODOO-47",
                "title": "Replace Links with [6, 0, ids]",
                "points": [
                    "[6, 0, ids] replaces all current links.",
                    "ids is the full final list.",
                    "Use it when syncing a complete selection.",
                ],
                "examples": [
                    {
                        "label": "Replace tags",
                        "code": "record.write({'tag_ids': [(6, 0, [1, 2, 3])]})",
                    },
                    {
                        "label": "Use ids from records",
                        "code": "record.write({'user_ids': [(6, 0, users.ids)]})",
                    },
                ],
            }
        ],
    },
    {
        "section": 48,
        "title": "XML Data Record",
        "topics": [
            {
                "id": "ODOO-48",
                "title": "Create an XML Data Record",
                "points": [
                    "XML data creates or updates records during module load.",
                    "The id becomes an external identifier.",
                    "Keep data files listed in the manifest.",
                ],
                "examples": [
                    {
                        "label": "Simple XML record",
                        "code": "<record id=\"estate_tag_garden\" model=\"estate.property.tag\">\n    <field name=\"name\">Garden</field>\n</record>",
                    },
                    {
                        "label": "Manifest data entry",
                        "code": "'data': [\n    'views/estate_property_views.xml',\n    'data/estate_tags.xml',\n]",
                    },
                ],
            }
        ],
    },
    {
        "section": 49,
        "title": "CSV Access Rights",
        "topics": [
            {
                "id": "ODOO-49",
                "title": "Introduce CSV Access Rights",
                "points": [
                    "ir.model.access.csv grants model permissions.",
                    "Access rights cover read, write, create, and delete.",
                    "Every new model usually needs an access line.",
                ],
                "examples": [
                    {
                        "label": "CSV header",
                        "code": "id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink",
                    },
                    {
                        "label": "Basic access row",
                        "code": "access_estate_property_user,estate.property.user,model_estate_property,base.group_user,1,1,1,0",
                    },
                ],
            }
        ],
    },
]

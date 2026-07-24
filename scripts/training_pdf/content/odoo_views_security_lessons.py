#!/usr/bin/env python3
"""Views, security, and data lessons for the Odoo training PDF generator."""


def _explanation(title, theme, design, implementation, verification, production):
    return [
        (
            f"{title} is best understood as part of the contract between the ORM, the "
            f"web client, and the business user. {theme} A senior Odoo developer reads "
            "a view or security file as executable configuration: it changes what users "
            "can see, which records they can touch, and which operations become safe or "
            "dangerous in production."
        ),
        (
            f"The design decision starts before writing XML. {design} Good modules keep "
            "layout, data defaults, and authorization close to the business process they "
            "serve, while avoiding clever view code that hides a weak model design."
        ),
        (
            f"Implementation should be small, explicit, and easy to inherit. {implementation} "
            "Prefer stable external ids, clear XPath anchors, model fields with meaningful "
            "states, and security definitions that can be reviewed by a functional lead."
        ),
        (
            f"Verification is not only clicking the happy path as an administrator. {verification} "
            "Test with at least two real security profiles, reload the module from a clean "
            "database, and check that exported or imported data behaves the same way as "
            "data created through the UI."
        ),
        (
            f"In production, the cost of a poor {title.lower()} decision appears during "
            f"upgrades, audits, and support tickets. {production} Keep the XML boring, "
            "make domains readable, document unusual choices in field help or comments, "
            "and treat permissions as part of the release checklist."
        ),
    ]


def _lesson(
    ident,
    title,
    objectives,
    theme,
    design,
    implementation,
    verification,
    production,
    key_points,
    examples,
    common_mistakes,
    lab,
    slide_extras=None,
):
    lesson = {
        "section": "odoo_views",
        "id": ident,
        "title": title,
        "objectives": objectives,
        "explanation": _explanation(title, theme, design, implementation, verification, production),
        "key_points": key_points,
        "examples": examples,
        "common_mistakes": common_mistakes,
        "lab": lab,
    }
    if slide_extras:
        lesson["slide_extras"] = slide_extras
    return lesson


LESSONS = [
    _lesson(
        "VS01",
        "Intro to Odoo Views and XML Data Loading",
        [
            "Explain how view records are stored and loaded.",
            "Choose reliable external ids for view and data records.",
            "Describe the relationship between model fields and UI architecture.",
        ],
        "Odoo views are not templates copied into the browser; they are records in ir.ui.view that the server combines, validates, and sends to the web client.",
        "Start from the model and workflow, then select the smallest view types needed to support the workflow instead of creating every possible view.",
        "Declare XML under a data file, reference existing models through ref, and keep view ids stable because other modules and upgrades depend on them.",
        "Install with demo data disabled and enabled, update the module, and confirm the view exists in developer mode with the expected inherited architecture.",
        "A predictable data-loading strategy makes migrations easier because broken XML ids and duplicated records are among the most common deployment failures.",
        [
            "A view is an ir.ui.view record with arch XML.",
            "External ids are part of the module API.",
            "Data files load in manifest order.",
            "Views should represent workflows, not database tables only.",
            "Developer mode is essential for inspecting final architecture.",
        ],
        [
            {
                "title": "Minimal window action and menu",
                "code": '''<odoo>
    <record id="training_course_action" model="ir.actions.act_window">
        <field name="name">Courses</field>
        <field name="res_model">training.course</field>
        <field name="view_mode">tree,form,kanban</field>
        <field name="context">{'search_default_active': 1}</field>
    </record>

    <menuitem id="training_menu_root" name="Training"/>
    <menuitem id="training_menu_courses"
              name="Courses"
              parent="training_menu_root"
              action="training_course_action"/>
</odoo>''',
                "explain": "The action defines the model and ordered view modes; the menu only points users to that action.",
            }
        ],
        [
            "Changing external ids after another module inherits them.",
            "Loading views before the model fields exist.",
            "Putting business rules only in XML instead of model methods.",
            "Forgetting that manifest data file order is significant.",
        ],
        "Create a model action, menu, tree view, and form view for a small training.course model, then update the module twice to verify idempotency.",
        [
            {
                "kind": "table",
                "title": "View loading checkpoints",
                "headers": ["Checkpoint", "Reason"],
                "rows": [
                    ["External id", "Needed for inheritance and upgrades"],
                    ["Manifest order", "Dependencies must load first"],
                    ["Developer mode", "Shows combined architecture"],
                ],
            }
        ],
    ),
    _lesson(
        "VS02",
        "List Views, Sorting, and Limits",
        [
            "Build a readable list view for operational records.",
            "Use default_order and limit intentionally.",
            "Select list columns that support the primary user decision.",
        ],
        "The list view is usually the first screen where users scan volume, compare records, and decide what needs attention.",
        "Choose columns by asking what a user must know before opening a form; do not mirror every field in the model.",
        "Use default_order on indexed or naturally sortable fields and reserve limit for dashboards or queues where a short list is part of the design.",
        "Check list load time with realistic data, confirm sorting is stable, and verify that invisible technical fields are still available when used by decorations or buttons.",
        "Poor list views create hidden operational cost because every extra column can increase read payloads and every confusing order creates manual work.",
        [
            "Tree views are now commonly referred to as list views in newer Odoo discussions.",
            "default_order belongs on the view arch.",
            "limit changes the initial row count for that view.",
            "Columns should reflect the user decision.",
            "Decorations and modifiers may require invisible helper fields.",
        ],
        [
            {
                "title": "Operational list with stable ordering",
                "code": '''<record id="training_course_view_tree" model="ir.ui.view">
    <field name="name">training.course.tree</field>
    <field name="model">training.course</field>
    <field name="arch" type="xml">
        <tree string="Courses" default_order="start_date desc, name" limit="80">
            <field name="name"/>
            <field name="teacher_id"/>
            <field name="start_date"/>
            <field name="seat_count"/>
            <field name="state"/>
        </tree>
    </field>
</record>''',
                "explain": "The list opens with recent courses first and only includes fields needed to triage the course catalog.",
            }
        ],
        [
            "Using a non-indexed computed field as the default sort on a large table.",
            "Adding every field because it is available.",
            "Using limit to hide bad performance rather than fixing the cause.",
            "Forgetting multi-company or active filters when reviewing list content.",
        ],
        "Replace a wide list view with a decision-focused list, add default_order, and compare the generated read fields in the browser network tab.",
    ),
    _lesson(
        "VS03",
        "Editable Lists, Mass Editing, and the Handle Widget",
        [
            "Enable safe inline edits for simple records.",
            "Understand when mass editing is appropriate.",
            "Use handle widgets for sequence-based ordering.",
        ],
        "Editable lists reduce navigation when users are maintaining line-like records, but they also reduce the friction that normally makes users review a form.",
        "Only make fields editable when validation is local and obvious; complex onchange chains, attachments, chatter, or approvals usually deserve a form.",
        "Use editable='bottom' for controlled creation, multi_edit='1' for deliberate mass changes, and widget='handle' with an integer sequence field for manual ordering.",
        "Test create, edit, discard, required fields, access rights, and record rules with a non-admin user because inline editing exposes write paths quickly.",
        "A safe editable list feels fast without bypassing business rules because constraints, onchange logic, and access rights still execute server-side.",
        [
            "Inline editing is a workflow choice, not a default.",
            "multi_edit applies one value to many selected rows.",
            "The handle widget requires an orderable sequence field.",
            "Server constraints remain mandatory.",
            "Editable lists are risky on approval records.",
        ],
        [
            {
                "title": "Editable line list with sequence handle",
                "code": '''<tree editable="bottom" multi_edit="1" default_order="sequence, id">
    <field name="sequence" widget="handle"/>
    <field name="name" required="1"/>
    <field name="duration_hours"/>
    <field name="price"/>
</tree>''',
                "explain": "Users can reorder and maintain simple training lines without opening each form, while required fields remain enforced.",
            }
        ],
        [
            "Enabling editable lists on records with complex workflow transitions.",
            "Forgetting to include sequence in _order on the model.",
            "Assuming mass edit bypasses access rights.",
            "Relying on onchange instead of constraints for critical validation.",
        ],
        "Add an editable list to course session lines, include a handle sequence, and prove that a negative duration is blocked by a Python constraint.",
    ),
    _lesson(
        "VS04",
        "List Decorations, Field Decorations, Widths, and Hidden Labels",
        [
            "Apply visual decorations without changing data semantics.",
            "Use invisible fields as decoration inputs.",
            "Tune field width and labels for dense operational screens.",
        ],
        "Decorations are a fast way to turn a list into an exception queue, but they should reinforce a business meaning already present in the data.",
        "Design the visual language first: one color for danger, one for success, and a small number of badges so users do not learn to ignore noise.",
        "Use row decoration attributes, field-level decorations, optional fields, width hints, and nolabel where they clarify the screen without hiding important data.",
        "Review decorations with sample records in every state and confirm helper fields are present in the view when expressions need them.",
        "Visual rules age badly when they are undocumented, so connect decoration expressions to stable state values rather than fragile names or dates embedded in text.",
        [
            "Row decorations use expressions evaluated by the client.",
            "Field decorations work well on status or KPI fields.",
            "Invisible helper fields can feed modifiers and decorations.",
            "Width hints are guidance, not a security feature.",
            "Do not encode business rules only as colors.",
        ],
        [
            {
                "title": "Exception-oriented decorated list",
                "code": '''<tree decoration-danger="state == 'cancel'"
      decoration-warning="seat_count &lt; minimum_seats"
      decoration-success="state == 'done'">
    <field name="name" width="240px"/>
    <field name="minimum_seats" invisible="1"/>
    <field name="seat_count" decoration-warning="seat_count &lt; minimum_seats"/>
    <field name="state" widget="badge"/>
</tree>''',
                "explain": "The list highlights cancellation, under-filled courses, and completion while keeping the comparison field available invisibly.",
            }
        ],
        [
            "Using many colors for unrelated meanings.",
            "Forgetting XML escaping for comparison operators.",
            "Treating invisible fields as secure.",
            "Making labels disappear when the field meaning is not obvious.",
        ],
        "Create three sample records that trigger danger, warning, and success decorations, then ask another user to explain the meaning without reading the XML.",
    ),
    _lesson(
        "VS05",
        "List Totals, Averages, and Grouped Lists",
        [
            "Use sum and avg footers on numeric fields.",
            "Understand how grouped list aggregations help operations.",
            "Avoid misleading totals on filtered data.",
        ],
        "Totals and averages make a list view useful for reconciliation, capacity planning, and quick financial checks.",
        "Decide whether a metric should be summed, averaged, counted, or left out; not every numeric field communicates meaningful aggregate information.",
        "Add sum and avg labels directly on fields, combine with groupby where appropriate, and ensure computed fields are stored if aggregation must happen in SQL.",
        "Validate totals under filters, groups, multi-company access, and currency contexts so users know exactly what population is being summarized.",
        "Production incidents often happen when users export or approve based on a subtotal they misunderstood, so the label should name the business measure precisely.",
        [
            "sum and avg attributes create list footers.",
            "Grouped lists aggregate per group and overall.",
            "Stored fields are safer for SQL aggregation.",
            "Currency and unit of measure context matters.",
            "Totals reflect the current domain and access rules.",
        ],
        [
            {
                "title": "Capacity and revenue footers",
                "code": '''<tree default_order="start_date desc">
    <field name="name"/>
    <field name="teacher_id"/>
    <field name="seat_count" sum="Total Seats"/>
    <field name="price_total" sum="Total Revenue"/>
    <field name="satisfaction_score" avg="Average Score"/>
</tree>''',
                "explain": "The footer gives immediate operational totals without requiring an export to a spreadsheet.",
            }
        ],
        [
            "Summing percentages or scores that should be averaged.",
            "Aggregating non-stored computed fields that cannot be grouped efficiently.",
            "Ignoring currency mixing across companies.",
            "Letting totals imply a complete population when filters are active.",
        ],
        "Add sum and average footers to a list, group by teacher, and compare grouped totals against a manual read_group call in the Odoo shell.",
    ),
    _lesson(
        "VS06",
        "Search Views, Default Filters, and Dynamic Date Filters",
        [
            "Build search filters that match daily work.",
            "Set default filters from actions.",
            "Use dynamic datetime domains safely.",
        ],
        "A search view turns a generic model list into a work queue, a reporting entry point, or a compliance review screen.",
        "Start with the questions users ask every day, then encode those questions as filters, separators, date filters, and search fields with understandable labels.",
        "Declare filters in the search view, pass search_default keys from the action context, and use context_today or relative datetime helpers carefully in domains.",
        "Verify defaults from every menu and action that opens the model because the same search view may serve multiple workflows with different assumptions.",
        "Dynamic filters are powerful during operations but risky during audits, so reports that require a fixed period should store or pass explicit dates.",
        [
            "Search filters are reusable domain snippets.",
            "search_default_filter_name activates a named filter.",
            "Dynamic dates are evaluated relative to context.",
            "Search fields should map to indexed or useful fields.",
            "Menus can share a search view with different contexts.",
        ],
        [
            {
                "title": "Default active and this-month filters",
                "code": '''<search string="Courses">
    <field name="name"/>
    <field name="teacher_id"/>
    <filter name="active" string="Active" domain="[('active', '=', True)]"/>
    <filter name="this_month" string="Starts This Month"
            domain="[('start_date', '&gt;=', context_today().strftime('%Y-%m-01'))]"/>
    <filter name="group_teacher" string="Teacher" context="{'group_by': 'teacher_id'}"/>
</search>''',
                "explain": "The search view offers direct text search, a reusable active filter, a dynamic date filter, and a group-by shortcut.",
            }
        ],
        [
            "Using dynamic filters for legally fixed reporting periods.",
            "Forgetting that action context controls default filters.",
            "Adding filters users cannot explain.",
            "Creating domains that ignore timezone expectations.",
        ],
        "Create a menu that opens courses with Active and Starts This Month enabled by default, then add a second menu that opens the same model without those defaults.",
    ),
    _lesson(
        "VS07",
        "Search Panel and Groupby UX",
        [
            "Use search panels for guided filtering.",
            "Design groupby options that explain the data.",
            "Avoid filter combinations that create empty screens.",
        ],
        "The search panel is a navigation aid for users who think in categories more than domains.",
        "Use it when the model has meaningful many2one, many2many, selection, or hierarchy fields that users naturally use to narrow a dataset.",
        "Define searchpanel fields separately from groupby filters and decide whether a user needs counters, multi-select, or category dependencies.",
        "Test large datasets because counters and many category values can become expensive if the model or domains are not indexed well.",
        "A good search panel reduces training cost because new users discover the available dimensions without memorizing advanced search syntax.",
        [
            "Search panel fields guide filtering from the left side.",
            "Groupby filters change result organization, not just filtering.",
            "Counters can have performance cost.",
            "Hierarchies need clean parent relationships.",
            "Use labels that match business language.",
        ],
        [
            {
                "title": "Category and teacher search panel",
                "code": '''<search string="Courses">
    <field name="name"/>
    <searchpanel>
        <field name="category_id" icon="fa-folder-open" enable_counters="1"/>
        <field name="teacher_id" select="multi" icon="fa-user"/>
    </searchpanel>
    <filter name="group_category" string="Category" context="{'group_by': 'category_id'}"/>
</search>''',
                "explain": "The panel supports guided category and teacher filtering while groupby remains a separate analytical option.",
            }
        ],
        [
            "Enabling counters on a model with slow domains without measuring.",
            "Duplicating every groupby as a search panel field.",
            "Using technical field names as labels.",
            "Assuming search panel visibility is a security boundary.",
        ],
        "Add a search panel to a course model with categories and teachers, then measure the difference between counters enabled and disabled on sample data.",
    ),
    _lesson(
        "VS08",
        "Form Customization with Groups, Tags, and Widgets",
        [
            "Create clean form layouts with semantic grouping.",
            "Use tags and widgets where they improve comprehension.",
            "Keep forms aligned with business workflow.",
        ],
        "A form view is where the user understands and changes one business object, so layout communicates priority as much as labels do.",
        "Group fields by decision area, place identity fields first, and use widgets such as many2many_tags only when the compact representation is easier to read.",
        "Use sheet, group, separator, field options, placeholder, widget, and help text in a way that supports scanning without turning the form into a dashboard.",
        "Review the form at common screen sizes, with empty and populated data, and with readonly states so the layout does not collapse when fields disappear.",
        "Stable form design reduces downstream customizations because partners can inherit predictable groups and users develop muscle memory.",
        [
            "Forms should tell a story about one record.",
            "sheet and group provide standard Odoo visual structure.",
            "many2many_tags is compact but can hide detail.",
            "Place technical fields only when they help the workflow.",
            "Readable anchors make later inheritance safer.",
        ],
        [
            {
                "title": "Structured course form",
                "code": '''<form string="Course">
    <sheet>
        <group>
            <group string="Identity">
                <field name="name" placeholder="Functional Odoo Basics"/>
                <field name="category_id"/>
                <field name="tag_ids" widget="many2many_tags"/>
            </group>
            <group string="Delivery">
                <field name="teacher_id"/>
                <field name="start_date"/>
                <field name="duration_hours"/>
            </group>
        </group>
    </sheet>
</form>''',
                "explain": "The form separates identity from delivery so users can understand the record before editing schedule details.",
            }
        ],
        [
            "Making one enormous group with no visual hierarchy.",
            "Using tag widgets for records where users need columns or attributes.",
            "Hiding required context in tabs users rarely open.",
            "Letting inherited views depend on brittle positional anchors.",
        ],
        "Redesign a flat form into two groups and one tag field, then inspect the final architecture after installing a second module that inherits it.",
    ),
    _lesson(
        "VS09",
        "Notebook Pages, Button Containers, Header Buttons, and Statusbars",
        [
            "Use notebook pages for secondary information.",
            "Place workflow buttons in the header.",
            "Represent state with a statusbar widget.",
        ],
        "The header and notebook areas turn a simple form into a workflow screen without requiring custom JavaScript.",
        "Put state-changing actions where users expect workflow controls, and use notebook pages for details that matter after the primary identity is understood.",
        "Implement object buttons for Python methods, action buttons for client actions or window actions, and statusbar_visible to show the intended lifecycle.",
        "Verify every button in every state with access rights applied, because a visible button that fails server-side damages user trust.",
        "A disciplined header prevents form sprawl: actions are discoverable, state is explicit, and secondary data stays organized.",
        [
            "Header buttons should map to business transitions.",
            "statusbar displays the lifecycle field.",
            "Notebook pages are for secondary or repeated information.",
            "Button visibility should match server-side rules.",
            "Use button_box for smart buttons, not random actions.",
        ],
        [
            {
                "title": "Workflow header and notebook",
                "code": '''<form string="Course">
    <header>
        <button name="action_confirm" type="object" string="Confirm"
                class="oe_highlight" invisible="state != 'draft'"/>
        <button name="action_done" type="object" string="Mark Done"
                invisible="state != 'confirmed'"/>
        <field name="state" widget="statusbar"
               statusbar_visible="draft,confirmed,done"/>
    </header>
    <sheet>
        <notebook>
            <page string="Sessions">
                <field name="session_ids"/>
            </page>
            <page string="Notes">
                <field name="internal_note"/>
            </page>
        </notebook>
    </sheet>
</form>''',
                "explain": "The header owns the lifecycle while the notebook separates operational details from notes.",
            }
        ],
        [
            "Putting workflow buttons in random groups inside the form.",
            "Showing states in the statusbar that users cannot reach.",
            "Hiding buttons only in XML while Python methods remain too permissive.",
            "Using notebooks for required first-step data.",
        ],
        "Add a draft-confirmed-done workflow with header buttons, then test every transition as a manager and as a read-only user.",
    ),
    _lesson(
        "VS10",
        "Attrs Migration and Dynamic Readonly, Invisible, Required Rules",
        [
            "Convert legacy attrs and states into modern modifier expressions.",
            "Use readonly, invisible, and required conditions safely.",
            "Design dynamic statusbar behavior without hiding business truth.",
        ],
        "Odoo's view modifiers evolved from attrs dictionaries toward direct Python-like expressions in XML attributes.",
        "Treat migration as a chance to simplify conditions rather than translating every old attrs expression mechanically.",
        "Write direct invisible, readonly, and required expressions against fields loaded in the view, and keep dynamic statusbar_visible decisions tied to meaningful workflow states.",
        "Compare the final architecture before and after migration and test records in each state because modifier errors often appear only with specific values.",
        "Clear modifier expressions survive upgrades better because reviewers can understand the condition without unpacking nested domain tuples.",
        [
            "Modern modifiers use direct expressions such as invisible=\"state != 'draft'\".",
            "Fields referenced by expressions must be available to the client.",
            "Required conditions should match model constraints where possible.",
            "Migration is a refactoring opportunity.",
            "Server-side validation remains authoritative.",
        ],
        [
            {
                "title": "Modern modifiers replacing attrs",
                "code": '''<field name="cancel_reason"
       invisible="state != 'cancel'"
       required="state == 'cancel'"
       readonly="state in ('done', 'cancel')"/>
<field name="state" widget="statusbar"
       statusbar_visible="draft,confirmed,done,cancel"/>''',
                "explain": "The conditions are readable in place and no longer require a nested attrs dictionary.",
            }
        ],
        [
            "Migrating syntax without checking behavior in every state.",
            "Referencing a field not present in the view.",
            "Using invisible required fields without a server default.",
            "Relying on UI required rules instead of model constraints.",
        ],
        "Take a legacy form using attrs, convert three modifiers to direct expressions, and run through draft, confirmed, done, and cancel examples.",
    ),
    _lesson(
        "VS11",
        "Buttons that Open Forms, URL Actions, and Disabled Actions",
        [
            "Return window actions from object buttons.",
            "Create URL actions for external systems.",
            "Disable buttons through state and group rules.",
        ],
        "Buttons connect views to behavior, so every button should make the next user step obvious and safe.",
        "Choose object buttons for model methods, action buttons for existing actions, stat buttons for counters, and URL actions only when the target is trustworthy.",
        "Return ir.actions.act_window dictionaries for opening forms, use target='new' for modal flows, and make visibility conditions mirror server-side checks.",
        "Test buttons with missing related records, blocked access rights, and invalid states because button methods often become support hot spots.",
        "The production rule is simple: a disabled or hidden button is only a usability hint, while Python access checks are the real control.",
        [
            "type='object' calls a model method.",
            "Window actions can open a specific record form.",
            "URL actions should be generated from trusted values.",
            "Button visibility is not authorization.",
            "Use groups on buttons for role-specific actions.",
        ],
        [
            {
                "title": "Open the related partner form",
                "code": '''def action_open_teacher_partner(self):
    self.ensure_one()
    return {
        "type": "ir.actions.act_window",
        "name": "Teacher",
        "res_model": "res.partner",
        "res_id": self.teacher_id.id,
        "view_mode": "form",
        "target": "current",
    }''',
                "explain": "The object button returns a precise form action instead of relying on a generic menu action.",
            }
        ],
        [
            "Building URLs from user input without validation.",
            "Hiding a button but leaving the method callable by any user.",
            "Returning an action without res_id when a specific form is expected.",
            "Using buttons for operations that should be computed automatically.",
        ],
        "Add a smart button that opens the teacher partner and a separate URL action to documentation, then secure the object method with a group check.",
    ),
    _lesson(
        "VS12",
        "Kanban Views, Templates, and Images",
        [
            "Build kanban cards with QWeb templates.",
            "Render image fields efficiently.",
            "Choose card content that supports quick triage.",
        ],
        "Kanban views are visual workspaces for records that benefit from cards, images, statuses, or stage-based scanning.",
        "Design the card around the action users take next, not around showing every field in a compact rectangle.",
        "Declare fields before templates, use kanban_image or image data URLs carefully, and keep card templates simple enough for inheritance.",
        "Verify empty images, slow networks, mobile widths, and access to binary fields because kanban screens often become the first page users open.",
        "A useful kanban card has strong information scent: a user can decide whether to open the record in a few seconds.",
        [
            "Kanban templates use QWeb under the kanban arch.",
            "Fields must be declared for use in templates.",
            "Images should have fallbacks.",
            "Cards should prioritize the next action.",
            "Keep templates easy to inherit.",
        ],
        [
            {
                "title": "Course kanban with image fallback",
                "code": '''<kanban>
    <field name="name"/>
    <field name="teacher_id"/>
    <field name="image_128"/>
    <templates>
        <t t-name="kanban-box">
            <div class="oe_kanban_global_click o_kanban_record">
                <img t-att-src="kanban_image('training.course', 'image_128', record.id.raw_value)"
                     class="o_kanban_image"/>
                <strong><field name="name"/></strong>
                <div><field name="teacher_id"/></div>
            </div>
        </t>
    </templates>
</kanban>''',
                "explain": "The card declares fields used by the QWeb template and uses the standard kanban image helper.",
            }
        ],
        [
            "Using undeclared fields inside the kanban template.",
            "Putting large binary images directly into crowded cards.",
            "Making every element clickable with unclear affordance.",
            "Forgetting fallback behavior when images are empty.",
        ],
        "Create a kanban card with an image, title, teacher, and state badge, then test it with records that do and do not have images.",
    ),
    _lesson(
        "VS13",
        "Kanban Drag and Drop, Handle Ordering, and Progressbars",
        [
            "Enable stage-based drag and drop in kanban.",
            "Use sequence fields for manual ordering.",
            "Display progressbar summaries on kanban columns.",
        ],
        "Kanban becomes operational when records can move between stages and users can see column-level progress.",
        "Only enable drag and drop when a move is a valid business transition; otherwise the UI invites users to bypass workflow thinking.",
        "Use default_group_by for stages, a handle sequence for ordering, and progressbar definitions for quick aggregated status.",
        "Test dragging with record rules, state constraints, and onchange side effects because kanban writes happen quickly from the client.",
        "Production kanban design must balance speed and control: the faster the drag gesture, the more reliable the server-side transition rules must be.",
        [
            "default_group_by creates a column-oriented kanban.",
            "Drag and drop writes the grouped field.",
            "Handle ordering needs a sequence field.",
            "Progressbars summarize grouped records.",
            "Server constraints must protect invalid moves.",
        ],
        [
            {
                "title": "Stage kanban with progressbar",
                "code": '''<kanban default_group_by="stage_id" records_draggable="1">
    <field name="stage_id"/>
    <field name="sequence"/>
    <field name="state"/>
    <progressbar field="state"
                 colors="{'draft': 'muted', 'confirmed': 'warning', 'done': 'success'}"/>
    <templates>
        <t t-name="kanban-box">
            <div class="oe_kanban_global_click">
                <field name="sequence" widget="handle"/>
                <strong><field name="name"/></strong>
            </div>
        </t>
    </templates>
</kanban>''',
                "explain": "The kanban groups by stage, allows drag ordering, and visualizes state distribution per column.",
            }
        ],
        [
            "Allowing drag and drop when state transitions require approvals.",
            "Forgetting access rules on the grouped field.",
            "Using progressbar colors with states that do not exist.",
            "Assuming client drag behavior replaces server validation.",
        ],
        "Build a stage kanban, add a constraint that blocks moving done records back to draft, and verify the drag is rejected.",
    ),
    _lesson(
        "VS14",
        "Graph, Pivot, Cohort, and Gantt Views",
        [
            "Select the correct analytical view for the question.",
            "Configure measures and intervals.",
            "Understand enterprise-only planning views such as cohort and gantt.",
        ],
        "Analytical views answer different questions: graph shows shape, pivot supports exploration, cohort tracks retention, and gantt plans time.",
        "Start from the business question and expected measure, then choose the view type rather than adding every reporting view automatically.",
        "Declare measures, row and column fields, date intervals, and dependencies with stored fields so the database can aggregate predictably.",
        "Validate analytical views with known fixtures and compare totals against read_group or SQL because a beautiful chart can still be wrong.",
        "In production, reporting views become decision tools, so access rules, date ranges, and measure definitions must be as carefully reviewed as forms.",
        [
            "Graph views visualize aggregated measures.",
            "Pivot views support exploratory analysis.",
            "Cohort views track behavior over periods.",
            "Gantt views schedule records across dates.",
            "Stored fields make reporting reliable.",
        ],
        [
            {
                "title": "Revenue pivot and graph",
                "code": '''<pivot string="Course Revenue">
    <field name="teacher_id" type="row"/>
    <field name="start_date" interval="month" type="col"/>
    <field name="price_total" type="measure"/>
</pivot>

<graph string="Seats by Month" type="bar">
    <field name="start_date" interval="month"/>
    <field name="seat_count" type="measure"/>
</graph>''',
                "explain": "The pivot supports analysis by teacher and month, while the graph shows capacity trends.",
            }
        ],
        [
            "Using non-stored computed measures.",
            "Mixing unrelated measures in one graph.",
            "Forgetting enterprise availability for cohort and gantt.",
            "Ignoring access-rule effects on reported totals.",
        ],
        "Create graph and pivot views for courses, seed five months of data, and verify one total manually with read_group.",
    ),
    _lesson(
        "VS15",
        "Security Overview: Six Components, Groups, Categories, and Hierarchy",
        [
            "Describe the main layers of Odoo security.",
            "Organize groups under useful application categories.",
            "Explain parent-child group relationships to functional users.",
        ],
        "Odoo security is layered: model access rights, record rules, groups, field/view/action group restrictions, sudo boundaries, and business-method checks all matter.",
        "Design roles from real job responsibilities, then map them to groups and categories that users can understand in the Settings UI.",
        "Create module categories for clean group presentation and define parent-child categories only when they reflect a real application hierarchy.",
        "Verify each role with a separate user, not by switching an administrator's groups while staying in the same browser session.",
        "Security that is easy to explain is easier to audit; if a role requires a diagram to justify every permission, the design is probably too broad.",
        [
            "Security has more than CSV access rights.",
            "Groups collect permissions and UI visibility.",
            "Categories organize groups in the user form.",
            "Record rules restrict rows after model access is granted.",
            "Business methods must still check sensitive transitions.",
        ],
        [
            {
                "title": "Application category and groups",
                "code": '''<record id="module_category_training" model="ir.module.category">
    <field name="name">Training</field>
    <field name="sequence">35</field>
</record>

<record id="group_training_user" model="res.groups">
    <field name="name">Training User</field>
    <field name="category_id" ref="module_category_training"/>
</record>''',
                "explain": "The category makes the group visible in the expected application section of the user form.",
            }
        ],
        [
            "Assuming menus are security controls.",
            "Designing groups from developer convenience instead of job roles.",
            "Granting broad access and trying to patch it later with record rules.",
            "Testing security only as the administrator.",
        ],
        "Create three job-role groups for a training app and write a one-sentence business description for each before adding permissions.",
    ),
    _lesson(
        "VS16",
        "Implied Groups and Combobox Group Selection",
        [
            "Use implied_ids to build role inheritance.",
            "Understand group selection behavior in the user form.",
            "Avoid accidental privilege escalation through implied groups.",
        ],
        "Implied groups let one role include another role, which keeps permissions maintainable when managers should also have normal user capabilities.",
        "Design implication from smaller to larger roles and make the chain obvious; hidden implication is a common source of unexpected access.",
        "Set implied_ids with the many2many command syntax and use exclusive category behavior carefully when groups are presented as a combobox-style selection.",
        "Test adding and removing groups from a user because implied groups may remain or disappear in ways that surprise administrators.",
        "In production, implied groups are part of privilege design, so review them like code and document why each implication exists.",
        [
            "implied_ids grants included groups automatically.",
            "Role inheritance should go from broad basic access to stronger roles.",
            "Group categories affect how selections appear on users.",
            "Removing an implying group can affect implied membership.",
            "Implication is not a substitute for record rules.",
        ],
        [
            {
                "title": "Manager implies user",
                "code": '''<record id="group_training_manager" model="res.groups">
    <field name="name">Training Manager</field>
    <field name="category_id" ref="module_category_training"/>
    <field name="implied_ids" eval="[(4, ref('training.group_training_user'))]"/>
</record>''',
                "explain": "A manager automatically receives the base user permissions instead of duplicating them.",
            }
        ],
        [
            "Creating circular or confusing implication chains.",
            "Using implied groups to hide overly broad access rights.",
            "Forgetting that implied groups affect all users assigned the parent group.",
            "Not testing group removal behavior.",
        ],
        "Create user, teacher, and manager groups where manager implies teacher and teacher implies user, then inspect the effective groups on a test user.",
    ),
    _lesson(
        "VS17",
        "Access Rights in CSV and XML",
        [
            "Write ir.model.access.csv rows correctly.",
            "Know when XML access records are useful.",
            "Separate model access from row-level record rules.",
        ],
        "Access rights answer whether a group may create, read, write, or delete records of a model at all.",
        "Use CSV for normal module permissions because it is compact, reviewable, and recognized by Odoo conventions.",
        "Use XML only for exceptional cases where you need update behavior, conditions around noupdate data, or integration with a generated data process.",
        "Verify access with a user who has only the target group, because inherited administrator permissions can hide missing CSV rows.",
        "A clean access matrix is the foundation for every later record rule; record rules cannot grant access if model access denies it.",
        [
            "CSV rows live in security/ir.model.access.csv.",
            "perm_create/read/write/unlink are independent booleans.",
            "The model_id value references model_model_name.",
            "Record rules filter rows after access rights pass.",
            "XML access records are possible but less common.",
        ],
        [
            {
                "title": "Access CSV for course users",
                "code": '''id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_training_course_user,training.course user,model_training_course,training.group_training_user,1,0,0,0
access_training_course_manager,training.course manager,model_training_course,training.group_training_manager,1,1,1,1''',
                "explain": "Base users can read courses while managers receive full model-level access.",
            }
        ],
        [
            "Using record rules to compensate for missing model access.",
            "Misspelling model external ids in CSV.",
            "Granting unlink by default to operational users.",
            "Forgetting access rows for transient models used by wizards.",
        ],
        "Create an access CSV for course and session models, then confirm a read-only user cannot create from the UI or via RPC.",
    ),
    _lesson(
        "VS18",
        "Record Rules: Why They Exist and How Domains Work",
        [
            "Explain record rules as row-level filters.",
            "Write domains that match business ownership.",
            "Understand global and group-specific rule behavior.",
        ],
        "Record rules restrict which rows a user can see or change after model access rights have allowed the operation.",
        "Design rules from ownership and responsibility: own records, company records, assigned team records, or records in an approved state.",
        "Write domains using user, company, and field values, then assign rules to groups unless the rule truly applies globally.",
        "Test read, write, create, and unlink separately because record rules can be operation-specific and may interact in surprising ways.",
        "In production, record rules are audit controls; a permissive domain can expose customer, payroll, or student data even when menus look correct.",
        [
            "Rules are domains on records.",
            "Model access must pass before record rules matter.",
            "Global rules combine with group rules.",
            "Rules can be limited by operation.",
            "Domains should be readable and testable.",
        ],
        [
            {
                "title": "Own-record rule",
                "code": '''<record id="rule_training_course_own_teacher" model="ir.rule">
    <field name="name">Teachers see their courses</field>
    <field name="model_id" ref="model_training_course"/>
    <field name="domain_force">[('teacher_user_id', '=', user.id)]</field>
    <field name="groups" eval="[(4, ref('training.group_training_teacher'))]"/>
</record>''',
                "explain": "The rule limits teacher users to courses connected to their own user record.",
            }
        ],
        [
            "Forgetting that read rules also affect many2one display names.",
            "Creating global rules when a group rule was intended.",
            "Using domains that depend on fields users cannot access.",
            "Testing only one operation.",
        ],
        "Write a rule that lets teachers read only their assigned courses, then verify the list, form, export, and many2one search behavior.",
    ),
    _lesson(
        "VS19",
        "Record Rules Student and Teacher Example",
        [
            "Model a realistic student-teacher security matrix.",
            "Combine group access and record ownership.",
            "Validate cross-role behavior with fixtures.",
        ],
        "Education and training modules are excellent record-rule examples because students, teachers, and managers see overlapping but different data.",
        "Give every role the smallest model access it needs, then use rules for ownership: students see their enrollments, teachers see their courses, managers see all.",
        "Use related fields such as student_user_id and teacher_user_id to make domains readable and avoid deep joins where possible.",
        "Create fixture users for each role and run scripted checks so future developers do not accidentally widen a rule during maintenance.",
        "The goal is not to hide screens; the goal is to make every data path return only the records the business allows.",
        [
            "Students and teachers need different ownership fields.",
            "Managers often need a broader rule, not sudo everywhere.",
            "Related user fields simplify domains.",
            "Fixtures make rule testing repeatable.",
            "Rules affect UI and RPC access.",
        ],
        [
            {
                "title": "Student and teacher domains",
                "code": '''<record id="rule_enrollment_student_self" model="ir.rule">
    <field name="name">Students see own enrollments</field>
    <field name="model_id" ref="model_training_enrollment"/>
    <field name="domain_force">[('student_user_id', '=', user.id)]</field>
    <field name="groups" eval="[(4, ref('training.group_training_student'))]"/>
</record>

<record id="rule_enrollment_teacher_courses" model="ir.rule">
    <field name="name">Teachers see course enrollments</field>
    <field name="model_id" ref="model_training_enrollment"/>
    <field name="domain_force">[('course_id.teacher_user_id', '=', user.id)]</field>
    <field name="groups" eval="[(4, ref('training.group_training_teacher'))]"/>
</record>''',
                "explain": "The student rule follows direct ownership while the teacher rule follows the course relationship.",
            }
        ],
        [
            "Letting students read the course roster through an unrestricted related model.",
            "Using sudo in controllers instead of fixing the rule design.",
            "Forgetting portal or external users if the module exposes them.",
            "Assuming a hidden menu blocks RPC reads.",
        ],
        "Create three users and four enrollments, then prove each role sees the expected records through the UI and an XML-RPC read call.",
    ),
    _lesson(
        "VS20",
        "Security Inheritance and Groups on Fields, Views, and Actions",
        [
            "Apply groups attributes to UI elements.",
            "Understand how inherited security data changes effective permissions.",
            "Avoid confusing UI restrictions with real authorization.",
        ],
        "Security inheritance happens when modules add groups, access rows, rules, or UI restrictions on top of existing behavior.",
        "Use groups on fields, buttons, menus, views, and actions to reduce clutter for users who cannot use those features anyway.",
        "Keep actual data protection in access rights, record rules, and business methods; groups on views are a presentation and workflow control.",
        "Test inherited modules in the full dependency stack because a later module may add a broad rule or imply a powerful group.",
        "Good security inheritance is additive and reviewable, while scattered group attributes become hard to audit during upgrades.",
        [
            "groups attributes hide UI elements from users outside the group.",
            "Menus and actions can be group-restricted.",
            "Field-level groups can protect field visibility.",
            "Server-side checks remain necessary.",
            "Inherited modules can widen or narrow effective access.",
        ],
        [
            {
                "title": "Group-restricted margin field and action",
                "code": '''<field name="margin_percent" groups="training.group_training_manager"/>

<record id="training_finance_action" model="ir.actions.act_window">
    <field name="name">Course Margins</field>
    <field name="res_model">training.course</field>
    <field name="view_mode">pivot,graph</field>
    <field name="groups_id" eval="[(4, ref('training.group_training_manager'))]"/>
</record>''',
                "explain": "Managers see finance information in the view and can access the reporting action, but model security must still protect the data.",
            }
        ],
        [
            "Believing hidden fields are secure if the model allows read.",
            "Adding group attributes in many inherited views without a central role design.",
            "Forgetting server checks on object buttons.",
            "Not reviewing implied groups when a module is installed.",
        ],
        "Hide a margin field and finance action from normal users, then attempt to read the field by RPC to confirm whether server security is sufficient.",
    ),
    _lesson(
        "VS21",
        "Odoo 19 Privilege Model",
        [
            "Understand the direction of Odoo 19 privilege tightening.",
            "Identify where custom modules depend on broad administrative behavior.",
            "Plan privilege reviews during upgrades.",
        ],
        "Odoo 19 continues the trend of making privileges more explicit, especially around administrative operations, technical settings, and cross-app access.",
        "Audit custom modules for places where code assumes that a user with one application role can manage technical records or operate outside their business scope.",
        "Keep methods explicit about sudo usage, group checks, and record ownership so a framework privilege change does not silently break or overexpose behavior.",
        "During verification, run upgrade tests with real users for settings, imports, server actions, scheduled jobs, and any custom controller endpoint.",
        "Privilege models evolve because production systems need stronger boundaries; custom modules should be ready by avoiding implicit administrator shortcuts.",
        [
            "Expect stronger separation between business and technical privileges.",
            "Audit sudo calls and administrative group checks.",
            "Do not assume old Settings access remains enough.",
            "Test server actions and scheduled jobs during upgrade.",
            "Treat privilege changes as security changes, not only migration work.",
        ],
        [
            {
                "title": "Explicit group check around sensitive action",
                "code": '''def action_recompute_certificates(self):
    if not self.env.user.has_group("training.group_training_manager"):
        raise AccessError("Only training managers can recompute certificates.")
    self.sudo()._recompute_certificate_numbers()
    return True''',
                "explain": "The method checks the business role before using sudo for the narrow internal operation.",
            }
        ],
        [
            "Using sudo to make upgrade errors disappear.",
            "Assuming a technical user interface group equals business approval.",
            "Leaving server actions callable by broad groups.",
            "Skipping tests for scheduled and automated actions.",
        ],
        "Review one custom module and list every sudo call, then classify each as required, removable, or needing a preceding group check.",
    ),
    _lesson(
        "VS22",
        "Odoo 18 to 19 Migration Notes for Views and Security",
        [
            "Plan view modifier migration work.",
            "Review deprecated XML patterns.",
            "Regression-test security after framework upgrades.",
        ],
        "Migration from Odoo 18 to 19 should be treated as a behavioral review, not a search-and-replace exercise.",
        "Inventory view modifiers, JavaScript widgets, access files, record rules, automated actions, and reports before changing code.",
        "Update XML syntax where required, remove obsolete patterns, and prefer direct modifier expressions and clear inherited views over compatibility clutter.",
        "Run upgrade tests from a fresh restored database, then test real role journeys because view errors and security regressions often appear only after registry reload.",
        "A good migration leaves the module easier to understand than before; do not preserve unshipped branch behavior by layering shims around it.",
        [
            "Inventory before editing.",
            "Migrate modifiers deliberately.",
            "Review groups, access rights, and record rules together.",
            "Test reports and server actions, not only menus.",
            "Keep migration commits focused.",
        ],
        [
            {
                "title": "Migration checklist fragment",
                "code": '''# Suggested review commands
rg "attrs=|states=" custom_addons/training
rg "sudo\\(|has_group\\(" custom_addons/training
rg "ir.rule|ir.model.access|groups=" custom_addons/training/security custom_addons/training/views''',
                "explain": "The first pass locates legacy modifiers, privilege-sensitive code, and security XML that deserve manual review.",
            }
        ],
        [
            "Migrating syntax without comparing behavior.",
            "Leaving obsolete inherited views that no longer match upstream anchors.",
            "Testing only with admin users.",
            "Combining migration with unrelated refactors.",
        ],
        "Build a migration checklist for one module, convert two legacy modifiers, and document one security rule that needs a functional owner review.",
    ),
    _lesson(
        "VS23",
        "XML Data, CSV Data, and Choosing Between Them",
        [
            "Choose XML or CSV based on data shape.",
            "Load reference data idempotently.",
            "Understand noupdate implications.",
        ],
        "Odoo modules use data files to install configuration, security, records, actions, and sometimes initial business data.",
        "Use XML when records need references, nested structure, eval expressions, noupdate control, or readable grouping; use CSV for flat bulk rows.",
        "Keep reference data stable with external ids and be careful with noupdate because it protects user-edited records from future module updates.",
        "Test install, update, uninstall where relevant, and import into a fresh database because data files often pass locally only due to leftover records.",
        "The correct file format reduces future migration pain: XML is expressive, CSV is efficient, and mixing them intentionally is normal.",
        [
            "XML is better for relational configuration records.",
            "CSV is better for large flat datasets.",
            "noupdate affects later module updates.",
            "External ids make data repeatable.",
            "Manifest order controls references.",
        ],
        [
            {
                "title": "Reference category XML",
                "code": '''<odoo noupdate="1">
    <record id="course_category_functional" model="training.course.category">
        <field name="name">Functional</field>
        <field name="sequence">10</field>
    </record>
    <record id="course_category_technical" model="training.course.category">
        <field name="name">Technical</field>
        <field name="sequence">20</field>
    </record>
</odoo>''',
                "explain": "noupdate is appropriate when administrators may rename categories after installation.",
            }
        ],
        [
            "Using CSV for records that need complex references or eval.",
            "Putting user-editable configuration outside noupdate without a reason.",
            "Referencing records before their files load.",
            "Duplicating records by removing external ids.",
        ],
        "Create the same three category records in XML and CSV, then decide which version should ship and explain the upgrade behavior.",
    ),
    _lesson(
        "VS24",
        "View Inheritance Overview and XPath Positions",
        [
            "Use inherited views instead of copying base views.",
            "Select robust XPath anchors.",
            "Apply position attributes safely.",
        ],
        "View inheritance lets modules extend or change existing screens without replacing the upstream view entirely.",
        "Choose XPath anchors that express intent and are likely to survive upgrades, such as named fields or groups with stable names.",
        "Use positions before, after, inside, replace, attributes, and move carefully, keeping each inherited view focused on one business change.",
        "Verify the final combined architecture in developer mode and run module updates after upstream changes because broken XPaths fail at load time.",
        "Small inherited views make customizations easier to remove during migrations and easier for another developer to review.",
        [
            "inherit_id points to the parent view.",
            "XPath anchors should be stable and specific.",
            "position='attributes' changes attributes only.",
            "Avoid copying full upstream views.",
            "One inherited view should have one clear purpose.",
        ],
        [
            {
                "title": "Add a field after teacher",
                "code": '''<record id="training_course_form_inherit_capacity" model="ir.ui.view">
    <field name="name">training.course.form.inherit.capacity</field>
    <field name="model">training.course</field>
    <field name="inherit_id" ref="training.training_course_view_form"/>
    <field name="arch" type="xml">
        <xpath expr="//field[@name='teacher_id']" position="after">
            <field name="seat_count"/>
        </xpath>
        <xpath expr="//field[@name='price_total']" position="attributes">
            <attribute name="groups">training.group_training_manager</attribute>
        </xpath>
    </field>
</record>''',
                "explain": "The extension adds one field and changes one attribute without copying the whole parent form.",
            }
        ],
        [
            "Using positional XPaths like //group[2] that break after small upstream changes.",
            "Replacing large blocks when attributes would be enough.",
            "Combining unrelated changes in one inherited view.",
            "Ignoring priority when multiple modules inherit the same target.",
        ],
        "Inherit a form twice from two small modules, then inspect how priority and XPath anchors affect the final architecture.",
    ),
    _lesson(
        "VS25",
        "ir.sequence for Business Numbers",
        [
            "Create reliable sequence records.",
            "Assign sequence values in create.",
            "Handle company-specific numbering when needed.",
        ],
        "Business users expect order numbers, certificate numbers, and ticket references to be unique, readable, and stable.",
        "Decide whether the number is legal, operational, or cosmetic because that determines gaps, prefixes, date ranges, and company separation.",
        "Define an ir.sequence record with code, prefix, padding, and implementation, then call next_by_code in create only when the placeholder value is still new.",
        "Test imports, duplicate creation, multi-company behavior, and rollback scenarios so the sequence does not create confusing references.",
        "A sequence is part of external communication; changing it carelessly can break integrations, printed reports, and customer support procedures.",
        [
            "Use code as the stable lookup key.",
            "Assign numbers server-side in create.",
            "Do not recompute sequence values on write.",
            "Date ranges and companies change numbering behavior.",
            "Legal sequences may require stricter gap handling.",
        ],
        [
            {
                "title": "Certificate sequence",
                "code": '''<record id="seq_training_certificate" model="ir.sequence">
    <field name="name">Training Certificate</field>
    <field name="code">training.certificate</field>
    <field name="prefix">CERT/%(year)s/</field>
    <field name="padding">5</field>
</record>

@api.model_create_multi
def create(self, vals_list):
    for vals in vals_list:
        if vals.get("name", "New") == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("training.certificate")
    return super().create(vals_list)''',
                "explain": "The XML defines the sequence and create assigns it once when the record is created.",
            }
        ],
        [
            "Calling next_by_code in default_get and consuming numbers for abandoned forms.",
            "Changing sequence prefixes without migration communication.",
            "Using one sequence when companies require separate ranges.",
            "Allowing users to edit legal sequence numbers casually.",
        ],
        "Add a certificate number sequence, create records through UI and import, and confirm every saved record receives one unique number.",
    ),
    _lesson(
        "VS26",
        "QWeb Intro and Core Directives",
        [
            "Explain how QWeb renders XML templates.",
            "Use t-call, t-set, t-esc, and t-att safely.",
            "Separate template logic from business logic.",
        ],
        "QWeb is Odoo's XML templating engine for reports, website fragments, mail snippets, and many kanban templates.",
        "Keep templates focused on presentation and put calculations, permissions, and data preparation in models or report helpers.",
        "Use t-call for composition, t-set for local values, t-esc for escaped output, and t-att or t-attf for attributes that come from safe values.",
        "Render reports with representative records and check HTML output before PDF rendering because QWeb errors can be easier to diagnose in HTML.",
        "Clean QWeb survives design changes because layout can move without rediscovering hidden business logic buried in template conditions.",
        [
            "QWeb templates are XML and must be valid XML.",
            "t-esc escapes output and is safer for user data.",
            "t-call composes reusable templates.",
            "t-att builds dynamic attributes.",
            "Business calculations belong outside templates.",
        ],
        [
            {
                "title": "Reusable certificate block",
                "code": '''<template id="training_certificate_block">
    <div class="certificate">
        <h2><t t-esc="doc.name"/></h2>
        <p>Issued to <span t-esc="doc.student_id.name"/></p>
        <p t-att-class="'grade grade-%s' % doc.grade_code">
            Score: <span t-esc="doc.score"/>
        </p>
    </div>
</template>''',
                "explain": "The template escapes record values and uses a dynamic class for styling without doing heavy calculation in QWeb.",
            }
        ],
        [
            "Using t-raw for user-provided data.",
            "Putting complex calculations in template expressions.",
            "Forgetting XML escaping rules.",
            "Copying templates instead of using t-call.",
        ],
        "Create a QWeb template that renders a certificate title, student name, teacher name, and escaped note field.",
    ),
    _lesson(
        "VS27",
        "QWeb Conditionals, Loops, and Template Inheritance",
        [
            "Use t-if and t-foreach for report structures.",
            "Inherit QWeb templates with XPath.",
            "Keep repeated report sections maintainable.",
        ],
        "Most useful QWeb reports need conditional sections and repeated lines, but that does not mean the template should become a program.",
        "Prepare clean recordsets in Python and let QWeb decide only whether to show sections and how to repeat display rows.",
        "Use t-if, t-elif, t-else, t-foreach, t-as, and inherited templates with XPath to extend report layouts without copying them.",
        "Verify empty lists, one-row lists, and many-row reports because loop boundaries and page breaks are common report defects.",
        "Template inheritance keeps local changes upgradeable; full report copies are expensive when Odoo changes base layouts or assets.",
        [
            "t-if controls conditional rendering.",
            "t-foreach repeats over recordsets or lists.",
            "Template inheritance uses XPath like view inheritance.",
            "Prepare complex data before rendering.",
            "Test empty and long datasets.",
        ],
        [
            {
                "title": "Loop and inherit report template",
                "code": '''<template id="report_course_roster">
    <t t-call="web.external_layout">
        <h2><span t-esc="doc.name"/></h2>
        <table>
            <tr t-foreach="doc.enrollment_ids" t-as="line">
                <td><span t-esc="line.student_id.name"/></td>
                <td><span t-esc="line.state"/></td>
            </tr>
        </table>
        <p t-if="not doc.enrollment_ids">No students enrolled.</p>
    </t>
</template>''',
                "explain": "The template handles both a roster and an empty state with simple QWeb directives.",
            }
        ],
        [
            "Looping over unsorted recordsets when report order matters.",
            "Using t-raw to inject HTML without sanitizing.",
            "Copying external_layout instead of inheriting or calling it.",
            "Forgetting the empty state.",
        ],
        "Build a roster report that shows a table for enrolled students and a clear message when no students are enrolled.",
    ),
    _lesson(
        "VS28",
        "Paper Formats, Barcodes, Images, Server Actions, and Email Templates",
        [
            "Configure report paper formats and media assets.",
            "Add barcode or QR output to PDFs.",
            "Connect server actions and email templates to document workflows.",
        ],
        "Printed documents are often where Odoo leaves the browser and becomes part of legal, warehouse, or customer-facing process.",
        "Define paper format before fine-tuning CSS, because margins, orientation, and DPI change how every report element behaves.",
        "Use report barcode routes for QR codes, serve images from binary fields or attachments, and trigger emails through templates or server actions only after permissions are clear.",
        "Test PDFs with missing images, long names, different companies, and email previews so failures are visible before a customer receives a broken document.",
        "Production reporting is operational communication; once a certificate, invoice, or label is emailed, users expect it to be stable and traceable.",
        [
            "Paper format controls margins, orientation, and page size.",
            "Barcode and QR images can be rendered through report routes.",
            "Binary images need fallbacks and size control.",
            "Server actions should run with deliberate privileges.",
            "Email templates should be previewed with real records.",
        ],
        [
            {
                "title": "QR code and email send",
                "code": '''<img t-att-src="'/report/barcode/QR/%s?width=120&amp;height=120' % doc.verification_url"/>

def action_send_certificate(self):
    self.ensure_one()
    template = self.env.ref("training.email_template_certificate")
    template.send_mail(self.id, force_send=True)
    return True''',
                "explain": "The report renders a QR code from a verification URL and the model action sends the matching email template.",
            }
        ],
        [
            "Hard-coding paper margins in CSS while ignoring paperformat.",
            "Embedding huge images that slow every PDF render.",
            "Running server actions with sudo without business checks.",
            "Sending emails without previewing language and company context.",
        ],
        "Create a certificate PDF with a custom paper format, company logo, QR verification link, and an email template action.",
        [
            {
                "kind": "items",
                "title": "Report production checklist",
                "items": [
                    "Paper format selected",
                    "Images tested when missing",
                    "QR or barcode verified",
                    "Email preview approved",
                    "Permissions reviewed",
                ],
            }
        ],
    ),
]

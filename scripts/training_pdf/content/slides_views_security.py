#!/usr/bin/env python3
"""Atomic beginner-friendly slides for Odoo views, security, and data."""


def _topic(topic_id, title, points, examples):
    return {
        "id": topic_id,
        "title": title,
        "points": points,
        "examples": examples,
    }


SLIDES = [
    {
        "section": 1,
        "title": "List and Search Views",
        "topics": [
            _topic(
                "VS-01",
                "List View Basics",
                [
                    "A list view shows many records in rows.",
                    "Choose columns that help users decide what to open.",
                    "Keep technical fields hidden unless users need them.",
                ],
                [
                    {
                        "label": "Simple list view",
                        "code": """<tree string="Courses">
    <field name="name"/>
    <field name="teacher_id"/>
    <field name="start_date"/>
</tree>""",
                    },
                    {
                        "label": "List view action",
                        "code": """<field name="view_mode">tree,form</field>
<field name="res_model">training.course</field>""",
                    },
                ],
            ),
            _topic(
                "VS-02",
                "Editable List",
                [
                    "Editable lists let users change rows without opening a form.",
                    "Use them for simple line data, not complex workflows.",
                    "Always keep required fields visible or prefilled.",
                ],
                [
                    {
                        "label": "Edit at bottom",
                        "code": """<tree editable="bottom">
    <field name="product_id"/>
    <field name="quantity"/>
</tree>""",
                    },
                    {
                        "label": "Edit at top",
                        "code": """<tree editable="top">
    <field name="name"/>
    <field name="score"/>
</tree>""",
                    },
                ],
            ),
            _topic(
                "VS-03",
                "List Decorations",
                [
                    "Decorations color rows based on field values.",
                    "They guide attention but do not replace real validation.",
                    "Include invisible helper fields when the expression needs them.",
                ],
                [
                    {
                        "label": "Danger row",
                        "code": """<tree decoration-danger="state == 'late'">
    <field name="name"/>
    <field name="state"/>
</tree>""",
                    },
                    {
                        "label": "Hidden helper field",
                        "code": """<field name="deadline_passed" invisible="1"/>
<tree decoration-warning="deadline_passed">
    <field name="name"/>
</tree>""",
                    },
                ],
            ),
            _topic(
                "VS-04",
                "List Button",
                [
                    "A list button starts an action from a row.",
                    "Use object buttons for Python model methods.",
                    "Keep the label short because row space is limited.",
                ],
                [
                    {
                        "label": "Object button",
                        "code": """<button name="action_confirm"
        type="object"
        string="Confirm"
        class="btn-primary"/>""",
                    },
                    {
                        "label": "Button with state rule",
                        "code": """<button name="action_reset"
        type="object"
        string="Reset"
        invisible="state == 'draft'"/>""",
                    },
                ],
            ),
            _topic(
                "VS-05",
                "Sort and Limit",
                [
                    "default_order controls the first sort users see.",
                    "limit controls how many rows load at first.",
                    "Sort on fields that make business sense.",
                ],
                [
                    {
                        "label": "Newest first",
                        "code": """<tree default_order="create_date desc" limit="80">
    <field name="name"/>
</tree>""",
                    },
                    {
                        "label": "Priority queue",
                        "code": """<tree default_order="priority desc, date_deadline">
    <field name="priority"/>
    <field name="date_deadline"/>
</tree>""",
                    },
                ],
            ),
            _topic(
                "VS-06",
                "Group By in Search",
                [
                    "Group by organizes records into collapsible buckets.",
                    "Put common groupings in the search view.",
                    "Use fields that users already understand.",
                ],
                [
                    {
                        "label": "Group by teacher",
                        "code": """<filter string="Teacher"
        name="group_teacher"
        context="{'group_by': 'teacher_id'}"/>""",
                    },
                    {
                        "label": "Group by month",
                        "code": """<filter string="Start Month"
        name="group_start_month"
        context="{'group_by': 'start_date:month'}"/>""",
                    },
                ],
            ),
            _topic(
                "VS-07",
                "Search View Basics",
                [
                    "A search view defines quick filters and search fields.",
                    "It supports both typed search and saved filter buttons.",
                    "Name filters clearly for non-technical users.",
                ],
                [
                    {
                        "label": "Search by fields",
                        "code": """<search string="Courses">
    <field name="name"/>
    <field name="teacher_id"/>
</search>""",
                    },
                    {
                        "label": "Simple filter",
                        "code": """<filter string="Published"
        name="published"
        domain="[('is_published', '=', True)]"/>""",
                    },
                ],
            ),
            _topic(
                "VS-08",
                "Search Panel",
                [
                    "The search panel gives a left-side filter menu.",
                    "It works well for categories, companies, and owners.",
                    "Avoid panels with too many rarely used options.",
                ],
                [
                    {
                        "label": "Category panel",
                        "code": """<searchpanel>
    <field name="category_id"/>
</searchpanel>""",
                    },
                    {
                        "label": "Multi-select panel",
                        "code": """<searchpanel>
    <field name="tag_ids" select="multi"/>
</searchpanel>""",
                    },
                ],
            ),
            _topic(
                "VS-09",
                "Default Filter",
                [
                    "A default filter opens an action with a filter already active.",
                    "Use the action context to enable it.",
                    "The key must match the filter name.",
                ],
                [
                    {
                        "label": "Action context",
                        "code": """<field name="context">
    {'search_default_published': 1}
</field>""",
                    },
                    {
                        "label": "Matching filter",
                        "code": """<filter string="Published"
        name="published"
        domain="[('is_published', '=', True)]"/>""",
                    },
                ],
            ),
            _topic(
                "VS-10",
                "Action View Modes",
                [
                    "view_mode controls which views users can switch between.",
                    "Put the most common view first.",
                    "Do not expose a view type that has no useful design.",
                ],
                [
                    {
                        "label": "List first",
                        "code": """<field name="view_mode">tree,form,kanban</field>""",
                    },
                    {
                        "label": "Report first",
                        "code": """<field name="view_mode">pivot,graph,tree</field>""",
                    },
                ],
            ),
        ],
    },
    {
        "section": 2,
        "title": "Form and Analytical Views",
        "topics": [
            _topic(
                "VS-11",
                "Form Sheet and Group",
                [
                    "A sheet gives the form a document-like area.",
                    "Groups align labels and fields in readable columns.",
                    "Place important fields near the top.",
                ],
                [
                    {
                        "label": "Basic form",
                        "code": """<form string="Course">
    <sheet>
        <group>
            <field name="name"/>
            <field name="teacher_id"/>
        </group>
    </sheet>
</form>""",
                    },
                    {
                        "label": "Two columns",
                        "code": """<group>
    <group><field name="start_date"/></group>
    <group><field name="end_date"/></group>
</group>""",
                    },
                ],
            ),
            _topic(
                "VS-12",
                "Notebook Pages",
                [
                    "A notebook splits a form into tabs.",
                    "Use tabs for secondary details, not the main identity.",
                    "Keep tab names short and task based.",
                ],
                [
                    {
                        "label": "Notebook with lines",
                        "code": """<notebook>
    <page string="Students">
        <field name="student_ids"/>
    </page>
</notebook>""",
                    },
                    {
                        "label": "Notes tab",
                        "code": """<page string="Notes">
    <field name="description"/>
</page>""",
                    },
                ],
            ),
            _topic(
                "VS-13",
                "Statusbar",
                [
                    "A statusbar shows the record stage.",
                    "It usually uses a selection field named state.",
                    "Pair it with buttons that move the workflow forward.",
                ],
                [
                    {
                        "label": "State field",
                        "code": """<field name="state"
       widget="statusbar"
       statusbar_visible="draft,confirmed,done"/>""",
                    },
                    {
                        "label": "Workflow button",
                        "code": """<button name="action_confirm"
        type="object"
        string="Confirm"
        invisible="state != 'draft'"/>""",
                    },
                ],
            ),
            _topic(
                "VS-14",
                "Kanban Basics",
                [
                    "Kanban views show records as cards.",
                    "They are useful for pipelines, tasks, and visual queues.",
                    "Keep each card focused on one quick decision.",
                ],
                [
                    {
                        "label": "Small card",
                        "code": """<kanban>
    <templates>
        <t t-name="kanban-box">
            <div><field name="name"/></div>
        </t>
    </templates>
</kanban>""",
                    },
                    {
                        "label": "Group by stage",
                        "code": """<kanban default_group_by="stage_id">
    <field name="stage_id"/>
</kanban>""",
                    },
                ],
            ),
            _topic(
                "VS-15",
                "Graph View",
                [
                    "A graph view turns records into charts.",
                    "Use measures for numbers and grouping fields for axes.",
                    "Start simple before adding many dimensions.",
                ],
                [
                    {
                        "label": "Bar chart",
                        "code": """<graph string="Enrollments" type="bar">
    <field name="teacher_id"/>
    <field name="student_count" type="measure"/>
</graph>""",
                    },
                    {
                        "label": "Line chart",
                        "code": """<graph string="Revenue" type="line">
    <field name="date" interval="month"/>
    <field name="amount_total" type="measure"/>
</graph>""",
                    },
                ],
            ),
            _topic(
                "VS-16",
                "Pivot View",
                [
                    "A pivot view helps users summarize records.",
                    "Rows and columns are dimensions.",
                    "Measures are numeric values to total or count.",
                ],
                [
                    {
                        "label": "Pivot by teacher",
                        "code": """<pivot string="Course Analysis">
    <field name="teacher_id" type="row"/>
    <field name="student_count" type="measure"/>
</pivot>""",
                    },
                    {
                        "label": "Pivot by month",
                        "code": """<pivot string="Monthly Sales">
    <field name="date_order" interval="month" type="col"/>
    <field name="amount_total" type="measure"/>
</pivot>""",
                    },
                ],
            ),
            _topic(
                "VS-17",
                "Invisible, Readonly, and Required",
                [
                    "View attributes guide user input in the client.",
                    "They improve usability but do not replace server rules.",
                    "Keep expressions easy to read.",
                ],
                [
                    {
                        "label": "Conditional readonly",
                        "code": """<field name="teacher_id"
       readonly="state != 'draft'"/>""",
                    },
                    {
                        "label": "Conditional required",
                        "code": """<field name="cancel_reason"
       invisible="state != 'cancelled'"
       required="state == 'cancelled'"/>""",
                    },
                ],
            ),
            _topic(
                "VS-18",
                "View Inheritance XPath",
                [
                    "XPath lets one module modify another module's view.",
                    "Use stable anchors such as field names or page names.",
                    "Keep inherited changes small and easy to review.",
                ],
                [
                    {
                        "label": "Find a field",
                        "code": """<xpath expr="//field[@name='name']" position="after">
    <field name="code"/>
</xpath>""",
                    },
                    {
                        "label": "Find a page",
                        "code": """<xpath expr="//page[@name='settings']" position="inside">
    <group string="Training"/>
</xpath>""",
                    },
                ],
            ),
        ],
    },
    {
        "section": 3,
        "title": "View Inheritance Positions and Groups",
        "topics": [
            _topic(
                "VS-19",
                "Position After",
                [
                    "position='after' inserts new XML after the matched node.",
                    "It is common for adding a field beside an existing field.",
                    "Use it when order matters for the user.",
                ],
                [
                    {
                        "label": "After a field",
                        "code": """<xpath expr="//field[@name='name']" position="after">
    <field name="short_code"/>
</xpath>""",
                    },
                    {
                        "label": "After a button",
                        "code": """<xpath expr="//button[@name='action_confirm']" position="after">
    <button name="action_print" type="object" string="Print"/>
</xpath>""",
                    },
                ],
            ),
            _topic(
                "VS-20",
                "Position Before",
                [
                    "position='before' inserts new XML before the matched node.",
                    "It is useful when the new field should be seen first.",
                    "Avoid moving too much layout with one XPath.",
                ],
                [
                    {
                        "label": "Before date",
                        "code": """<xpath expr="//field[@name='start_date']" position="before">
    <field name="priority"/>
</xpath>""",
                    },
                    {
                        "label": "Before page",
                        "code": """<xpath expr="//page[@name='notes']" position="before">
    <page name="students" string="Students"/>
</xpath>""",
                    },
                ],
            ),
            _topic(
                "VS-21",
                "Position Inside",
                [
                    "position='inside' adds content inside a matched container.",
                    "It works with group, page, sheet, and header nodes.",
                    "Make sure the target is a container, not a simple field.",
                ],
                [
                    {
                        "label": "Inside group",
                        "code": """<xpath expr="//group[@name='main']" position="inside">
    <field name="level"/>
</xpath>""",
                    },
                    {
                        "label": "Inside header",
                        "code": """<xpath expr="//header" position="inside">
    <button name="action_archive" type="object" string="Archive"/>
</xpath>""",
                    },
                ],
            ),
            _topic(
                "VS-22",
                "Position Replace",
                [
                    "position='replace' removes the matched node and inserts new XML.",
                    "Use it carefully because it can break later inherited views.",
                    "Prefer smaller changes when possible.",
                ],
                [
                    {
                        "label": "Replace a field",
                        "code": """<xpath expr="//field[@name='description']" position="replace">
    <field name="description" placeholder="Write notes here"/>
</xpath>""",
                    },
                    {
                        "label": "Remove by empty replace",
                        "code": """<xpath expr="//field[@name='legacy_code']" position="replace"/>""",
                    },
                ],
            ),
            _topic(
                "VS-23",
                "Security Groups",
                [
                    "A group represents a security role.",
                    "Users receive permissions through their groups.",
                    "Use groups for roles, not for individual people.",
                ],
                [
                    {
                        "label": "Teacher group",
                        "code": """<record id="group_training_teacher" model="res.groups">
    <field name="name">Teacher</field>
</record>""",
                    },
                    {
                        "label": "Student group",
                        "code": """<record id="group_training_student" model="res.groups">
    <field name="name">Student</field>
</record>""",
                    },
                ],
            ),
            _topic(
                "VS-24",
                "Group Category",
                [
                    "A category groups related security roles in the user form.",
                    "It makes permissions easier to understand.",
                    "Use a module-specific category for custom apps.",
                ],
                [
                    {
                        "label": "Category record",
                        "code": """<record id="module_category_training" model="ir.module.category">
    <field name="name">Training</field>
    <field name="sequence">30</field>
</record>""",
                    },
                    {
                        "label": "Group in category",
                        "code": """<field name="category_id"
       ref="module_category_training"/>""",
                    },
                ],
            ),
            _topic(
                "VS-25",
                "Implied Groups",
                [
                    "implied_ids automatically adds another group.",
                    "Use it for role inheritance such as manager includes user.",
                    "Keep the chain simple so access is predictable.",
                ],
                [
                    {
                        "label": "Manager implies teacher",
                        "code": """<field name="implied_ids"
       eval="[(4, ref('group_training_teacher'))]"/>""",
                    },
                    {
                        "label": "Base user implied",
                        "code": """<field name="implied_ids"
       eval="[(4, ref('base.group_user'))]"/>""",
                    },
                ],
            ),
            _topic(
                "VS-26",
                "Groups on Menu",
                [
                    "The groups attribute hides a menu from other users.",
                    "It is a usability rule, not a full security rule.",
                    "Pair menu groups with access rights and record rules.",
                ],
                [
                    {
                        "label": "Teacher menu",
                        "code": """<menuitem id="training_menu_teacher"
          name="Teacher Tools"
          groups="training.group_training_teacher"/>""",
                    },
                    {
                        "label": "Manager menu",
                        "code": """<menuitem id="training_menu_reports"
          name="Reports"
          groups="training.group_training_manager"/>""",
                    },
                ],
            ),
        ],
    },
    {
        "section": 4,
        "title": "Access Rights, Record Rules, and Data",
        "topics": [
            _topic(
                "VS-27",
                "ir.model.access.csv",
                [
                    "CSV access files grant model-level permissions.",
                    "They control read, write, create, and delete.",
                    "Every business model usually needs at least read access.",
                ],
                [
                    {
                        "label": "CSV header",
                        "code": """id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink""",
                    },
                    {
                        "label": "Teacher access row",
                        "code": """access_course_teacher,course teacher,model_training_course,training.group_training_teacher,1,1,1,0""",
                    },
                ],
            ),
            _topic(
                "VS-28",
                "Access Rights XML",
                [
                    "Access rights can also be written as XML records.",
                    "XML is useful when values need references or conditions.",
                    "CSV is still the common choice for simple access matrices.",
                ],
                [
                    {
                        "label": "XML access record",
                        "code": """<record id="access_course_teacher_xml" model="ir.model.access">
    <field name="name">course teacher</field>
    <field name="model_id" ref="model_training_course"/>
    <field name="group_id" ref="group_training_teacher"/>
    <field name="perm_read" eval="1"/>
</record>""",
                    },
                    {
                        "label": "No delete access",
                        "code": """<field name="perm_unlink" eval="0"/>
<field name="perm_write" eval="1"/>""",
                    },
                ],
            ),
            _topic(
                "VS-29",
                "Record Rules",
                [
                    "Record rules filter which records a user can access.",
                    "They apply after model access rights.",
                    "Domains should be simple enough to audit.",
                ],
                [
                    {
                        "label": "Own records only",
                        "code": """<field name="domain_force">
    [('user_id', '=', user.id)]
</field>""",
                    },
                    {
                        "label": "Company records only",
                        "code": """<field name="domain_force">
    [('company_id', 'in', company_ids)]
</field>""",
                    },
                ],
            ),
            _topic(
                "VS-30",
                "Student Record Rule Example",
                [
                    "A student should usually see only their own enrollments.",
                    "The rule links records to the current user's partner.",
                    "Test with a real student account, not the administrator.",
                ],
                [
                    {
                        "label": "Student enrollment rule",
                        "code": """<record id="rule_student_own_enrollments" model="ir.rule">
    <field name="name">Students see own enrollments</field>
    <field name="model_id" ref="model_training_enrollment"/>
    <field name="domain_force">[('student_id.partner_id', '=', user.partner_id.id)]</field>
    <field name="groups" eval="[(4, ref('group_training_student'))]"/>
</record>""",
                    },
                    {
                        "label": "Model access row",
                        "code": """access_enrollment_student,enrollment student,model_training_enrollment,training.group_training_student,1,0,0,0""",
                    },
                ],
            ),
            _topic(
                "VS-31",
                "Teacher Record Rule Example",
                [
                    "A teacher may see courses they teach.",
                    "The rule should match the business relationship.",
                    "Give broader access only to manager groups.",
                ],
                [
                    {
                        "label": "Teacher course rule",
                        "code": """<record id="rule_teacher_own_courses" model="ir.rule">
    <field name="name">Teachers see own courses</field>
    <field name="model_id" ref="model_training_course"/>
    <field name="domain_force">[('teacher_id.user_id', '=', user.id)]</field>
    <field name="groups" eval="[(4, ref('group_training_teacher'))]"/>
</record>""",
                    },
                    {
                        "label": "Manager bypass group",
                        "code": """<field name="groups"
       eval="[(4, ref('group_training_manager'))]"/>""",
                    },
                ],
            ),
            _topic(
                "VS-32",
                "Groups on Actions",
                [
                    "Groups on an action limit who can launch it.",
                    "They help hide reports or tools from unrelated roles.",
                    "They do not replace model permissions.",
                ],
                [
                    {
                        "label": "Action with group",
                        "code": """<record id="action_training_report" model="ir.actions.act_window">
    <field name="name">Training Report</field>
    <field name="groups_id" eval="[(4, ref('group_training_manager'))]"/>
</record>""",
                    },
                    {
                        "label": "Server action group",
                        "code": """<field name="groups_id"
       eval="[(4, ref('base.group_system'))]"/>""",
                    },
                ],
            ),
            _topic(
                "VS-33",
                "Groups on Fields",
                [
                    "A field can be visible only to selected groups.",
                    "Use this for sensitive or advanced fields.",
                    "Server permissions still protect the underlying model.",
                ],
                [
                    {
                        "label": "View field group",
                        "code": """<field name="internal_note"
       groups="training.group_training_manager"/>""",
                    },
                    {
                        "label": "Python field group",
                        "code": """internal_note = fields.Text(
    groups="training.group_training_manager"
)""",
                    },
                ],
            ),
            _topic(
                "VS-34",
                "XML Data noupdate",
                [
                    "noupdate protects data from being overwritten on module update.",
                    "Use it for user-edited configuration records.",
                    "Do not use it for views you expect to upgrade.",
                ],
                [
                    {
                        "label": "Protected data",
                        "code": """<data noupdate="1">
    <record id="seq_training_course" model="ir.sequence">
        <field name="name">Course Sequence</field>
    </record>
</data>""",
                    },
                    {
                        "label": "Normal data",
                        "code": """<data>
    <record id="view_training_course_form" model="ir.ui.view"/>
</data>""",
                    },
                ],
            ),
            _topic(
                "VS-35",
                "CSV vs XML Data",
                [
                    "CSV is compact for many similar rows.",
                    "XML is better for nested records and references.",
                    "Choose the format that future maintainers can review.",
                ],
                [
                    {
                        "label": "CSV access row",
                        "code": """access_course_user,course user,model_training_course,base.group_user,1,0,0,0""",
                    },
                    {
                        "label": "XML menu record",
                        "code": """<menuitem id="training_menu_root"
          name="Training"
          sequence="20"/>""",
                    },
                ],
            ),
            _topic(
                "VS-36",
                "Sequence Basics",
                [
                    "ir.sequence generates readable document numbers.",
                    "Use a code that your model can call.",
                    "Keep prefixes short and meaningful.",
                ],
                [
                    {
                        "label": "Sequence XML",
                        "code": """<record id="seq_training_course" model="ir.sequence">
    <field name="name">Course</field>
    <field name="code">training.course</field>
    <field name="prefix">CRS/</field>
</record>""",
                    },
                    {
                        "label": "Python use",
                        "code": """vals["name"] = self.env["ir.sequence"].next_by_code(
    "training.course"
)""",
                    },
                ],
            ),
            _topic(
                "VS-37",
                "External IDs",
                [
                    "External IDs let XML and CSV records refer to each other.",
                    "They must stay stable across upgrades.",
                    "Use clear names with the module purpose included.",
                ],
                [
                    {
                        "label": "Reference a group",
                        "code": """<field name="group_id" ref="training.group_training_teacher"/>""",
                    },
                    {
                        "label": "Reference a model",
                        "code": """<field name="model_id" ref="model_training_course"/>""",
                    },
                ],
            ),
        ],
    },
    {
        "section": 5,
        "title": "Reports, Templates, and Automation",
        "topics": [
            _topic(
                "VS-38",
                "QWeb Report Basics",
                [
                    "QWeb reports render HTML that can become PDF.",
                    "A report action connects the model to the template.",
                    "Keep report templates simple and printable.",
                ],
                [
                    {
                        "label": "Report action",
                        "code": """<record id="action_report_course" model="ir.actions.report">
    <field name="name">Course Report</field>
    <field name="model">training.course</field>
    <field name="report_type">qweb-pdf</field>
    <field name="report_name">training.report_course</field>
</record>""",
                    },
                    {
                        "label": "Template shell",
                        "code": """<template id="report_course">
    <t t-call="web.html_container">
        <t t-foreach="docs" t-as="doc"/>
    </t>
</template>""",
                    },
                ],
            ),
            _topic(
                "VS-39",
                "t-field and t-out",
                [
                    "t-field renders an Odoo field with formatting.",
                    "t-out prints a computed expression safely.",
                    "Prefer t-field for dates, money, and relational fields.",
                ],
                [
                    {
                        "label": "Formatted field",
                        "code": """<span t-field="doc.start_date"/>""",
                    },
                    {
                        "label": "Expression output",
                        "code": """<span t-out="doc.name.upper()"/>""",
                    },
                ],
            ),
            _topic(
                "VS-40",
                "QWeb If",
                [
                    "t-if conditionally shows a piece of template.",
                    "Use it for optional values and simple branches.",
                    "Keep business decisions in Python when they become complex.",
                ],
                [
                    {
                        "label": "Optional note",
                        "code": """<p t-if="doc.note">
    <span t-field="doc.note"/>
</p>""",
                    },
                    {
                        "label": "State message",
                        "code": """<strong t-if="doc.state == 'done'">Completed</strong>""",
                    },
                ],
            ),
            _topic(
                "VS-41",
                "QWeb Foreach",
                [
                    "t-foreach repeats markup for each record or value.",
                    "Use t-as to name the current item.",
                    "Keep loop rows small for readable reports.",
                ],
                [
                    {
                        "label": "Loop lines",
                        "code": """<tr t-foreach="doc.line_ids" t-as="line">
    <td><span t-field="line.name"/></td>
</tr>""",
                    },
                    {
                        "label": "Loop numbers",
                        "code": """<li t-foreach="[1, 2, 3]" t-as="number">
    <span t-out="number"/>
</li>""",
                    },
                ],
            ),
            _topic(
                "VS-42",
                "Paper Format",
                [
                    "Paper formats define page size and margins.",
                    "Attach one when a report needs special layout.",
                    "Test printed output, not only the browser preview.",
                ],
                [
                    {
                        "label": "A4 format",
                        "code": """<record id="paperformat_training" model="report.paperformat">
    <field name="name">Training A4</field>
    <field name="format">A4</field>
    <field name="margin_top">20</field>
</record>""",
                    },
                    {
                        "label": "Attach to report",
                        "code": """<field name="paperformat_id"
       ref="paperformat_training"/>""",
                    },
                ],
            ),
            _topic(
                "VS-43",
                "Email Template",
                [
                    "Email templates generate messages from records.",
                    "Use placeholders for record-specific values.",
                    "Keep the subject clear and searchable.",
                ],
                [
                    {
                        "label": "Template record",
                        "code": """<record id="email_course_confirmed" model="mail.template">
    <field name="name">Course Confirmed</field>
    <field name="model_id" ref="model_training_course"/>
    <field name="subject">Course {{ object.name }} confirmed</field>
</record>""",
                    },
                    {
                        "label": "Body expression",
                        "code": """<field name="body_html" type="html">
    <p>Hello <t t-out="object.teacher_id.name"/>.</p>
</field>""",
                    },
                ],
            ),
            _topic(
                "VS-44",
                "Server Action",
                [
                    "A server action runs server-side logic from the UI or automation.",
                    "Use it for small administrative actions.",
                    "Move complex logic into model methods.",
                ],
                [
                    {
                        "label": "Call Python method",
                        "code": """<record id="server_action_confirm_courses" model="ir.actions.server">
    <field name="name">Confirm Courses</field>
    <field name="model_id" ref="model_training_course"/>
    <field name="state">code</field>
    <field name="code">records.action_confirm()</field>
</record>""",
                    },
                    {
                        "label": "Bind to model",
                        "code": """<field name="binding_model_id" ref="model_training_course"/>
<field name="binding_view_types">list,form</field>""",
                    },
                ],
            ),
            _topic(
                "VS-45",
                "Header Buttons and Security",
                [
                    "Header buttons should match the record workflow.",
                    "Use groups to hide actions from users who cannot run them.",
                    "The Python method must still check important rules.",
                ],
                [
                    {
                        "label": "Manager-only button",
                        "code": """<button name="action_approve"
        type="object"
        string="Approve"
        groups="training.group_training_manager"/>""",
                    },
                    {
                        "label": "State-based button",
                        "code": """<button name="action_done"
        type="object"
        string="Done"
        invisible="state != 'confirmed'"/>""",
                    },
                ],
            ),
            _topic(
                "VS-46",
                "Manifest Data Order",
                [
                    "Data files load in the order listed in the manifest.",
                    "Load security before views that use security groups.",
                    "Load reports after their templates and dependencies exist.",
                ],
                [
                    {
                        "label": "Manifest order",
                        "code": """"data": [
    "security/groups.xml",
    "security/ir.model.access.csv",
    "views/course_views.xml",
]""",
                    },
                    {
                        "label": "Report files",
                        "code": """"data": [
    "report/course_templates.xml",
    "report/course_reports.xml",
]""",
                    },
                ],
            ),
        ],
    },
]

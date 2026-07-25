#!/usr/bin/env python3
"""Atomic beginner-friendly slides for Odoo OWL, POS, and external APIs."""


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
        "title": "OWL Component Basics",
        "topics": [
            _topic(
                "OWL-01",
                "OWL Intro",
                [
                    "OWL is Odoo's JavaScript component framework.",
                    "Components combine state, behavior, and templates.",
                    "Change state instead of directly changing the DOM.",
                ],
                [
                    {
                        "label": "Component idea",
                        "code": """Component class + XML template + optional services""",
                    },
                    {
                        "label": "Small import",
                        "code": """import { Component } from "@odoo/owl";""",
                    },
                ],
            ),
            _topic(
                "OWL-02",
                "Component Structure",
                [
                    "A component class owns behavior.",
                    "A template owns the displayed markup.",
                    "The setup method prepares state and services.",
                ],
                [
                    {
                        "label": "Component class",
                        "code": """/** @odoo-module **/
import { Component } from "@odoo/owl";

export class TrainingCard extends Component {
    static template = "training.TrainingCard";
}""",
                    },
                    {
                        "label": "Template name",
                        "code": """<t t-name="training.TrainingCard">
    <div class="o_training_card">Training</div>
</t>""",
                    },
                ],
            ),
            _topic(
                "OWL-03",
                "setup Method",
                [
                    "setup runs when the component is created.",
                    "Use it to initialize hooks and services.",
                    "Keep heavy work out of setup when possible.",
                ],
                [
                    {
                        "label": "Use a service",
                        "code": """setup() {
    this.notification = useService("notification");
}""",
                    },
                    {
                        "label": "Prepare local state",
                        "code": """setup() {
    this.state = useState({ ready: false });
}""",
                    },
                ],
            ),
            _topic(
                "OWL-04",
                "useState",
                [
                    "useState creates reactive local state.",
                    "Changing state causes the component to rerender.",
                    "Use it for values owned by this component.",
                ],
                [
                    {
                        "label": "Counter state",
                        "code": """this.state = useState({ count: 0 });
this.state.count += 1;""",
                    },
                    {
                        "label": "Display state",
                        "code": """<span t-out="state.count"/>""",
                    },
                ],
            ),
            _topic(
                "OWL-05",
                "Props",
                [
                    "Props pass data from a parent to a child component.",
                    "The child should treat props as input.",
                    "Use props for reusable display components.",
                ],
                [
                    {
                        "label": "Parent passes prop",
                        "code": """<TrainingBadge label="'Ready'"/>""",
                    },
                    {
                        "label": "Child reads prop",
                        "code": """<span t-out="props.label"/>""",
                    },
                ],
            ),
            _topic(
                "OWL-06",
                "t-if",
                [
                    "t-if shows markup only when a condition is true.",
                    "Use it for simple visible or hidden blocks.",
                    "Keep complex decisions in JavaScript methods.",
                ],
                [
                    {
                        "label": "Show message",
                        "code": """<div t-if="state.ready">Ready</div>""",
                    },
                    {
                        "label": "Show warning",
                        "code": """<span t-if="props.total === 0">No lines</span>""",
                    },
                ],
            ),
            _topic(
                "OWL-07",
                "t-foreach",
                [
                    "t-foreach repeats markup for a list.",
                    "Always provide a stable t-key.",
                    "Use clear variable names with t-as.",
                ],
                [
                    {
                        "label": "Loop records",
                        "code": """<li t-foreach="state.records" t-as="record" t-key="record.id">
    <span t-out="record.name"/>
</li>""",
                    },
                    {
                        "label": "Loop simple values",
                        "code": """<span t-foreach="props.tags" t-as="tag" t-key="tag">
    <t t-out="tag"/>
</span>""",
                    },
                ],
            ),
            _topic(
                "OWL-08",
                "t-model",
                [
                    "t-model binds an input to component state.",
                    "It is useful for simple forms.",
                    "Validate important data on the server too.",
                ],
                [
                    {
                        "label": "Text input",
                        "code": """<input t-model="state.name" placeholder="Course name"/>""",
                    },
                    {
                        "label": "Checkbox input",
                        "code": """<input type="checkbox" t-model="state.active"/>""",
                    },
                ],
            ),
            _topic(
                "OWL-09",
                "Custom Field Widget Idea",
                [
                    "A field widget customizes how one field appears.",
                    "Register it in the field registry.",
                    "Start with display behavior before adding editing.",
                ],
                [
                    {
                        "label": "Registry entry",
                        "code": """registry.category("fields").add("training_badge", {
    component: TrainingBadgeField,
});""",
                    },
                    {
                        "label": "Use in XML view",
                        "code": """<field name="state" widget="training_badge"/>""",
                    },
                ],
            ),
            _topic(
                "OWL-10",
                "patch Function",
                [
                    "patch extends existing Odoo JavaScript behavior.",
                    "Keep patches narrow and named by purpose.",
                    "Prefer registries when a clean extension point exists.",
                ],
                [
                    {
                        "label": "Patch prototype",
                        "code": """import { patch } from "@web/core/utils/patch";

patch(SomeComponent.prototype, {
    get trainingLabel() {
        return "Training";
    },
});""",
                    },
                    {
                        "label": "Call original method",
                        "code": """patch(SomeComponent.prototype, {
    setup() {
        super.setup(...arguments);
        this.trainingReady = true;
    },
});""",
                    },
                ],
            ),
            _topic(
                "OWL-11",
                "RPC Service",
                [
                    "The rpc service calls server routes from JavaScript.",
                    "Use it at workflow edges, such as save or refresh.",
                    "Show clear errors when a call fails.",
                ],
                [
                    {
                        "label": "Get rpc service",
                        "code": """setup() {
    this.rpc = useService("rpc");
}""",
                    },
                    {
                        "label": "Call a route",
                        "code": """const result = await this.rpc("/training/course/count", {
    teacher_id: this.props.teacherId,
});""",
                    },
                ],
            ),
            _topic(
                "OWL-12",
                "Notifications",
                [
                    "Notifications give immediate feedback to users.",
                    "Use success messages for completed actions.",
                    "Use danger messages for failures users can understand.",
                ],
                [
                    {
                        "label": "Success notification",
                        "code": """this.notification.add("Course saved", {
    type: "success",
});""",
                    },
                    {
                        "label": "Warning notification",
                        "code": """this.notification.add("Select a customer first", {
    type: "warning",
});""",
                    },
                ],
            ),
        ],
    },
    {
        "section": 2,
        "title": "POS Customization",
        "topics": [
            _topic(
                "OWL-13",
                "POS Custom Button",
                [
                    "A POS button adds a cashier action to the screen.",
                    "Register it through the POS component system.",
                    "Keep the button label short for touch screens.",
                ],
                [
                    {
                        "label": "Button template",
                        "code": """<t t-name="training.PosButton">
    <button class="control-button">Training</button>
</t>""",
                    },
                    {
                        "label": "Button class",
                        "code": """export class TrainingPosButton extends Component {
    static template = "training.PosButton";
}""",
                    },
                ],
            ),
            _topic(
                "OWL-14",
                "POS Click Handler",
                [
                    "A click handler reacts to cashier input.",
                    "Keep the handler small and easy to test.",
                    "Call a method instead of writing logic in the template.",
                ],
                [
                    {
                        "label": "Template click",
                        "code": """<button t-on-click="onClick">Training</button>""",
                    },
                    {
                        "label": "Handler method",
                        "code": """onClick() {
    this.notification.add("Button clicked");
}""",
                    },
                ],
            ),
            _topic(
                "OWL-15",
                "Hide POS Button",
                [
                    "Hide a button when the action is not useful.",
                    "Use a condition that matches the cashier workflow.",
                    "Security still belongs on the server.",
                ],
                [
                    {
                        "label": "Template condition",
                        "code": """<button t-if="shouldShowButton" t-on-click="onClick">
    Training
</button>""",
                    },
                    {
                        "label": "Getter condition",
                        "code": """get shouldShowButton() {
    return this.pos.get_order()?.get_orderlines().length > 0;
}""",
                    },
                ],
            ),
            _topic(
                "OWL-16",
                "POS Popup",
                [
                    "A popup asks for confirmation or extra input.",
                    "Use it when the cashier must make a clear choice.",
                    "Avoid popups for routine actions that need speed.",
                ],
                [
                    {
                        "label": "Confirmation call",
                        "code": """await this.dialog.add(ConfirmationDialog, {
    title: "Clear order",
    body: "Remove all order lines?",
});""",
                    },
                    {
                        "label": "Popup button",
                        "code": """<button t-on-click="confirm">Confirm</button>
<button t-on-click="cancel">Cancel</button>""",
                    },
                ],
            ),
            _topic(
                "OWL-17",
                "Translate JS String",
                [
                    "Use _t for text shown to users.",
                    "Translated strings make POS customizations production ready.",
                    "Do not translate technical keys or route names.",
                ],
                [
                    {
                        "label": "Import _t",
                        "code": """import { _t } from "@web/core/l10n/translation";""",
                    },
                    {
                        "label": "Translated label",
                        "code": """this.notification.add(_t("Order cleared"), {
    type: "success",
});""",
                    },
                ],
            ),
            _topic(
                "OWL-18",
                "POS RPC",
                [
                    "POS can call the server for live data.",
                    "Keep calls fast because cashiers are waiting.",
                    "Handle offline or network failure paths.",
                ],
                [
                    {
                        "label": "Server call",
                        "code": """const loyalty = await this.rpc("/pos/loyalty/balance", {
    partner_id: partner.id,
});""",
                    },
                    {
                        "label": "Route response",
                        "code": """return {
    "points": partner.loyalty_points,
    "name": partner.name,
}""",
                    },
                ],
            ),
            _topic(
                "OWL-19",
                "Clear Order Lines",
                [
                    "Clearing an order removes all current order lines.",
                    "Ask for confirmation because the action is destructive.",
                    "Use POS order methods instead of editing arrays directly.",
                ],
                [
                    {
                        "label": "Get current order",
                        "code": """const order = this.pos.get_order();
const lines = [...order.get_orderlines()];""",
                    },
                    {
                        "label": "Remove lines",
                        "code": """for (const line of lines) {
    order.removeOrderline(line);
}""",
                    },
                ],
            ),
            _topic(
                "OWL-20",
                "POS Assets",
                [
                    "POS JavaScript and XML must be loaded in POS assets.",
                    "Add only the files the POS really needs.",
                    "Restart and update assets when files do not appear.",
                ],
                [
                    {
                        "label": "Manifest assets",
                        "code": """"point_of_sale._assets_pos": [
    "training/static/src/pos/**/*",
]""",
                    },
                    {
                        "label": "XML template file",
                        "code": """<templates xml:space="preserve">
    <t t-name="training.PosButton"/>
</templates>""",
                    },
                ],
            ),
        ],
    },
    {
        "section": 3,
        "title": "XML-RPC and Integration APIs",
        "topics": [
            _topic(
                "OWL-21",
                "XML-RPC Auth",
                [
                    "XML-RPC clients authenticate before calling models.",
                    "The result is a user id for later calls.",
                    "Use an API-specific user when possible.",
                ],
                [
                    {
                        "label": "Python authenticate",
                        "code": """uid = common.authenticate(db, username, password, {})""",
                    },
                    {
                        "label": "Connection objects",
                        "code": """common = xmlrpc.client.ServerProxy(url + "/xmlrpc/2/common")
models = xmlrpc.client.ServerProxy(url + "/xmlrpc/2/object")""",
                    },
                ],
            ),
            _topic(
                "OWL-22",
                "XML-RPC search_read",
                [
                    "search_read finds records and returns selected fields.",
                    "It is ideal for simple read integrations.",
                    "Always request only the fields you need.",
                ],
                [
                    {
                        "label": "Read partners",
                        "code": """records = models.execute_kw(
    db, uid, password, "res.partner", "search_read",
    [[["is_company", "=", True]]],
    {"fields": ["name", "email"], "limit": 10},
)""",
                    },
                    {
                        "label": "Read courses",
                        "code": """courses = models.execute_kw(
    db, uid, password, "training.course", "search_read",
    [[["state", "=", "confirmed"]]],
)""",
                    },
                ],
            ),
            _topic(
                "OWL-23",
                "XML-RPC create",
                [
                    "create inserts a new record through the ORM.",
                    "Required fields must be present.",
                    "Server constraints and access rights still apply.",
                ],
                [
                    {
                        "label": "Create partner",
                        "code": """partner_id = models.execute_kw(
    db, uid, password, "res.partner", "create",
    [{"name": "API Customer", "email": "api@example.com"}],
)""",
                    },
                    {
                        "label": "Create course",
                        "code": """course_id = models.execute_kw(
    db, uid, password, "training.course", "create",
    [{"name": "Beginner Odoo"}],
)""",
                    },
                ],
            ),
            _topic(
                "OWL-24",
                "XML-RPC write",
                [
                    "write updates existing records.",
                    "Pass a list of ids and a values dictionary.",
                    "Check the returned boolean for success.",
                ],
                [
                    {
                        "label": "Update email",
                        "code": """ok = models.execute_kw(
    db, uid, password, "res.partner", "write",
    [[partner_id], {"email": "new@example.com"}],
)""",
                    },
                    {
                        "label": "Archive record",
                        "code": """models.execute_kw(
    db, uid, password, "training.course", "write",
    [[course_id], {"active": False}],
)""",
                    },
                ],
            ),
            _topic(
                "OWL-25",
                "XML-RPC unlink",
                [
                    "unlink deletes records when access rights allow it.",
                    "Prefer archiving business records when history matters.",
                    "Use unlink carefully in integrations.",
                ],
                [
                    {
                        "label": "Delete one record",
                        "code": """models.execute_kw(
    db, uid, password, "training.course", "unlink",
    [[course_id]],
)""",
                    },
                    {
                        "label": "Archive instead",
                        "code": """models.execute_kw(
    db, uid, password, "training.course", "write",
    [[course_id], {"active": False}],
)""",
                    },
                ],
            ),
            _topic(
                "OWL-26",
                "Postman Auth Idea",
                [
                    "Postman can test authentication and model calls.",
                    "Keep database, username, and password in variables.",
                    "Never store production passwords in shared collections.",
                ],
                [
                    {
                        "label": "Variables",
                        "code": """url = https://odoo.example.com
db = prod_db
username = api@example.com""",
                    },
                    {
                        "label": "Auth body idea",
                        "code": """{
  "service": "common",
  "method": "authenticate",
  "args": ["{{db}}", "{{username}}", "{{password}}", {}]
}""",
                    },
                ],
            ),
            _topic(
                "OWL-27",
                "Integration User Least Privilege",
                [
                    "An integration user should have only needed access.",
                    "Use groups and record rules like any other user.",
                    "Avoid using administrator credentials for APIs.",
                ],
                [
                    {
                        "label": "Dedicated login",
                        "code": """api.training@example.com""",
                    },
                    {
                        "label": "Limited group",
                        "code": """<field name="groups_id"
       eval="[(4, ref('training.group_training_api'))]"/>""",
                    },
                ],
            ),
            _topic(
                "OWL-28",
                "API Domains",
                [
                    "Domains filter records in API calls.",
                    "They use the same basic syntax as Odoo search views.",
                    "Keep domains explicit so integrations are predictable.",
                ],
                [
                    {
                        "label": "Active customers",
                        "code": """[["customer_rank", ">", 0], ["active", "=", True]]""",
                    },
                    {
                        "label": "Confirmed courses",
                        "code": """[["state", "=", "confirmed"], ["start_date", ">=", "2026-01-01"]]""",
                    },
                ],
            ),
            _topic(
                "OWL-29",
                "API Field Selection",
                [
                    "Requesting fewer fields makes API calls faster.",
                    "It also avoids exposing data the integration does not need.",
                    "Document which fields each integration consumes.",
                ],
                [
                    {
                        "label": "Partner fields",
                        "code": """{"fields": ["name", "email", "phone"]}""",
                    },
                    {
                        "label": "Course fields",
                        "code": """{"fields": ["name", "state", "teacher_id"]}""",
                    },
                ],
            ),
            _topic(
                "OWL-30",
                "API Error Handling",
                [
                    "APIs can fail because of access, validation, or network issues.",
                    "Log enough context to retry safely.",
                    "Do not ignore failed writes.",
                ],
                [
                    {
                        "label": "Try and log",
                        "code": """try:
    call_odoo()
except Exception as exc:
    logger.exception("Odoo API call failed: %s", exc)""",
                    },
                    {
                        "label": "Check result",
                        "code": """if not ok:
    raise RuntimeError("Odoo write did not succeed")""",
                    },
                ],
            ),
            _topic(
                "OWL-31",
                "API Pagination",
                [
                    "Large reads should use limit and offset.",
                    "Process records in batches.",
                    "Stable ordering helps prevent skipped records.",
                ],
                [
                    {
                        "label": "Batch options",
                        "code": """{"limit": 100, "offset": 0, "order": "id"}""",
                    },
                    {
                        "label": "Next batch",
                        "code": """offset += limit
records = search_read(domain, fields, offset=offset)""",
                    },
                ],
            ),
            _topic(
                "OWL-32",
                "API Create vs Update",
                [
                    "Decide how the external system identifies a record.",
                    "Search first when updating an existing business object.",
                    "Use external IDs or unique keys when available.",
                ],
                [
                    {
                        "label": "Find by reference",
                        "code": """domain = [["x_external_ref", "=", external_ref]]""",
                    },
                    {
                        "label": "Create or write idea",
                        "code": """if record_id:
    write(record_id, values)
else:
    create(values)""",
                    },
                ],
            ),
            _topic(
                "OWL-33",
                "API Test Data Cleanup",
                [
                    "Test integrations with safe sample records.",
                    "Mark test data clearly.",
                    "Clean up or archive test records after verification.",
                ],
                [
                    {
                        "label": "Test marker",
                        "code": """{"name": "API TEST Customer", "x_test_record": True}""",
                    },
                    {
                        "label": "Cleanup domain",
                        "code": """[["x_test_record", "=", True], ["create_uid", "=", uid]]""",
                    },
                ],
            ),
        ],
    },
]

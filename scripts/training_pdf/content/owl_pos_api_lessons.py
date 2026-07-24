#!/usr/bin/env python3
"""OWL, POS, and API lessons for the Odoo training PDF generator."""


def _explanation(title, theme, design, implementation, verification, production):
    return [
        (
            f"{title} belongs to the client-side layer where user intent, browser state, "
            f"and Odoo services meet. {theme} Senior developers treat JavaScript changes "
            "as product behavior, not decoration, because a small patch can alter every "
            "user session that loads the bundle."
        ),
        (
            f"The design starts with ownership of state and boundaries. {design} Keep "
            "components small, pass data through props where possible, and call services "
            "at clear workflow edges instead of scattering RPC calls through templates."
        ),
        (
            f"Implementation should follow Odoo's asset, registry, service, and template "
            f"patterns. {implementation} Favor explicit imports, named templates, stable "
            "registry keys, and patches that are narrow enough to survive upstream changes."
        ),
        (
            f"Verification requires more than refreshing the page once. {verification} "
            "Test with production-like data, translated labels, slow network behavior, "
            "and users with realistic access rights so browser success does not hide "
            "server-side failures."
        ),
        (
            f"In production, {title.lower()} decisions affect performance, offline "
            f"behavior, cache invalidation, and upgrade risk. {production} Keep examples "
            "traceable to business needs, document assumptions near extension points, "
            "and prefer framework services over ad hoc browser globals."
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
        "section": "owl",
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
        "W01",
        "OWL Architecture and Reactive Rendering",
        [
            "Explain how OWL components render from reactive state.",
            "Identify the role of services, registries, and templates.",
            "Avoid direct DOM manipulation in normal component logic.",
        ],
        "OWL is Odoo's component framework and provides the reactive mental model behind many modern web client features.",
        "Decide which component owns state, which services provide data, and which children only render props.",
        "Use Component classes, static templates, setup methods, hooks, and the registry rather than creating global scripts.",
        "Inspect rerenders, service calls, and asset loading in browser developer tools after every meaningful change.",
        "A maintainable OWL customization feels native because it composes with the framework instead of fighting it.",
        [
            "Reactive state changes trigger rerendering.",
            "Templates describe UI; components own behavior.",
            "Services centralize shared capabilities such as rpc and notifications.",
            "Registries let addons extend the web client.",
            "Direct DOM writes are a last resort.",
        ],
        [
            {
                "title": "Small reactive counter component",
                "code": '''/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class TrainingCounter extends Component {
    static template = "training.TrainingCounter";

    setup() {
        this.state = useState({ value: 0 });
    }

    increment() {
        this.state.value += 1;
    }
}

registry.category("actions").add("training_counter", TrainingCounter);''',
                "explain": "The state object is reactive, so incrementing value rerenders the template that displays it.",
            }
        ],
        [
            "Changing random DOM nodes instead of changing component state.",
            "Putting global variables in asset files for shared state.",
            "Forgetting to register the component under the correct registry category.",
            "Treating OWL like jQuery with templates attached.",
        ],
        "Create a small client action that increments a counter and logs when the component rerenders.",
        [
            {
                "kind": "items",
                "title": "OWL building blocks",
                "items": ["Component", "Template", "State", "Services", "Registry"],
            }
        ],
    ),
    _lesson(
        "W02",
        "Component Structure and Lifecycle Hooks",
        [
            "Organize component files and templates cleanly.",
            "Use lifecycle hooks for setup and cleanup.",
            "Keep asynchronous loading predictable.",
        ],
        "Component structure matters because Odoo assets are bundled, upgraded, translated, and extended by other modules.",
        "Keep JavaScript behavior, XML templates, and SCSS names aligned so another developer can find the complete feature quickly.",
        "Use setup for hooks, onWillStart for initial asynchronous work, onMounted for browser-only integration, and onWillUnmount for cleanup.",
        "Test navigation away from the component while requests are pending and verify that timers or listeners do not leak.",
        "Lifecycle discipline prevents slow memory leaks and race conditions that otherwise appear only during long back-office sessions.",
        [
            "setup is the main hook registration point.",
            "onWillStart can await data before first render.",
            "onMounted is safe for DOM-dependent integrations.",
            "onWillUnmount cleans up listeners and timers.",
            "Asset paths should mirror feature names.",
        ],
        [
            {
                "title": "Lifecycle with cleanup",
                "code": '''/** @odoo-module **/

import { Component, onMounted, onWillStart, onWillUnmount, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class CourseDashboard extends Component {
    static template = "training.CourseDashboard";

    setup() {
        this.orm = useService("orm");
        this.state = useState({ stats: null });
        let timer;

        onWillStart(async () => {
            this.state.stats = await this.orm.call("training.course", "dashboard_stats", []);
        });
        onMounted(() => {
            timer = setInterval(() => this.refresh(), 60000);
        });
        onWillUnmount(() => clearInterval(timer));
    }

    async refresh() {
        this.state.stats = await this.orm.call("training.course", "dashboard_stats", []);
    }
}''',
                "explain": "The component loads initial data before rendering and removes its refresh timer when it is destroyed.",
            }
        ],
        [
            "Starting intervals without clearing them.",
            "Calling browser APIs before the component is mounted.",
            "Loading data in the constructor instead of setup hooks.",
            "Ignoring navigation races during slow RPC responses.",
        ],
        "Build a dashboard component that loads statistics before render and refreshes every minute without leaking timers.",
    ),
    _lesson(
        "W03",
        "useState, useRef, Events, and Props",
        [
            "Use state for mutable component data.",
            "Use refs for specific DOM elements.",
            "Pass behavior through events and props cleanly.",
        ],
        "OWL gives developers clear tools for local state, DOM references, parent-to-child data, and child-to-parent communication.",
        "Before writing code, decide whether a value is owned by the component, passed by the parent, derived from services, or simply stored in the DOM.",
        "Use useState for reactive values, useRef for controlled DOM access, props for inputs, and callback props or triggered events for outputs.",
        "Verify that a child component still works when props change and that refs are not accessed before mount.",
        "Correct ownership keeps components reusable and avoids the common trap of several components mutating the same data without a single source of truth.",
        [
            "State is mutable and reactive inside the component.",
            "Props are inputs from the parent.",
            "Refs point to DOM nodes after render.",
            "Events should describe user intent.",
            "Derived values should not be duplicated unnecessarily.",
        ],
        [
            {
                "title": "Filter input with ref and callback prop",
                "code": '''/** @odoo-module **/

import { Component, useRef, useState } from "@odoo/owl";

export class CourseFilter extends Component {
    static template = "training.CourseFilter";
    static props = { onApply: Function };

    setup() {
        this.state = useState({ text: "" });
        this.inputRef = useRef("filterInput");
    }

    apply() {
        this.props.onApply(this.state.text.trim());
        this.inputRef.el.focus();
    }
}''',
                "explain": "The component owns the input text, calls the parent callback when applied, and uses a ref only to restore focus.",
            }
        ],
        [
            "Mutating props directly.",
            "Using refs as general state storage.",
            "Passing large objects when a small prop would do.",
            "Creating event names that describe implementation instead of intent.",
        ],
        "Create a child filter component that receives an onApply callback and prove it remains reusable in two parent components.",
    ),
    _lesson(
        "W04",
        "QWeb XML Directives: t-if, t-foreach, and t-model",
        [
            "Render conditional content in OWL XML templates.",
            "Loop over arrays safely with keys.",
            "Bind form controls with t-model where appropriate.",
        ],
        "OWL templates use QWeb-style XML directives to describe dynamic browser UI.",
        "Keep templates declarative: conditions should select presentation, loops should render prepared lists, and form bindings should update local state.",
        "Use t-if for conditions, t-foreach with t-as and t-key for repeatable data, and t-model for simple two-way form input binding.",
        "Test empty arrays, duplicate labels, and rapid typing because template mistakes often appear as unstable DOM updates.",
        "Good templates are readable enough that a reviewer can understand the UI states without opening the JavaScript file first.",
        [
            "Every t-foreach should have a stable t-key.",
            "t-if removes or inserts template branches.",
            "t-model is useful for simple local form values.",
            "Complex formatting belongs in component methods or getters.",
            "XML must remain valid and escaped.",
        ],
        [
            {
                "title": "OWL template directives",
                "code": '''<templates xml:space="preserve">
    <t t-name="training.CourseList">
        <input t-ref="filterInput" t-model="state.query" placeholder="Search courses"/>
        <p t-if="!state.courses.length">No courses found.</p>
        <ul>
            <li t-foreach="state.courses" t-as="course" t-key="course.id">
                <span t-esc="course.name"/>
                <span class="text-muted" t-esc="course.teacher"/>
            </li>
        </ul>
    </t>
</templates>''',
                "explain": "The template handles search input, empty state, and stable list rendering with a key per course.",
            }
        ],
        [
            "Looping without t-key.",
            "Putting business queries inside template expressions.",
            "Forgetting XML escaping for comparison operators.",
            "Using t-model against props instead of local state.",
        ],
        "Write a template that lists courses, shows an empty state, and filters from a t-model input stored in component state.",
    ),
    _lesson(
        "W05",
        "Custom Form Field Widgets",
        [
            "Register a field widget in the web client.",
            "Respect standard field props and update behavior.",
            "Use widgets to improve editing without changing model semantics.",
        ],
        "A custom field widget changes how one field is displayed or edited while keeping the model field as the source of truth.",
        "Use a widget when the default field component is correct semantically but not expressive enough for the workflow.",
        "Register the widget in the fields registry, accept standard props, and call props.update when the user changes the value.",
        "Test readonly mode, required fields, invalid values, and list/form contexts because widgets may be reused outside the original screen.",
        "Production widgets should be boringly compatible with Odoo's form renderer: they should not bypass validation, dirty state, or onchange behavior.",
        [
            "Field widgets are registered in the fields registry.",
            "props.value is the current field value.",
            "props.update writes a new value to the record buffer.",
            "Support readonly mode explicitly.",
            "Widgets should not own persistent business state.",
        ],
        [
            {
                "title": "Rating field widget",
                "code": '''/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class RatingField extends Component {
    static template = "training.RatingField";
    static props = { ...standardFieldProps };

    setRating(value) {
        if (!this.props.readonly) {
            this.props.update(value);
        }
    }
}

registry.category("fields").add("training_rating", {
    component: RatingField,
    supportedTypes: ["integer", "float"],
});''',
                "explain": "The widget follows the standard field contract and updates the form record through props.update.",
            }
        ],
        [
            "Writing directly to the server from the widget instead of using props.update.",
            "Ignoring readonly mode.",
            "Registering a widget with a generic key likely to collide.",
            "Supporting field types the component cannot handle.",
        ],
        "Create a five-star rating widget for an integer field and test it in readonly and editable form modes.",
    ),
    _lesson(
        "W06",
        "Overriding JavaScript Components with the Patch Utility",
        [
            "Patch existing components narrowly.",
            "Call super behavior when extending methods.",
            "Minimize upgrade risk when overriding Odoo web code.",
        ],
        "The patch utility is the preferred way to adjust existing JavaScript classes when registries or props are not enough.",
        "Patch only the method or getter you need, and first ask whether a registry extension, service, or template inheritance would be safer.",
        "Import the target class and patch it with a small object that adds or extends behavior while preserving upstream logic where required.",
        "Test against the exact Odoo version and read upstream changes during upgrades because patches depend on private implementation details more than normal extensions.",
        "A good patch is almost invisible: one responsibility, no global side effects, and an easy removal path when upstream gains the needed hook.",
        [
            "Patch is powerful and should be narrow.",
            "Prefer public extension points first.",
            "Call super when preserving behavior matters.",
            "Version upgrades can break patches.",
            "Name modules and methods clearly for traceability.",
        ],
        [
            {
                "title": "Patch a method to add a training flag",
                "code": '''/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";

patch(FormController.prototype, {
    async saveButtonClicked(params = {}) {
        this.env.bus.trigger("training:before-form-save", {
            resModel: this.props.resModel,
        });
        return super.saveButtonClicked(params);
    },
});''',
                "explain": "The patch adds a small event before save while delegating the actual save behavior to the original controller.",
            }
        ],
        [
            "Patching large methods by copying upstream source.",
            "Forgetting to call super when extending behavior.",
            "Using patch when a registry extension exists.",
            "Not reviewing patches during every major upgrade.",
        ],
        "Patch a small controller method to emit a custom event, then remove the patch and confirm the rest of the feature is isolated.",
    ),
    _lesson(
        "W07",
        "RPC and ORM Services",
        [
            "Use orm and rpc services appropriately.",
            "Call model methods from OWL components.",
            "Handle loading and errors cleanly.",
        ],
        "Odoo provides services so client code does not need to know every HTTP detail or session convention.",
        "Use orm for model operations and rpc for custom endpoints or lower-level calls where the ORM service does not fit.",
        "Inject services with useService, keep request code in explicit methods, and store loading or error state so the UI communicates what is happening.",
        "Test server access rights, record rules, network failures, and repeated clicks because the browser can make invalid calls faster than a human can diagnose them.",
        "Service-based code is easier to migrate because authentication, context, and error handling stay aligned with the framework.",
        [
            "useService injects framework services.",
            "orm.call invokes model methods.",
            "rpc is useful for custom routes.",
            "Always represent loading and failure states.",
            "Server methods must still validate access.",
        ],
        [
            {
                "title": "Load dashboard data through orm",
                "code": '''/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class TrainingDashboard extends Component {
    static template = "training.TrainingDashboard";

    setup() {
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.state = useState({ loading: false, stats: {} });
    }

    async load() {
        this.state.loading = true;
        try {
            this.state.stats = await this.orm.call("training.course", "dashboard_stats", []);
        } catch (error) {
            this.notification.add("Could not load dashboard data.", { type: "danger" });
        } finally {
            this.state.loading = false;
        }
    }
}''',
                "explain": "The component uses framework services and exposes loading and error feedback to users.",
            }
        ],
        [
            "Calling fetch directly for ORM work.",
            "Ignoring errors and leaving stale UI state.",
            "Trusting client parameters without server validation.",
            "Making one RPC call per row when a batched method would do.",
        ],
        "Replace a direct fetch call with orm.call and add a loading indicator plus a notification on failure.",
    ),
    _lesson(
        "W08",
        "Custom Kanban and Dashboard OWL Views",
        [
            "Design a dashboard as a client action or custom view.",
            "Register components in the correct registry.",
            "Keep dashboard data server-side and aggregated.",
        ],
        "Dashboards should present decisions, exceptions, and navigation paths rather than becoming a second database browser.",
        "Choose a client action for a standalone dashboard and a custom view only when it truly replaces how users inspect a model.",
        "Register the component, define an action tag, load aggregated data from model methods, and keep cards reusable where possible.",
        "Verify performance on realistic data because dashboards are often opened by managers every morning and must not run expensive per-card queries.",
        "A production dashboard is an operations surface: it needs clear ownership, stable metrics, and failure behavior that does not block the rest of Odoo.",
        [
            "Client actions are good for standalone dashboards.",
            "Custom views are deeper integrations with the view system.",
            "Aggregate on the server, render on the client.",
            "Use action tags and registries consistently.",
            "Dashboard cards should link to filtered records.",
        ],
        [
            {
                "title": "Client action registration",
                "code": '''/** @odoo-module **/

import { registry } from "@web/core/registry";
import { TrainingDashboard } from "./training_dashboard";

registry.category("actions").add("training.dashboard", TrainingDashboard);

// XML action
// <record id="action_training_dashboard" model="ir.actions.client">
//     <field name="name">Training Dashboard</field>
//     <field name="tag">training.dashboard</field>
// </record>''',
                "explain": "The action tag connects the server-side ir.actions.client record to the OWL component.",
            }
        ],
        [
            "Loading raw records in the browser and aggregating there.",
            "Creating dashboards without drill-down actions.",
            "Using a custom view when a client action is enough.",
            "Forgetting access rights on the server statistics method.",
        ],
        "Build a client action dashboard with three KPI cards and one card that opens a filtered course list.",
    ),
    _lesson(
        "W09",
        "POS Custom Buttons and Click Events",
        [
            "Add a custom control button to a POS screen.",
            "Handle click events with OWL methods.",
            "Keep POS actions compatible with offline behavior.",
        ],
        "POS extensions run in a high-speed operational UI where every button must be obvious and resilient.",
        "Decide which screen owns the action and whether the feature can work offline or must warn the cashier that connectivity is required.",
        "Register a button component, attach it to the target POS screen, and handle click events with methods that use POS services or models.",
        "Test with barcode scanning, touch screens, and rapid repeated clicks because POS users do not interact like back-office users.",
        "A good POS button adds one clear workflow step without slowing checkout or compromising order consistency.",
        [
            "POS buttons should be screen-specific.",
            "Click handlers should be idempotent where possible.",
            "Offline behavior must be considered.",
            "Use POS registries and services instead of globals.",
            "User feedback must be immediate.",
        ],
        [
            {
                "title": "Simple POS control button",
                "code": '''/** @odoo-module **/

import { Component } from "@odoo/owl";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";

export class CourseInfoButton extends Component {
    static template = "training.CourseInfoButton";

    onClick() {
        this.env.services.notification.add("Training mode is active.", {
            type: "info",
        });
    }
}

ProductScreen.addControlButton({
    component: CourseInfoButton,
    condition() {
        return true;
    },
});''',
                "explain": "The button is added to the ProductScreen and handles the click through a component method.",
            }
        ],
        [
            "Adding a button globally when it belongs to one screen.",
            "Not debouncing expensive click operations.",
            "Assuming a cashier has back-office permissions.",
            "Ignoring offline mode when the click needs the server.",
        ],
        "Add a POS ProductScreen button that shows a notification and disable it when no order is active.",
    ),
    _lesson(
        "W10",
        "Hiding POS Buttons Safely",
        [
            "Hide or show POS UI based on configuration.",
            "Distinguish visibility from authorization.",
            "Keep hidden actions protected server-side.",
        ],
        "Hiding a POS button can simplify cashier flow, but it must not be confused with security.",
        "Decide whether the control is hidden because it is irrelevant, disabled because a condition is missing, or forbidden because the user lacks a role.",
        "Use button conditions, configuration values loaded into POS, and server-side validation for any sensitive operation.",
        "Test every cashier role and POS configuration because a button hidden on one terminal may remain visible on another configuration.",
        "Production POS systems are distributed user interfaces; UI conditions must match central business policy and survive session reloads.",
        [
            "Visibility improves workflow but is not security.",
            "Button conditions can read POS configuration.",
            "Sensitive methods need server checks.",
            "Different POS configs may show different controls.",
            "Use clear disabled feedback when possible.",
        ],
        [
            {
                "title": "Configuration-based button condition",
                "code": '''ProductScreen.addControlButton({
    component: CourseInfoButton,
    condition() {
        const config = this.pos.config;
        return Boolean(config.module_training && config.show_training_button);
    },
});''',
                "explain": "The button appears only for POS configurations where the feature is enabled.",
            }
        ],
        [
            "Treating a hidden button as access control.",
            "Hard-coding user ids in JavaScript.",
            "Forgetting to load the configuration field into POS data.",
            "Making the button disappear without explaining why.",
        ],
        "Add a Boolean POS configuration field that controls a custom button and prove the server method still rejects unauthorized calls.",
    ),
    _lesson(
        "W11",
        "POS Popups and Dialog Flow",
        [
            "Show confirmation and input popups in POS.",
            "Handle popup results correctly.",
            "Design cashier-friendly dialog flows.",
        ],
        "POS popups interrupt the fastest workflow in Odoo, so they must be short, intentional, and recoverable.",
        "Use a popup when the cashier needs confirmation, small input, or a warning that cannot be ignored before continuing.",
        "Call the dialog or popup service, await the result where the framework supports it, and update the order only after the user confirms.",
        "Test keyboard, touch, barcode scanner focus, and cancel paths because popup usability is more important in POS than in most back-office screens.",
        "In production, a popup should prevent mistakes without creating a line at the register.",
        [
            "Use popups for short high-value interruptions.",
            "Always handle cancel and confirm paths.",
            "Do not put long forms in POS popups.",
            "Keep focus behavior cashier-friendly.",
            "Validate data after the popup closes.",
        ],
        [
            {
                "title": "Confirmation before clearing order",
                "code": '''async clearCurrentOrder() {
    const order = this.pos.get_order();
    if (!order || !order.get_orderlines().length) {
        return;
    }
    this.dialog.add(ConfirmationDialog, {
        title: "Clear order",
        body: "Remove all current order lines?",
        confirm: () => {
            for (const line of [...order.get_orderlines()]) {
                order.removeOrderline(line);
            }
        },
    });
}''',
                "explain": "The destructive action is performed only from the confirmation callback.",
            }
        ],
        [
            "Using a popup for information that could be a non-blocking notification.",
            "Forgetting the cancel path.",
            "Mutating orders before the user confirms.",
            "Creating popups that require too much typing at checkout.",
        ],
        "Create a confirmation popup that asks before applying a manager discount or clearing an order.",
    ),
    _lesson(
        "W12",
        "JavaScript Translations",
        [
            "Mark JavaScript strings for translation.",
            "Avoid concatenation that breaks translators' context.",
            "Test translated POS and web screens.",
        ],
        "JavaScript translations matter because OWL and POS features often introduce user-facing labels outside Python and XML fields.",
        "Write complete sentences for translators and pass variables as placeholders rather than building messages from fragments.",
        "Import _t or the appropriate translation helper, mark strings in components, and export translation terms through the normal Odoo i18n process.",
        "Test in a secondary language and look for layout overflow, untranslated strings, and strings generated dynamically from code values.",
        "A translated customization feels like part of the product; untranslated JavaScript is one of the fastest ways to expose custom code quality.",
        [
            "Use _t for user-facing JavaScript strings.",
            "Translate complete messages, not fragments.",
            "Avoid concatenation with translated text.",
            "Test labels in narrow screens.",
            "Do not translate technical keys or registry names.",
        ],
        [
            {
                "title": "Translated notification",
                "code": '''/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";

this.notification.add(
    _t("Course %(course)s was added to the training order.", {
        course: course.name,
    }),
    { type: "success" }
);''',
                "explain": "The full sentence is translatable and the course name is inserted as a placeholder.",
            }
        ],
        [
            "Concatenating translated fragments.",
            "Forgetting strings inside POS-only components.",
            "Translating technical identifiers.",
            "Not testing how long translated labels affect layout.",
        ],
        "Mark three JavaScript labels and one notification for translation, export terms, and verify them in another language.",
    ),
    _lesson(
        "W13",
        "POS RPC and Server Synchronization",
        [
            "Call server methods from POS safely.",
            "Respect offline and cashier permissions.",
            "Batch data where possible.",
        ],
        "POS RPC is tempting for every feature, but online calls can slow checkout and fail during network interruptions.",
        "Decide whether data must be loaded at session start, cached in POS, sent with the order, or fetched on demand.",
        "Use services to call model methods, batch requests, and show clear failure feedback when the POS must be online for the operation.",
        "Test disconnected network behavior and low permissions because POS often runs with users that differ from back-office managers.",
        "Production POS integrations should minimize synchronous calls during payment and order validation.",
        [
            "Prefer session-loaded data for frequently used reference data.",
            "Use RPC only when freshness is required.",
            "Batch calls to avoid checkout delays.",
            "Handle offline failures explicitly.",
            "Server methods must check permissions.",
        ],
        [
            {
                "title": "Fetch live loyalty balance",
                "code": '''async getLoyaltyBalance(partnerId) {
    if (!partnerId) {
        return 0;
    }
    try {
        return await this.orm.call(
            "training.loyalty",
            "pos_get_balance",
            [partnerId],
            { context: this.pos.user.context }
        );
    } catch {
        this.notification.add("Loyalty balance is unavailable while offline.", {
            type: "warning",
        });
        return null;
    }
}''',
                "explain": "The method calls the server only when a partner exists and gives a cashier-friendly warning on failure.",
            }
        ],
        [
            "Making one RPC call per product scan.",
            "Blocking payment on optional online data.",
            "Ignoring the POS user's access rights.",
            "Not deciding what happens offline.",
        ],
        "Implement one POS RPC method for live data and document exactly what the cashier sees when the network is down.",
    ),
    _lesson(
        "W14",
        "Rendering Dynamic POS Data",
        [
            "Load additional fields into POS data.",
            "Render dynamic data on products or order lines.",
            "Keep display values synchronized with order state.",
        ],
        "Dynamic POS rendering lets cashiers see availability, warnings, course metadata, or customer-specific information at the point of action.",
        "First decide whether the data is static for the session, changes during the session, or belongs on the order for accounting and audit.",
        "Load required fields through POS data loaders or model extensions, store display-ready values on POS models, and render them through OWL templates.",
        "Test reloads, order restore, and product cache updates because stale POS data can create incorrect cashier decisions.",
        "In production, dynamic POS UI should display enough information to guide action without becoming a back-office report.",
        [
            "Session-loaded data is fast but can become stale.",
            "Order-line data should be stored if needed later.",
            "Templates should render prepared values.",
            "Reload and restore behavior must be tested.",
            "Do not overload product tiles with too much data.",
        ],
        [
            {
                "title": "Product tile showing course level",
                "code": '''<t t-name="training.ProductCard" t-inherit="point_of_sale.ProductCard" t-inherit-mode="extension">
    <xpath expr="//div[hasclass('product-name')]" position="after">
        <div t-if="props.product.training_level" class="training-level">
            <t t-esc="props.product.training_level"/>
        </div>
    </xpath>
</t>''',
                "explain": "The template extension displays an extra product field only when the POS product data includes it.",
            }
        ],
        [
            "Rendering fields that were never loaded into POS.",
            "Showing stale stock or capacity without a refresh policy.",
            "Putting audit-critical values only in the UI.",
            "Making product cards unreadable with too many badges.",
        ],
        "Load a training_level field into POS products and render it on the product card with an empty-state fallback.",
    ),
    _lesson(
        "W15",
        "Clearing Order Lines and Mutating POS Orders",
        [
            "Mutate current orders through POS model APIs.",
            "Avoid unsafe direct array changes.",
            "Protect destructive actions with confirmation.",
        ],
        "POS order mutation must use framework methods so totals, taxes, discounts, and UI state remain consistent.",
        "Before clearing or changing lines, decide whether the action is reversible and whether a manager confirmation is required.",
        "Iterate over a copy of the current order lines and remove them with the POS order API rather than splicing internal arrays.",
        "Test lines with discounts, lots, taxes, notes, and combo products because destructive actions often fail on less common line types.",
        "A safe mutation preserves the invariants that payment, receipts, and order export depend on.",
        [
            "Use order APIs, not internal array mutation.",
            "Copy line arrays before removing while iterating.",
            "Confirm destructive actions.",
            "Recompute totals through framework behavior.",
            "Test special line types.",
        ],
        [
            {
                "title": "Clear all order lines safely",
                "code": '''clearOrderLines(order) {
    if (!order) {
        return;
    }
    for (const line of [...order.get_orderlines()]) {
        order.removeOrderline(line);
    }
    this.notification.add("The order was cleared.", { type: "success" });
}''',
                "explain": "The method iterates over a copy and delegates removal to the POS order API.",
            }
        ],
        [
            "Splicing order.orderlines directly.",
            "Removing lines while iterating over the live array.",
            "Skipping confirmation for destructive cashier actions.",
            "Forgetting special cases such as lot-tracked products.",
        ],
        "Add a clear-order control that confirms first, removes lines through the order API, and verifies totals return to zero.",
    ),
    _lesson(
        "W16",
        "XML-RPC Integration Fundamentals",
        [
            "Authenticate with Odoo over XML-RPC.",
            "Call model methods through execute_kw.",
            "Understand database, uid, password, model, method, and args.",
        ],
        "XML-RPC remains a practical integration interface for scripts, legacy systems, and training labs.",
        "Design integrations around explicit service users with narrow groups, not administrator credentials copied into scripts.",
        "Authenticate against common, then call object.execute_kw with model, method, positional args, and keyword options such as fields and limit.",
        "Verify access rights and record rules with the same service user because XML-RPC observes normal Odoo security unless code uses sudo internally.",
        "A production XML-RPC integration should have credentials, logging, retries, and data validation treated like any other external system.",
        [
            "Authenticate on /xmlrpc/2/common.",
            "Call models through /xmlrpc/2/object execute_kw.",
            "Use service users with limited groups.",
            "XML-RPC respects Odoo access rules.",
            "Never hard-code production passwords in code.",
        ],
        [
            {
                "title": "Python XML-RPC login and search_read",
                "code": '''import xmlrpc.client

url = "https://odoo.example.com"
db = "prod"
username = "integration@example.com"
password = "change-me"

common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
uid = common.authenticate(db, username, password, {})

models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")
courses = models.execute_kw(
    db, uid, password,
    "training.course", "search_read",
    [[["state", "=", "confirmed"]]],
    {"fields": ["name", "start_date"], "limit": 20},
)''',
                "explain": "The script authenticates once and calls search_read as the integration user.",
            }
        ],
        [
            "Using the admin account for integrations.",
            "Forgetting that record rules affect API results.",
            "Fetching all fields and all records by default.",
            "Logging passwords or full credential URLs.",
        ],
        "Create a script that authenticates over XML-RPC and reads the first ten confirmed courses with only three fields.",
    ),
    _lesson(
        "W17",
        "External API Authentication",
        [
            "Select an authentication pattern for external integrations.",
            "Store secrets outside source code.",
            "Validate callbacks and inbound requests.",
        ],
        "External APIs add another trust boundary around Odoo, so authentication design is part of the feature, not deployment cleanup.",
        "Choose API keys, OAuth2, signed webhooks, or basic authentication based on the provider and risk of the data being exchanged.",
        "Store secrets in system parameters, environment variables, or a secret manager, and wrap outbound calls in a service class or model method.",
        "Test expired credentials, revoked tokens, replayed webhooks, and provider downtime so the integration fails safely.",
        "Production API authentication should be observable: operators need enough logs to diagnose failures without exposing secrets.",
        [
            "Do not commit API credentials.",
            "Use least-privilege provider scopes.",
            "Validate webhook signatures when available.",
            "Handle token expiry deliberately.",
            "Log identifiers, not secrets.",
        ],
        [
            {
                "title": "Signed outbound request helper",
                "code": '''import requests
from odoo import models


class TrainingExternalClient(models.AbstractModel):
    _name = "training.external.client"
    _description = "Training External API Client"

    def _headers(self):
        token = self.env["ir.config_parameter"].sudo().get_param("training.api_token")
        return {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    def fetch_certificates(self):
        response = requests.get(
            "https://api.example.com/certificates",
            headers=self._headers(),
            timeout=10,
        )
        response.raise_for_status()
        return response.json()''',
                "explain": "The token is read from configuration at runtime and never appears in the source file.",
            }
        ],
        [
            "Committing secrets to the repository.",
            "Using broad OAuth scopes because they are easier during testing.",
            "Accepting inbound webhooks without signature validation.",
            "Logging Authorization headers during debugging.",
        ],
        "Design an authentication plan for one outbound API and one inbound webhook, including where each secret is stored.",
    ),
    _lesson(
        "W18",
        "Fetch and Export Workflows with XML-RPC",
        [
            "Export selected records over XML-RPC.",
            "Paginate large result sets.",
            "Make fetch jobs restartable.",
        ],
        "Export integrations fail in production when they assume the dataset is small and the network is perfect.",
        "Define the export domain, fields, ordering, and checkpoint strategy before writing the loop.",
        "Use search with offset or keyset-style domains, read only required fields, and persist the last successful checkpoint outside the transient process.",
        "Verify duplicates, skipped records, and interrupted runs by killing the process midway and restarting it against the same database.",
        "A robust export job values correctness over raw speed because downstream systems often cannot detect missing records.",
        [
            "Export only required fields.",
            "Paginate results instead of fetching everything.",
            "Use deterministic ordering.",
            "Persist checkpoints for restartability.",
            "Design for duplicates or idempotent downstream writes.",
        ],
        [
            {
                "title": "Paged XML-RPC export",
                "code": '''offset = 0
batch_size = 100
while True:
    rows = models.execute_kw(
        db, uid, password,
        "training.enrollment", "search_read",
        [[["write_date", ">=", "2026-01-01 00:00:00"]]],
        {
            "fields": ["id", "student_id", "course_id", "state", "write_date"],
            "order": "id",
            "offset": offset,
            "limit": batch_size,
        },
    )
    if not rows:
        break
    export_rows(rows)
    offset += batch_size''',
                "explain": "The loop exports in deterministic batches instead of loading the complete table at once.",
            }
        ],
        [
            "Exporting all records into memory.",
            "Using no order while paginating.",
            "Not handling retries or partial downstream failure.",
            "Exporting display names when stable ids are required.",
        ],
        "Write a paginated export for enrollments and simulate a restart after two batches.",
    ),
    _lesson(
        "W19",
        "CRUD Operations over XML-RPC",
        [
            "Create, read, update, and delete records through XML-RPC.",
            "Pass relational field commands correctly.",
            "Respect constraints and security during API writes.",
        ],
        "XML-RPC CRUD uses the same ORM methods that server code uses, so constraints, onchange gaps, access rights, and record rules all matter.",
        "Design write payloads from the model contract, not from the current form layout, because UI-only onchange logic may not run during API calls.",
        "Use create, write, unlink, search_read, and relational command lists for one2many or many2many fields when needed.",
        "Verify bad payloads, duplicate submissions, and permission failures because integrations often retry after ambiguous network errors.",
        "Production CRUD integrations should be idempotent where possible and should log remote ids, local ids, and operation outcomes.",
        [
            "create returns the new record id.",
            "write returns True when the update succeeds.",
            "unlink deletes records if access and rules allow it.",
            "Relational commands use tuple-like command lists.",
            "Onchange behavior is not a substitute for server validation.",
        ],
        [
            {
                "title": "Create and update enrollment",
                "code": '''enrollment_id = models.execute_kw(
    db, uid, password,
    "training.enrollment", "create",
    [{
        "student_id": student_id,
        "course_id": course_id,
        "state": "draft",
    }],
)

models.execute_kw(
    db, uid, password,
    "training.enrollment", "write",
    [[enrollment_id], {"state": "confirmed"}],
)''',
                "explain": "The API creates a draft enrollment and then updates its state through normal ORM security and constraints.",
            }
        ],
        [
            "Expecting form onchange methods to run during create.",
            "Sending display names instead of database ids for many2one fields.",
            "Deleting records with unlink when archiving would preserve audit history.",
            "Retrying creates without an external idempotency key.",
        ],
        "Create a course and enrollment over XML-RPC, update one field, and attempt an invalid write to confirm constraints are enforced.",
    ),
    _lesson(
        "W20",
        "Postman Authentication and CRUD Testing",
        [
            "Use Postman to document and test API calls.",
            "Authenticate against Odoo endpoints deliberately.",
            "Build repeatable CRUD request collections.",
        ],
        "Postman is useful for training and integration discovery because it makes request shape, authentication, and responses visible.",
        "For Odoo JSON-RPC or controller endpoints, define environment variables for base URL, database, credentials, token, and record ids.",
        "Create a collection that authenticates, stores returned values in variables, and then performs create, read, update, and delete or archive requests.",
        "Verify negative cases such as missing auth, wrong database, invalid ids, and insufficient rights because a collection that only proves success is incomplete.",
        "A good Postman collection becomes living integration documentation when examples, tests, and environment variables are kept clean.",
        [
            "Use environments for base URL and credentials.",
            "Store ids from responses for later requests.",
            "Add negative authorization tests.",
            "Do not export real secrets in shared collections.",
            "Document request purpose in the collection.",
        ],
        [
            {
                "title": "JSON-RPC body for search_read",
                "code": '''{
  "jsonrpc": "2.0",
  "method": "call",
  "params": {
    "service": "object",
    "method": "execute_kw",
    "args": [
      "{{db}}",
      {{uid}},
      "{{password}}",
      "training.course",
      "search_read",
      [[["state", "=", "confirmed"]]],
      {"fields": ["name", "start_date"], "limit": 5}
    ]
  },
  "id": 1
}''',
                "explain": "The request uses Postman environment variables so the same collection can run against staging or local databases.",
            }
        ],
        [
            "Exporting collections with real passwords.",
            "Hard-coding record ids that differ by database.",
            "Testing only successful CRUD operations.",
            "Confusing web session authentication with integration authentication.",
        ],
        "Build a Postman collection with login, search_read, create, write, and negative-access requests using environment variables only.",
        [
            {
                "kind": "table",
                "title": "Postman collection sections",
                "headers": ["Folder", "Purpose"],
                "rows": [
                    ["Auth", "Login and store uid or token"],
                    ["Read", "search_read and field checks"],
                    ["Write", "create and update examples"],
                    ["Negative", "missing auth and forbidden role tests"],
                ],
            }
        ],
    ),
]

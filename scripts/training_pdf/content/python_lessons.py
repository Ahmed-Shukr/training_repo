"""Python lesson content for the Odoo training PDF generator."""


def _explanation(topic, focus, mental_model, risk, odoo_context, practice):
    return [
        (
            f"{topic} is important because Python is both the language of Odoo customization and the daily tool for automation around Odoo. "
            f"Understanding {focus} helps developers read existing modules, change behavior deliberately, and avoid accidental side effects."
        ),
        (
            f"The useful mental model is {mental_model}. "
            f"When that model is clear, syntax stops being a guessing game and becomes a way to express intent precisely."
        ),
        (
            f"Python is designed for readability, but readable code still needs disciplined structure. "
            f"The main risk in this lesson is {risk}, especially when code runs inside a large framework with many inherited conventions."
        ),
        (
            f"In Odoo work, {odoo_context}. "
            f"This means a small Python choice can affect database records, scheduled jobs, access rules, view rendering, and upgrade safety."
        ),
        (
            f"Senior developers do not stop at making an example run once. "
            f"They ask what type each value has, who owns the data, which errors are expected, and how the code will behave when a module is installed, upgraded, or called by many users."
        ),
        (
            f"The practice habit is to write a tiny experiment, inspect the result, then move the idea into production code only after the behavior is understood. "
            f"{practice} is the kind of repetition that makes Python reliable under real Odoo constraints."
        ),
    ]


def _lesson(
    lesson_id,
    title,
    objectives,
    focus,
    mental_model,
    risk,
    odoo_context,
    practice,
    key_points,
    examples,
    common_mistakes,
    lab,
    slide_extras=None,
):
    return {
        "section": "python",
        "id": lesson_id,
        "title": title,
        "objectives": objectives,
        "explanation": _explanation(title, focus, mental_model, risk, odoo_context, practice),
        "key_points": key_points,
        "examples": examples,
        "common_mistakes": common_mistakes,
        "lab": lab,
        "slide_extras": slide_extras or [],
    }


LESSONS = [
    _lesson(
        "P01",
        "What Is a Programming Language and Interpreter",
        [
            "Explain what a programming language gives to humans and machines.",
            "Describe how an interpreter executes Python source code.",
            "Distinguish source code, bytecode, runtime objects, and process state.",
            "Connect interpreted execution to rapid Odoo development.",
        ],
        "the role of language rules, runtime behavior, and interpretation",
        "source code is parsed into instructions that create and manipulate objects while the interpreter manages execution",
        "thinking that code is just text rather than instructions with runtime state and side effects",
        "server actions, models, controllers, and scripts are all Python instructions executed by a long-running process",
        "Running small files and inspecting values builds confidence before touching framework code.",
        [
            "A programming language defines syntax, semantics, and a standard way to express computation.",
            "The Python interpreter reads code, builds objects, executes statements, and reports errors.",
            "Interactive execution is useful for experiments, but production code must be repeatable.",
            "The same source code can behave differently when the environment, imports, or data changes.",
            "Odoo developers need both language knowledge and framework knowledge.",
            "Understanding the interpreter explains why restarts are required after many code changes.",
        ],
        [
            {
                "title": "Observe Python executing statements",
                "code": """message = "hello Odoo developer"
print(message)
print(type(message))
print(len(message))""",
                "explain": (
                    "The source code creates a string object, binds it to a name, and passes it to functions. "
                    "Seeing the type and length makes the invisible runtime state concrete."
                ),
            }
        ],
        [
            "Treating Python files as configuration rather than executable code.",
            "Assuming an interactive experiment automatically matches Odoo's runtime environment.",
            "Ignoring errors because the interpreter stops at the first failing statement.",
            "Forgetting that a long-running Odoo process may need a restart to load changed code.",
        ],
        "Create a file named interpreter_lab.py that prints three values and their types. Run it, change one value, run again, and explain what the interpreter did each time.",
    ),
    _lesson(
        "P02",
        "Running Python, First Program, and Python 2 vs Python 3",
        [
            "Run Python from a file and from an interactive shell.",
            "Write a first program that accepts input and prints output.",
            "Explain why Python 3 is the standard for modern Odoo work.",
            "Recognize Python 2 compatibility problems in old code.",
        ],
        "executing Python consistently and recognizing version boundaries",
        "a command chooses a specific interpreter binary, and that interpreter defines available syntax and libraries",
        "running code with the wrong interpreter and misdiagnosing syntax or dependency errors",
        "modern Odoo versions use Python 3, while older community snippets may still contain Python 2 assumptions",
        "Always print sys.version and sys.executable when the environment is uncertain.",
        [
            "python3 usually selects Python 3 on Linux; python may vary by system.",
            "sys.executable shows the exact interpreter used for the running process.",
            "Python 3 treats print as a function and text as Unicode strings.",
            "Python 2 is end of life and should not be used for new Odoo development.",
            "Virtual environments change which interpreter and packages a command uses.",
            "A first program should be small enough that every line can be explained.",
        ],
        [
            {
                "title": "Confirm interpreter identity",
                "code": """import sys

print(sys.version)
print(sys.executable)
print("Hello from Python 3")""",
                "explain": (
                    "This program proves which Python is running before any dependency debugging begins. "
                    "It is a simple but valuable habit on servers with system Python, virtual environments, and deployment scripts."
                ),
            },
            {
                "title": "A small interactive program",
                "code": """name = input("Module name: ").strip()
print(f"Preparing scaffold for {name}")""",
                "explain": (
                    "input returns a string, strip removes surrounding whitespace, and an f-string formats the response. "
                    "Even this tiny program demonstrates data flow from user input to output."
                ),
            },
        ],
        [
            "Using python when the server expects python3.",
            "Copying Python 2 snippets with print statements or old exception syntax.",
            "Installing packages into one interpreter and running another.",
            "Skipping version checks during deployment troubleshooting.",
        ],
        "Write a first_program.py file that asks for a developer name and prints the Python executable, version, and a greeting. Run it with the interpreter from a virtual environment if available.",
    ),
    _lesson(
        "P03",
        "Data Types Overview",
        [
            "Name the common built-in Python data types.",
            "Explain mutable versus immutable objects.",
            "Use type inspection to understand unfamiliar values.",
            "Choose appropriate data structures for Odoo code.",
        ],
        "the shape and behavior of runtime values",
        "every value is an object with a type, identity, and operations that may or may not mutate the object",
        "using a value as if it were another type and producing subtle framework errors",
        "recordsets, dictionaries, lists, strings, dates, booleans, and numbers move constantly between models, controllers, and templates",
        "Inspecting type and representation in small examples prevents wrong assumptions in larger methods.",
        [
            "Core types include None, bool, int, float, str, list, tuple, dict, set, and custom classes.",
            "Mutable objects can change in place; immutable objects produce new values when transformed.",
            "type(value) and isinstance(value, type) answer different questions.",
            "Choosing the right type communicates intent to future maintainers.",
            "Framework APIs often expect a specific type, not merely a similar-looking value.",
            "Readable code makes conversions explicit at boundaries.",
        ],
        [
            {
                "title": "Inspect common values",
                "code": """values = [None, True, 42, 19.5, "odoo", ["sale"], ("draft",), {"state": "draft"}, {"crm", "sale"}]

for value in values:
    print(repr(value), type(value).__name__)""",
                "explain": (
                    "repr shows an unambiguous display of each value, and type reveals what operations are valid. "
                    "This is a useful debugging pattern when values arrive from JSON, forms, or ORM calls."
                ),
            }
        ],
        [
            "Assuming a string that looks like a number behaves like a number.",
            "Mutating a list that is shared by another part of the program.",
            "Using type(value) == SomeType when isinstance would handle subclasses better.",
            "Returning None where a caller expects an empty list or dictionary.",
        ],
        "Build a table of ten Python values with their type, whether they are mutable, and one valid operation. Include at least one value that would commonly appear in Odoo data.",
    ),
    _lesson(
        "P04",
        "Numbers, Math, and Operator Precedence",
        [
            "Use integer, float, and decimal-style thinking appropriately.",
            "Apply arithmetic operators and understand division behavior.",
            "Explain how operator precedence affects expressions.",
            "Write clear numeric code for business logic.",
        ],
        "numeric operations and expression grouping",
        "operators combine operands according to precedence rules unless parentheses make the intended order explicit",
        "encoding financial or quantity calculations with unclear grouping or inappropriate float assumptions",
        "prices, taxes, quantities, discounts, and stock moves depend on careful numeric logic",
        "Use parentheses and named intermediate values when a business rule matters.",
        [
            "int represents whole numbers of arbitrary size.",
            "float represents binary floating-point values and can surprise in decimal money calculations.",
            "/ returns true division, // returns floor division, and % returns remainder.",
            "** binds more tightly than multiplication and addition.",
            "Parentheses are better than relying on readers to remember precedence.",
            "Odoo monetary logic should usually use framework currency rounding utilities.",
        ],
        [
            {
                "title": "Make precedence visible",
                "code": """subtotal = 100
discount = 10
tax_rate = 0.15

wrong = subtotal - discount * (1 + tax_rate)
right = (subtotal - discount) * (1 + tax_rate)

print(wrong)
print(right)""",
                "explain": (
                    "Both expressions are syntactically valid, but they encode different business rules. "
                    "Parentheses turn the pricing rule into visible documentation."
                ),
            },
            {
                "title": "Division operators",
                "code": """quantity = 17
box_size = 5

print(quantity / box_size)
print(quantity // box_size)
print(quantity % box_size)""",
                "explain": (
                    "True division, floor division, and remainder answer different questions. "
                    "Stock and packaging code often needs all three, but each should be named clearly."
                ),
            },
        ],
        [
            "Using floats for money without understanding rounding requirements.",
            "Relying on precedence in long business expressions.",
            "Confusing / with // when calculating batches or pages.",
            "Forgetting that negative numbers affect floor division behavior.",
        ],
        "Implement a small price calculation with subtotal, discount, and tax. Write two versions, one compact and one using named intermediate values, then compare readability.",
    ),
    _lesson(
        "P05",
        "Variables, Expressions, and Statements",
        [
            "Define variables as name bindings to objects.",
            "Distinguish expressions that produce values from statements that perform actions.",
            "Write assignments that clarify business intent.",
            "Avoid misleading names and accidental rebinding.",
        ],
        "names, values, and executable instructions",
        "a variable name points to an object, expressions compute values, and statements tell the interpreter to do work",
        "believing assignment copies every object or that names and values are the same thing",
        "model methods often combine ORM recordsets, computed values, and side-effect statements such as writes",
        "Trace names through a method before changing logic that writes to records.",
        [
            "Assignment binds a name to an object; it does not always copy the object.",
            "An expression can be used where a value is needed.",
            "A statement changes control flow, binding, or program state.",
            "Good variable names explain domain meaning, not just type.",
            "Rebinding a name can be clear or confusing depending on scope and length.",
            "Side-effect statements should be easy to find in business methods.",
        ],
        [
            {
                "title": "Name binding with mutable values",
                "code": """tags = ["vip", "renewal"]
same_tags = tags
copy_tags = list(tags)

same_tags.append("priority")

print(tags)
print(copy_tags)""",
                "explain": (
                    "same_tags and tags point to the same list, while copy_tags points to a separate list. "
                    "This distinction matters when preparing values for ORM create and write calls."
                ),
            }
        ],
        [
            "Using names like data or temp for important business concepts.",
            "Assuming assignment makes a deep copy.",
            "Hiding database writes among many harmless expressions.",
            "Reusing one variable name for unrelated meanings in the same method.",
        ],
        "Write a short script that builds an order summary from named variables. Then refactor it so each variable name explains a business concept rather than a data type.",
    ),
    _lesson(
        "P06",
        "Strings: Concatenation, Formatting, Indexes, and Immutability",
        [
            "Create and combine strings safely.",
            "Use f-strings for readable formatting.",
            "Index and slice strings without mutating them.",
            "Handle text values carefully in Odoo fields and logs.",
        ],
        "text values and immutable sequence behavior",
        "a string is an immutable sequence of characters, so operations produce new strings instead of changing the original",
        "building unclear or unsafe text output with manual concatenation and hidden conversions",
        "names, emails, XML IDs, domains, log lines, and translated labels are all text-heavy surfaces",
        "Use formatting for display and structured values for logic.",
        [
            "Strings can be indexed and sliced like sequences.",
            "Immutability means assigning to a string index is not allowed.",
            "f-strings are usually the clearest formatting tool for local variables.",
            "join is preferable for combining many strings.",
            "strip, lower, and replace return new strings.",
            "Text used in SQL, XML, or HTML needs the appropriate framework escaping rules.",
        ],
        [
            {
                "title": "Format a user-facing label",
                "code": """partner = "Azure Interior"
amount = 1250.5
currency = "USD"

label = f"{partner}: {amount:,.2f} {currency}"
print(label)
print(label[0:14])""",
                "explain": (
                    "The f-string keeps the formatting rule close to the values and makes decimal display explicit. "
                    "The slice returns a new string; it does not change the original label."
                ),
            },
            {
                "title": "Join many parts",
                "code": """parts = ["sale", "order", "confirmed"]
xml_id = ".".join(parts)
print(xml_id)""",
                "explain": (
                    "join communicates that a separator is being placed between existing pieces. "
                    "It is clearer and more efficient than repeated concatenation in loops."
                ),
            },
        ],
        [
            "Concatenating strings and numbers without explicit conversion or formatting.",
            "Expecting string methods to modify the original value.",
            "Using slicing indexes without naming why the slice matters.",
            "Manually building SQL or HTML strings instead of using safe APIs.",
        ],
        "Create formatted labels for three fake invoices using f-strings. Include amount formatting, then demonstrate that calling upper on a string returns a new value.",
    ),
    _lesson(
        "P07",
        "Booleans and Type Conversion",
        [
            "Use True and False values in decisions.",
            "Explain truthy and falsy values.",
            "Convert between common types explicitly.",
            "Avoid ambiguous conversions in business rules.",
        ],
        "truth values and explicit boundaries between types",
        "Python asks objects for truth value in conditionals, while conversion functions build new values of requested types",
        "treating empty values, strings, numbers, and None as interchangeable",
        "forms and integrations often deliver strings that must become booleans, numbers, dates, or empty values intentionally",
        "Normalize external input at the boundary and keep core logic typed clearly.",
        [
            "False, None, zero, empty strings, and empty containers are falsy.",
            "Non-empty strings are truthy, even the string 'False'.",
            "bool, int, float, str, list, and dict perform conversions when valid.",
            "Explicit conversion makes validation errors visible.",
            "Use is None when testing for the absence marker specifically.",
            "Odoo field values may distinguish False, 0, empty strings, and empty recordsets.",
        ],
        [
            {
                "title": "Truthiness surprises",
                "code": """samples = [False, None, 0, "", [], "False", "0"]

for sample in samples:
    print(repr(sample), bool(sample))""",
                "explain": (
                    "The non-empty strings are truthy even though humans may read them as false-like. "
                    "External text input should be parsed with domain-specific rules instead of passed directly to bool."
                ),
            },
            {
                "title": "Validate conversion",
                "code": """raw_quantity = "12"
quantity = int(raw_quantity)

if quantity <= 0:
    raise ValueError("quantity must be positive")

print(quantity * 2)""",
                "explain": (
                    "Conversion and validation are separate steps. "
                    "This makes invalid input fail early instead of spreading string values through numeric logic."
                ),
            },
        ],
        [
            "Using bool('False') and expecting False.",
            "Testing if value when None and zero mean different things.",
            "Converting user input without handling ValueError.",
            "Letting raw JSON strings reach ORM write values unchecked.",
        ],
        "Write a parser for a yes/no text value that accepts yes, no, true, false, 1, and 0. Make invalid input raise ValueError with a clear message.",
    ),
    _lesson(
        "P08",
        "Lists: Slicing, Matrix Data, Methods, and Unpacking",
        [
            "Create and modify lists safely.",
            "Use indexes, slices, and common methods.",
            "Represent matrix-like data with nested lists.",
            "Unpack list values clearly.",
        ],
        "ordered mutable collections",
        "a list stores references in order and can be changed in place by index, slice, or method calls",
        "mutating shared lists or confusing shallow copies with independent nested data",
        "Odoo code often builds command lists, report rows, import buffers, and wizard selections",
        "Copy deliberately and keep list mutation close to where the list is created.",
        [
            "append adds one item; extend adds items from an iterable.",
            "Slicing returns a new list, while slice assignment mutates the original list.",
            "Nested lists can represent rows, but each row must be a separate list.",
            "Unpacking assigns multiple names from a sequence in one statement.",
            "sort mutates a list; sorted returns a new sorted list.",
            "Lists are good for ordered, repeatable collections.",
        ],
        [
            {
                "title": "List methods and slicing",
                "code": """states = ["draft", "sent", "sale"]
states.append("done")
first_two = states[:2]
states[1] = "quoted"

print(states)
print(first_two)""",
                "explain": (
                    "append and item assignment change the list in place, while the slice creates a new list. "
                    "This distinction is important when one function should not modify a caller's list."
                ),
            },
            {
                "title": "Unpack rows",
                "code": """rows = [
    ["SO001", 100.0],
    ["SO002", 250.0],
]

for order_name, total in rows:
    print(f"{order_name}: {total:.2f}")""",
                "explain": (
                    "Unpacking gives names to positions and makes row structure obvious. "
                    "If the row shape changes, Python raises an error instead of silently producing the wrong report."
                ),
            },
        ],
        [
            "Using one inner list repeatedly when building a matrix.",
            "Calling sort when the original order must be preserved.",
            "Appending a list when extend was intended.",
            "Changing a list passed into a function without documenting that side effect.",
        ],
        "Build a list of invoice rows, slice the first three, sort a copy by amount, and unpack each row into named variables while printing a summary.",
    ),
    _lesson(
        "P09",
        "Dictionaries: Keys, Values, and Methods",
        [
            "Use dictionaries for named data.",
            "Access keys safely with direct lookup and get.",
            "Iterate over keys, values, and items.",
            "Prepare dictionaries for ORM create and write operations.",
        ],
        "mapping keys to values",
        "a dictionary stores unique hashable keys, and each key identifies one current value",
        "using loose dictionaries without knowing which keys are required or optional",
        "Odoo create and write methods receive dictionaries whose keys must match field names and whose values must be valid for those fields",
        "Treat dictionaries at framework boundaries as contracts, not bags of random values.",
        [
            "Dictionary keys must be unique and hashable.",
            "dict[key] raises KeyError when missing; dict.get(key) can provide a default.",
            "items returns key-value pairs for iteration.",
            "update merges values and overwrites existing keys.",
            "in checks keys, not values.",
            "Clear key names make business payloads easier to review.",
        ],
        [
            {
                "title": "Build ORM values",
                "code": """partner_vals = {
    "name": "Azure Interior",
    "email": "info@example.com",
    "customer_rank": 1,
}

required = ["name", "email"]
missing = [key for key in required if not partner_vals.get(key)]
print(missing)
print(partner_vals.items())""",
                "explain": (
                    "The dictionary mirrors the field-value contract used by Odoo's create method. "
                    "Checking required keys before calling the ORM produces clearer errors."
                ),
            }
        ],
        [
            "Using get for required keys and accidentally accepting missing data.",
            "Overwriting a key during update without noticing.",
            "Assuming dictionaries preserve a business order in older Python contexts.",
            "Passing unknown field names into ORM write values.",
        ],
        "Create a dictionary for a fake product with name, default_code, list_price, and active. Validate required keys and print each key-value pair in a readable format.",
    ),
    _lesson(
        "P10",
        "Tuples",
        [
            "Create tuples and understand their immutability.",
            "Use tuples for fixed-size grouped values.",
            "Unpack tuples in assignments and loops.",
            "Recognize tuple syntax in Odoo domains and commands.",
        ],
        "fixed grouped values",
        "a tuple is an immutable ordered container, often used when position and size are part of the meaning",
        "confusing tuple immutability with immutability of objects inside the tuple",
        "domains, selection values, and relational command patterns use tuple-shaped data frequently",
        "Use tuples when the shape of the data is part of the contract.",
        [
            "A one-item tuple needs a trailing comma.",
            "Tuples are immutable, but contained mutable objects can still change.",
            "Tuple unpacking documents expected position meanings.",
            "Tuples are hashable only if all contained values are hashable.",
            "Odoo domains commonly use three-item tuples such as ('field', '=', value).",
            "Fixed shapes should be validated before dynamic construction.",
        ],
        [
            {
                "title": "Domain tuple shape",
                "code": """domain = [
    ("state", "=", "sale"),
    ("amount_total", ">", 1000),
]

for field, operator, value in domain:
    print(field, operator, value)""",
                "explain": (
                    "Each tuple has a fixed three-part meaning, and unpacking enforces that expectation. "
                    "This mirrors a common Odoo domain pattern."
                ),
            }
        ],
        [
            "Writing ('draft') and thinking it is a tuple instead of a string.",
            "Trying to assign to a tuple element.",
            "Assuming mutable objects inside a tuple cannot change.",
            "Using positional tuples where a dictionary would be clearer.",
        ],
        "Build three domain tuples and unpack them in a loop. Add one malformed tuple and observe the error, then explain why early failure is useful.",
    ),
    _lesson(
        "P11",
        "Sets",
        [
            "Create sets for unique values.",
            "Use membership and set operations.",
            "Choose sets over lists for uniqueness and fast lookup.",
            "Apply sets to validation and import cleanup tasks.",
        ],
        "unordered unique collections",
        "a set stores unique hashable values and supports mathematical operations such as union and intersection",
        "using lists for uniqueness checks and producing duplicate business actions",
        "imports, access checks, tags, and external identifiers often need duplicate detection",
        "Convert to a set when uniqueness is the rule, then sort if presentation order matters.",
        [
            "Sets remove duplicates automatically.",
            "Membership checks in sets are efficient.",
            "Union, intersection, and difference express comparison logic clearly.",
            "Sets are unordered and should not drive display order directly.",
            "Only hashable values can be set members.",
            "An empty set is created with set(), not {}.",
        ],
        [
            {
                "title": "Find duplicate external IDs",
                "code": """external_ids = ["sale.order_1", "sale.order_2", "sale.order_1"]
seen = set()
duplicates = set()

for xml_id in external_ids:
    if xml_id in seen:
        duplicates.add(xml_id)
    seen.add(xml_id)

print(duplicates)""",
                "explain": (
                    "The seen set makes duplicate detection direct and efficient. "
                    "This pattern is useful before import jobs where duplicates would create confusing failures."
                ),
            }
        ],
        [
            "Expecting a set to preserve insertion order for presentation.",
            "Trying to put dictionaries or lists inside a set.",
            "Using {} when an empty set was intended.",
            "Converting to a set too early and losing meaningful duplicates.",
        ],
        "Given two lists of module technical names, find modules in both lists, modules only in the first list, and the sorted union of all modules.",
    ),
    _lesson(
        "P12",
        "Conditionals: Truthy Values, Ternary Expressions, and Short-Circuiting",
        [
            "Write if, elif, and else branches clearly.",
            "Use truthy values deliberately.",
            "Apply ternary expressions only when they improve readability.",
            "Explain and use short-circuit boolean evaluation.",
        ],
        "controlled branching based on conditions",
        "Python evaluates conditions to a truth value and executes only the matching branch, while and and or may skip later expressions",
        "compressing business rules until nobody can see which case is handled",
        "computed fields, constraints, button actions, and controllers often branch by state, permissions, and input completeness",
        "Prefer explicit branches for business policy and compact expressions for simple value selection.",
        [
            "if starts a branch, elif adds alternatives, and else catches the remainder.",
            "and returns when the first falsy value is found; or returns when the first truthy value is found.",
            "A ternary expression has the form a if condition else b.",
            "Short-circuiting can prevent unsafe access to missing values.",
            "Complex conditionals deserve named boolean variables.",
            "Condition order should reflect business priority and safety.",
        ],
        [
            {
                "title": "Readable business branch",
                "code": """state = "draft"
amount_total = 1500

if state != "draft":
    action = "readonly"
elif amount_total > 1000:
    action = "manager_approval"
else:
    action = "confirm"

print(action)""",
                "explain": (
                    "The branches read like a policy and make the exceptional cases visible. "
                    "This is better than hiding the same rule in a dense expression."
                ),
            },
            {
                "title": "Short-circuit guard",
                "code": """partner = {"name": "Azure", "email": ""}
message = partner.get("email") and f"Send mail to {partner['email']}"
print(message or "No email available")""",
                "explain": (
                    "The f-string is only built when the email value is truthy. "
                    "Short-circuiting is helpful, but it should remain easy to read."
                ),
            },
        ],
        [
            "Using truthiness when zero, False, and None have different meanings.",
            "Writing nested ternary expressions for business rules.",
            "Forgetting that and and or return operands, not always True or False.",
            "Placing expensive or unsafe checks before cheap guard checks.",
        ],
        "Write a decision function that returns an invoice approval state based on amount, customer status, and whether required fields are present. Refactor complex conditions into named booleans.",
    ),
    _lesson(
        "P13",
        "for Loops, Iterables, range, and enumerate",
        [
            "Iterate over sequences and other iterables.",
            "Use range for counted loops.",
            "Use enumerate when an index is genuinely needed.",
            "Write loop bodies that avoid accidental side effects.",
        ],
        "repeated work over iterable values",
        "a for loop asks an iterable for values one at a time and binds each value to the loop variable",
        "looping by index when direct iteration would be safer and clearer",
        "Odoo recordsets, lists of values, import rows, and report lines are all iterated constantly",
        "Choose the loop form that matches the data: values, index plus value, or generated counts.",
        [
            "for item in items is the default readable loop.",
            "range produces integer sequences without storing a full list.",
            "enumerate provides index and value together.",
            "Loop variables are ordinary names and remain bound after the loop.",
            "Avoid modifying a list while iterating over it unless the pattern is deliberate.",
            "Odoo recordsets can be iterated directly like collections of records.",
        ],
        [
            {
                "title": "Enumerate import rows",
                "code": """rows = [
    {"name": "A", "price": 10},
    {"name": "B", "price": 20},
]

for line_number, row in enumerate(rows, start=1):
    print(f"Line {line_number}: {row['name']} costs {row['price']}")""",
                "explain": (
                    "enumerate keeps the human line number next to the row data without manual counters. "
                    "This is ideal for import validation errors."
                ),
            }
        ],
        [
            "Using range(len(items)) when the item itself is all that is needed.",
            "Changing the list being iterated and skipping elements unexpectedly.",
            "Forgetting start=1 when reporting human line numbers.",
            "Using loop variables after the loop without considering empty input.",
        ],
        "Validate a list of CSV-like row dictionaries. Use enumerate(start=1) to collect readable error messages that include line numbers.",
    ),
    _lesson(
        "P14",
        "while Loops, break, continue, and pass",
        [
            "Use while loops for condition-driven repetition.",
            "Exit loops intentionally with break.",
            "Skip to the next iteration with continue.",
            "Use pass as an explicit placeholder only when appropriate.",
        ],
        "looping until a condition changes",
        "a while loop keeps executing while its condition remains truthy, so the body must move the program toward completion",
        "creating infinite loops or hiding unfinished code behind pass",
        "polling jobs, batch processing, and retry loops appear in integration and maintenance scripts around Odoo",
        "Make loop exit conditions visible and test them with small limits.",
        [
            "while is best when the number of iterations is not known upfront.",
            "break exits the nearest loop immediately.",
            "continue skips the rest of the current iteration.",
            "pass does nothing and should not hide missing implementation.",
            "Loop counters and retry limits prevent runaway scripts.",
            "Sleep and backoff are important in real polling loops.",
        ],
        [
            {
                "title": "Batch loop with explicit progress",
                "code": """remaining = [1, 2, 3, 4, 5]
processed = []

while remaining:
    item = remaining.pop(0)
    if item == 3:
        continue
    processed.append(item)

print(processed)""",
                "explain": (
                    "The loop condition is tied to the remaining work, and each iteration removes one item. "
                    "continue skips one item without stopping the entire batch."
                ),
            }
        ],
        [
            "Writing while True without a clear break condition.",
            "Using pass where a real implementation or explicit error should exist.",
            "Forgetting to update the condition variable.",
            "Catching all errors inside a loop and continuing forever.",
        ],
        "Write a retry loop that attempts a fake operation up to three times. Use break on success, continue on a recoverable validation issue, and raise an error after all retries fail.",
    ),
    _lesson(
        "P15",
        "Functions: Parameters, args, kwargs, return, and Docstrings",
        [
            "Define reusable functions with clear parameters.",
            "Use positional, keyword, *args, and **kwargs appropriately.",
            "Return values deliberately.",
            "Write docstrings that explain behavior and constraints.",
        ],
        "packaging behavior behind a callable interface",
        "a function receives arguments, binds them to parameter names, executes a body, and optionally returns a value",
        "creating functions with vague contracts that callers misuse",
        "Odoo model methods are functions with framework-provided self, decorators, context, and return conventions",
        "Write the call site first in a small example, then design the function signature to make that call obvious.",
        [
            "Parameters define what information a function needs.",
            "return sends a value back to the caller and stops function execution.",
            "*args collects extra positional arguments; **kwargs collects extra keyword arguments.",
            "Default arguments are evaluated once when the function is defined.",
            "Docstrings should state purpose, important parameters, return value, and notable errors.",
            "Small pure functions are easier to test than large methods with hidden side effects.",
        ],
        [
            {
                "title": "A clear calculation function",
                "code": """def compute_discounted_total(subtotal, discount_rate=0.0):
    \"\"\"Return subtotal after applying a decimal discount rate.\"\"\"
    if not 0 <= discount_rate <= 1:
        raise ValueError("discount_rate must be between 0 and 1")
    return subtotal * (1 - discount_rate)

print(compute_discounted_total(100, discount_rate=0.15))""",
                "explain": (
                    "The signature exposes the required subtotal and optional discount, while validation protects the business rule. "
                    "The docstring describes behavior rather than repeating the code."
                ),
            },
            {
                "title": "Forward keyword options",
                "code": """def log_action(action, **details):
    print(action)
    for key, value in sorted(details.items()):
        print(f"  {key}: {value}")

log_action("confirm_order", order="SO001", user="admin")""",
                "explain": (
                    "**kwargs is useful for flexible metadata, but the function still needs a clear purpose. "
                    "Sorting details gives stable output for logs and tests."
                ),
            },
        ],
        [
            "Using mutable default arguments such as [] or {}.",
            "Returning different types for similar outcomes without documenting them.",
            "Accepting **kwargs and silently ignoring misspelled options.",
            "Writing docstrings that say what is obvious instead of why constraints exist.",
        ],
        "Write a function that accepts product price, quantity, and optional discount. Validate inputs, return a total, and include a docstring with one example call.",
    ),
    _lesson(
        "P16",
        "Scope, global, and nonlocal",
        [
            "Explain local, enclosing, global, and built-in scopes.",
            "Understand name resolution with the LEGB rule.",
            "Use global and nonlocal sparingly and deliberately.",
            "Avoid hidden shared state in Odoo modules.",
        ],
        "where names are looked up and rebound",
        "Python searches local, enclosing, global, and built-in scopes for a name, while assignment normally binds in the local scope",
        "using hidden module-level state that behaves unpredictably under long-running workers",
        "Odoo workers may serve many requests, so module globals can leak state between users or transactions",
        "Pass values explicitly unless shared state is truly part of the design.",
        [
            "LEGB means local, enclosing, global, built-in.",
            "Reading a global name is different from rebinding it.",
            "global tells Python assignment should target the module scope.",
            "nonlocal targets an enclosing function scope.",
            "Module constants are acceptable; mutable module caches need careful invalidation.",
            "Framework context should usually travel through self.env.context, parameters, or records.",
        ],
        [
            {
                "title": "Local and enclosing scope",
                "code": """def make_counter():
    count = 0

    def next_value():
        nonlocal count
        count += 1
        return count

    return next_value

counter = make_counter()
print(counter())
print(counter())""",
                "explain": (
                    "nonlocal allows the inner function to rebind a name from the enclosing function. "
                    "This is powerful, but in application code explicit objects are often easier to reason about."
                ),
            }
        ],
        [
            "Using global to avoid passing parameters.",
            "Storing request-specific data in module-level variables.",
            "Shadowing built-in names such as list, dict, or id.",
            "Assuming each web request starts with fresh module globals.",
        ],
        "Write a function that accidentally shadows a built-in, then fix the name. Next, create a small closure with nonlocal and explain why you would avoid the same pattern for request data.",
    ),
    _lesson(
        "P17",
        "OOP: Classes, __init__, and Methods",
        [
            "Define classes and create instances.",
            "Use __init__ to initialize object state.",
            "Write instance methods that use self correctly.",
            "Connect Python classes to Odoo models.",
        ],
        "bundling data and behavior into objects",
        "a class defines behavior, an instance holds state, and methods receive the instance as self",
        "placing behavior in disconnected helper code when object state would make the design clearer",
        "Odoo models are Python classes whose fields and methods are extended by the framework metaclass and registry",
        "Practice with plain classes first so Odoo model classes feel less magical.",
        [
            "class creates a new type.",
            "__init__ runs when an instance is created.",
            "self is the current instance passed automatically to instance methods.",
            "Instance attributes belong to one object unless shared deliberately.",
            "Methods should operate on the object's coherent state.",
            "Odoo model methods receive recordsets as self, not always one record.",
        ],
        [
            {
                "title": "Plain class with state",
                "code": """class InvoiceSummary:
    def __init__(self, number, total):
        self.number = number
        self.total = total

    def label(self):
        return f"{self.number}: {self.total:.2f}"

summary = InvoiceSummary("INV001", 250.0)
print(summary.label())""",
                "explain": (
                    "The instance owns number and total, and the method formats state through self. "
                    "This mirrors how model methods organize behavior around record data."
                ),
            }
        ],
        [
            "Forgetting self in method definitions.",
            "Using class attributes when instance attributes were intended.",
            "Doing too much work in __init__ instead of keeping construction simple.",
            "Assuming an Odoo recordset method always receives a single record.",
        ],
        "Create a plain ProductLabel class with name, default_code, and price. Add a method that returns a formatted label and test it with two instances.",
    ),
    _lesson(
        "P18",
        "classmethod and staticmethod",
        [
            "Distinguish instance methods, class methods, and static methods.",
            "Use classmethod for alternate constructors or class-level behavior.",
            "Use staticmethod only when no instance or class state is needed.",
            "Avoid unnecessary method types in framework code.",
        ],
        "choosing the right method binding",
        "instance methods receive self, class methods receive cls, and static methods receive neither automatically",
        "using method decorators to hide unclear responsibilities",
        "Odoo has its own API decorators, so plain Python method decorators should be used only when the semantics are clear",
        "Prefer ordinary instance methods until a class-level or stateless behavior is truly needed.",
        [
            "Instance methods are the default and receive self.",
            "classmethod receives the class and can create instances polymorphically.",
            "staticmethod is namespaced on the class but has no automatic access to state.",
            "Alternate constructors are a common classmethod use case.",
            "Utility functions do not always need to live inside a class.",
            "Framework decorators and Python decorators solve different problems.",
        ],
        [
            {
                "title": "Alternate constructor",
                "code": """class Money:
    def __init__(self, amount, currency):
        self.amount = amount
        self.currency = currency

    @classmethod
    def from_string(cls, text):
        amount_text, currency = text.split()
        return cls(float(amount_text), currency)

    @staticmethod
    def is_supported_currency(currency):
        return currency in {"USD", "EUR"}

money = Money.from_string("10.50 USD")
print(money.amount, money.currency)
print(Money.is_supported_currency("USD"))""",
                "explain": (
                    "from_string receives cls, so subclasses could reuse the constructor correctly. "
                    "The currency check is static because it does not need instance or class state."
                ),
            }
        ],
        [
            "Using staticmethod to avoid thinking about where a function belongs.",
            "Using classmethod when no class-level behavior exists.",
            "Confusing Python decorators with Odoo api decorators.",
            "Putting business logic in utility methods that bypass record rules or environment context.",
        ],
        "Create a small CodeParser class with a classmethod from_text and a staticmethod is_valid_code. Explain which method would become an instance method if it needed stored state.",
    ),
    _lesson(
        "P19",
        "Encapsulation, Inheritance, Polymorphism, and super",
        [
            "Explain encapsulation as controlled access to behavior and state.",
            "Use inheritance to specialize behavior.",
            "Recognize polymorphism through shared method contracts.",
            "Call parent behavior correctly with super.",
        ],
        "object-oriented extension patterns",
        "objects expose behavior through methods, subclasses can override methods, and callers can rely on shared method names",
        "overriding framework methods without preserving parent behavior or contracts",
        "Odoo customization frequently inherits models and extends methods such as create, write, unlink, and action methods",
        "Before overriding, read the parent contract and decide whether to run code before or after super.",
        [
            "Encapsulation keeps callers focused on behavior rather than internal representation.",
            "Inheritance models an is-a relationship or framework extension point.",
            "Polymorphism lets different classes respond to the same method call.",
            "super delegates to the next implementation in the method resolution order.",
            "Overridden methods must preserve expected arguments, return values, and side effects.",
            "Odoo super calls are essential for keeping core framework behavior intact.",
        ],
        [
            {
                "title": "Extend behavior with super",
                "code": """class Document:
    def validate(self):
        return ["base checks"]

class Invoice(Document):
    def validate(self):
        checks = super().validate()
        checks.append("invoice checks")
        return checks

print(Invoice().validate())""",
                "explain": (
                    "The subclass adds invoice-specific behavior without discarding the parent checks. "
                    "This is the same mindset needed when extending Odoo model methods."
                ),
            }
        ],
        [
            "Overriding a method and forgetting super when parent behavior is required.",
            "Changing the return type of an inherited method.",
            "Using inheritance where composition or a helper function would be clearer.",
            "Accessing internal attributes from outside instead of using methods.",
        ],
        "Build a base Approval class and two subclasses with different validation rules. Ensure each subclass calls super and returns the same type.",
    ),
    _lesson(
        "P20",
        "Dunders, MRO, and Multiple Inheritance",
        [
            "Recognize common double-underscore methods.",
            "Explain method resolution order.",
            "Understand the risks and uses of multiple inheritance.",
            "Design cooperative methods that work with super.",
        ],
        "Python's data model and inheritance lookup",
        "dunder methods let objects participate in Python protocols, and MRO defines the order used to find methods",
        "creating inheritance diamonds that break because methods do not cooperate",
        "Odoo models combine Python inheritance with framework inheritance mechanisms, so method lookup must be respected",
        "Use multiple inheritance only when each class has a narrow, cooperative responsibility.",
        [
            "__repr__, __str__, __len__, and __bool__ customize common Python operations.",
            "MRO can be inspected with ClassName.mro().",
            "super follows MRO, not simply the textual parent class.",
            "Multiple inheritance works best when methods accept compatible signatures.",
            "Mixins should be small and focused.",
            "Odoo's _inherit is not identical to plain Python inheritance, but Python method rules still matter.",
        ],
        [
            {
                "title": "Inspect MRO",
                "code": """class AuditMixin:
    def save(self):
        print("audit")
        return super().save()

class Base:
    def save(self):
        print("base")
        return True

class Document(AuditMixin, Base):
    pass

print([cls.__name__ for cls in Document.mro()])
Document().save()""",
                "explain": (
                    "The MRO shows the actual lookup order, and super follows that order cooperatively. "
                    "This is why mixins should call super when they participate in a shared method chain."
                ),
            },
            {
                "title": "Readable object representation",
                "code": """class PartnerRef:
    def __init__(self, name, ref):
        self.name = name
        self.ref = ref

    def __repr__(self):
        return f"PartnerRef(name={self.name!r}, ref={self.ref!r})"

print(PartnerRef("Azure", "AZ001"))""",
                "explain": (
                    "__repr__ makes debugging output precise and reconstructive. "
                    "Useful representations save time when inspecting collections of domain objects."
                ),
            },
        ],
        [
            "Assuming super always calls the immediate parent class.",
            "Writing mixins that do not call super in cooperative chains.",
            "Using dunder methods for cleverness instead of protocol clarity.",
            "Creating multiple inheritance hierarchies with incompatible method signatures.",
        ],
        "Create two mixins and a base class with a cooperative process method. Print the MRO and show the order in which each method runs.",
    ),
    _lesson(
        "P21",
        "map, filter, zip, reduce, and lambdas",
        [
            "Use functional helpers where they improve clarity.",
            "Write simple lambda expressions.",
            "Combine related iterables with zip.",
            "Recognize when comprehensions or explicit loops are clearer.",
        ],
        "functional iteration tools",
        "functions can be passed around as values, and iterable helpers apply them lazily or combine iterable streams",
        "choosing clever expressions that hide business logic and complicate debugging",
        "Odoo code benefits from readable transformations of records and values, but framework recordsets already provide rich APIs",
        "Use these tools for small transformations, not for hiding multi-step business rules.",
        [
            "map applies a function to each item.",
            "filter keeps items whose predicate is truthy.",
            "zip pairs items from iterables by position.",
            "functools.reduce combines items into one result but can be less readable than a loop.",
            "lambda creates a small anonymous function expression.",
            "In many cases, comprehensions are more Pythonic than map or filter.",
        ],
        [
            {
                "title": "Transform and pair values",
                "code": """names = ["sale", "crm", "stock"]
labels = list(map(str.upper, names))
enabled = [True, False, True]

for module, is_enabled in zip(names, enabled):
    print(module, is_enabled)

print(labels)""",
                "explain": (
                    "map performs a simple transformation, while zip pairs two related sequences. "
                    "Converting map to a list is necessary when you want to inspect all results immediately."
                ),
            },
            {
                "title": "Reduce with care",
                "code": """from functools import reduce

amounts = [10, 20, 30]
total = reduce(lambda current, amount: current + amount, amounts, 0)
print(total)""",
                "explain": (
                    "reduce works, but sum(amounts) would be clearer for this particular operation. "
                    "Choose the tool that makes the intent most obvious."
                ),
            },
        ],
        [
            "Using lambda for complex logic that deserves a named function.",
            "Forgetting that map and filter are lazy iterators in Python 3.",
            "Using zip when input lengths must be validated and may differ.",
            "Using reduce where sum, any, all, or a loop is clearer.",
        ],
        "Transform a list of product dictionaries into display names using both map and a comprehension. Explain which version your team should keep and why.",
    ),
    _lesson(
        "P22",
        "Comprehensions",
        [
            "Write list, dict, and set comprehensions.",
            "Use conditional clauses in comprehensions responsibly.",
            "Replace simple loops with clear comprehensions.",
            "Avoid dense comprehensions for business-heavy logic.",
        ],
        "concise collection construction",
        "a comprehension builds a new collection by iterating over an input and optionally filtering or transforming items",
        "packing too much logic into one line and making errors hard to locate",
        "Odoo developers often build domains, value lists, summaries, and validation messages from records or imported rows",
        "A comprehension is good when it reads like a sentence; otherwise use a loop.",
        [
            "List comprehensions build lists.",
            "Set comprehensions build unique sets.",
            "Dict comprehensions build key-value mappings.",
            "Filters appear after the for clause with if.",
            "Nested comprehensions should be used sparingly.",
            "Do not use comprehensions only for side effects.",
        ],
        [
            {
                "title": "Build validation messages",
                "code": """rows = [
    {"line": 1, "name": "A", "price": 10},
    {"line": 2, "name": "", "price": 5},
]

errors = [f"Line {row['line']}: missing name" for row in rows if not row["name"]]
print(errors)""",
                "explain": (
                    "The comprehension cleanly maps invalid rows into error messages. "
                    "If validation had multiple rules and side effects, a normal loop would be easier to maintain."
                ),
            },
            {
                "title": "Create a lookup dictionary",
                "code": """products = [
    {"default_code": "A001", "name": "Desk"},
    {"default_code": "A002", "name": "Chair"},
]

by_code = {product["default_code"]: product for product in products}
print(by_code["A001"]["name"])""",
                "explain": (
                    "The dict comprehension creates a direct lookup table from a list of records. "
                    "This is a common pattern before matching imported rows to existing data."
                ),
            },
        ],
        [
            "Using comprehensions for print, write, or other side effects.",
            "Writing nested comprehensions that require careful mental parsing.",
            "Forgetting duplicate keys overwrite earlier values in dict comprehensions.",
            "Hiding validation rules inside a long conditional expression.",
        ],
        "Given a list of order dictionaries, create a list of confirmed order names, a set of customer names, and a dictionary mapping order name to total.",
    ),
    _lesson(
        "P23",
        "Decorators",
        [
            "Explain decorators as functions that wrap or modify callables.",
            "Write a simple decorator with functools.wraps.",
            "Understand why decorators affect call behavior.",
            "Relate Python decorators to Odoo api decorators carefully.",
        ],
        "callable wrapping and metadata-preserving behavior",
        "a decorator receives a function and returns a replacement callable, often adding work before or after the original call",
        "using decorators without understanding that they change the callable being executed",
        "Odoo uses decorators such as api.depends, api.constrains, and api.model to tell the framework how methods participate in ORM behavior",
        "Read decorator documentation before changing method signatures or return expectations.",
        [
            "The @decorator syntax is assignment sugar around function wrapping.",
            "functools.wraps preserves name, docstring, and metadata.",
            "Decorators can add logging, validation, caching, or framework registration.",
            "The wrapper should accept compatible arguments.",
            "Odoo decorators are framework contracts, not merely style markers.",
            "Decorator order matters when multiple decorators are stacked.",
        ],
        [
            {
                "title": "Simple timing decorator",
                "code": """from functools import wraps
from time import perf_counter

def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = perf_counter() - start
            print(f"{func.__name__} took {elapsed:.4f}s")
    return wrapper

@timed
def compute_total(amounts):
    return sum(amounts)

print(compute_total([10, 20, 30]))""",
                "explain": (
                    "The decorator adds timing around the original function while returning its result. "
                    "wraps keeps debugging and documentation output tied to the original function name."
                ),
            }
        ],
        [
            "Forgetting to return the original function's result from the wrapper.",
            "Not using functools.wraps and losing useful metadata.",
            "Changing arguments in a wrapper without a clear contract.",
            "Copying Odoo decorators without understanding what the ORM expects.",
        ],
        "Write a decorator that logs function arguments and return value for a pure calculation function. Then explain why the same decorator might be unsafe around sensitive production data.",
    ),
    _lesson(
        "P24",
        "Error Handling",
        [
            "Raise and catch exceptions intentionally.",
            "Use try, except, else, and finally appropriately.",
            "Design error messages for operators and users.",
            "Avoid swallowing framework errors.",
        ],
        "explicit handling of exceptional control flow",
        "exceptions interrupt normal execution and travel up the call stack until code handles them or the program reports failure",
        "catching broad exceptions and hiding the actual cause of data or transaction problems",
        "Odoo translates many exceptions into user-visible errors and rolls back failed transactions",
        "Catch only errors you can handle locally, and let unexpected errors remain visible.",
        [
            "raise creates an exception.",
            "except handles matching exception types.",
            "else runs when no exception occurred.",
            "finally runs whether success or failure occurred.",
            "Specific exception types are safer than bare except.",
            "Logging should preserve traceback information for unexpected failures.",
        ],
        [
            {
                "title": "Validate input with a specific exception",
                "code": """def parse_positive_int(text):
    try:
        value = int(text)
    except ValueError as exc:
        raise ValueError(f"expected a whole number, got {text!r}") from exc
    if value <= 0:
        raise ValueError("value must be positive")
    return value

print(parse_positive_int("12"))""",
                "explain": (
                    "The function catches only conversion errors and raises a clearer domain message while preserving the original cause. "
                    "Validation after conversion keeps separate failure modes understandable."
                ),
            },
            {
                "title": "Always close local resources",
                "code": """path = "/tmp/python-error-lab.txt"
handle = open(path, "w")
try:
    handle.write("hello\\n")
finally:
    handle.close()""",
                "explain": (
                    "finally ensures cleanup even if writing fails. "
                    "In real code, a with statement is usually better, but finally explains the control-flow guarantee."
                ),
            },
        ],
        [
            "Using bare except and hiding KeyboardInterrupt or system exit.",
            "Catching an error only to print it and continue with corrupt state.",
            "Raising generic Exception when a specific type would be clearer.",
            "Discarding the original exception cause during re-raise.",
        ],
        "Write a parser for imported quantities that reports line numbers on invalid input. Catch only expected conversion errors and collect all row errors for display.",
    ),
    _lesson(
        "P25",
        "Generators",
        [
            "Define generator functions with yield.",
            "Explain lazy iteration and one-pass consumption.",
            "Use generators for streaming large data.",
            "Avoid generator surprises in debugging and reuse.",
        ],
        "lazy production of values",
        "a generator function pauses at yield and resumes later, producing values only as the caller requests them",
        "assuming a generator is a reusable list and accidentally consuming it once",
        "large exports, imports, and reports can benefit from streaming rather than loading everything into memory",
        "Use generators when memory or incremental processing matters, and materialize them only at the boundary that needs a list.",
        [
            "yield turns a function into a generator function.",
            "Generators are iterators and are consumed as they are iterated.",
            "Lazy evaluation can reduce memory use.",
            "list(generator) materializes all values and consumes the generator.",
            "Generator expressions are concise lazy expressions.",
            "Debugging generators often requires careful inspection because values appear over time.",
        ],
        [
            {
                "title": "Stream cleaned rows",
                "code": """def cleaned_rows(raw_rows):
    for row in raw_rows:
        name = row.get("name", "").strip()
        if not name:
            continue
        yield {"name": name, "price": float(row.get("price", 0))}

rows = [{"name": " Desk ", "price": "10.5"}, {"name": "", "price": "2"}]
for row in cleaned_rows(rows):
    print(row)""",
                "explain": (
                    "The generator yields only valid cleaned rows and skips empty names without building an intermediate list. "
                    "This pattern scales well for import pipelines."
                ),
            }
        ],
        [
            "Iterating a generator once and expecting values to remain for a second pass.",
            "Materializing a huge generator too early with list.",
            "Putting hidden side effects inside a generator and forgetting when they execute.",
            "Returning a list when the caller expects lazy behavior.",
        ],
        "Write a generator that yields valid invoice rows from raw dictionaries. Demonstrate that iterating it twice without recreating it produces values only the first time.",
    ),
    _lesson(
        "P26",
        "Modules, Packages, Imports, and __name__",
        [
            "Organize code into modules and packages.",
            "Use import forms responsibly.",
            "Explain how Python finds modules.",
            "Use __name__ == '__main__' for script entry points.",
        ],
        "code organization and import execution",
        "a module is executed once when imported, names become attributes, and packages group modules with importable paths",
        "putting side effects at import time and surprising tests, scripts, or Odoo module loading",
        "Odoo addons are Python packages whose __init__.py files import models, controllers, and other framework registrations",
        "Keep imports cheap and predictable, and put script-only behavior behind a main guard.",
        [
            "A .py file is a module; a package is a directory Python can import.",
            "import module keeps names qualified; from module import name brings a name directly into scope.",
            "Python searches sys.path to find modules.",
            "Module top-level code runs at import time.",
            "__name__ is '__main__' when a file is run as a script.",
            "Circular imports usually indicate misplaced responsibilities.",
        ],
        [
            {
                "title": "Use a main guard",
                "code": """def main():
    print("run as a script")

if __name__ == "__main__":
    main()""",
                "explain": (
                    "The main guard prevents script behavior from running when the module is imported elsewhere. "
                    "This is essential for reusable utilities and safe tests."
                ),
            },
            {
                "title": "Prefer qualified imports for clarity",
                "code": """import pathlib

config_path = pathlib.Path("/etc/odoo/odoo.conf")
print(config_path.exists())""",
                "explain": (
                    "The qualified pathlib.Path call shows where the name comes from. "
                    "This reduces ambiguity in modules with many imports."
                ),
            },
        ],
        [
            "Executing database or network work at import time.",
            "Using wildcard imports and hiding where names come from.",
            "Creating circular imports between modules.",
            "Forgetting to import a new Odoo models file in the package __init__.py.",
        ],
        "Create a two-file package with a helper module and a script module. Import the helper from the script and protect executable behavior with a main guard.",
    ),
    _lesson(
        "P27",
        "pip, venv, and PyPI",
        [
            "Create and activate a Python virtual environment.",
            "Install packages with pip into the intended environment.",
            "Explain PyPI as a package index.",
            "Manage dependencies safely for Odoo projects.",
        ],
        "isolated dependency management",
        "a virtual environment provides a separate interpreter context with its own installed packages",
        "installing dependencies into the wrong environment or accepting unreviewed packages",
        "Odoo deployments depend on exact Python packages for Odoo itself, custom addons, integrations, and tooling",
        "Record dependencies and reproduce environments instead of fixing imports manually on one server.",
        [
            "venv creates an isolated environment directory.",
            "Activating a venv changes PATH so python and pip point into that environment.",
            "python -m pip ensures pip belongs to the selected interpreter.",
            "PyPI hosts public Python packages, but packages still require review.",
            "requirements files should be pinned or constrained for production.",
            "System Python packages and project packages should not be mixed casually.",
        ],
        [
            {
                "title": "Create and inspect a virtual environment",
                "code": """python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -c "import sys; print(sys.executable)"
python -m pip list""",
                "explain": (
                    "Using python -m pip ties package installation to the currently selected interpreter. "
                    "Printing sys.executable confirms the shell is using the virtual environment."
                ),
            },
            {
                "title": "Install from a requirements file",
                "code": """cat > requirements.txt <<'REQ'
requests
REQ

python -m pip install -r requirements.txt
python -m pip show requests""",
                "explain": (
                    "A requirements file makes dependencies explicit and repeatable. "
                    "Production projects usually pin versions or use a lock process after security review."
                ),
            },
        ],
        [
            "Running pip without checking which Python it targets.",
            "Installing project packages into the system Python on a production host.",
            "Depending on unpinned package versions for repeatable deployments.",
            "Adding packages without license, maintenance, or security review.",
        ],
        "Create a virtual environment, install one small package, print the interpreter path, freeze dependencies, deactivate, and explain why the package is not necessarily available to system Python.",
    ),
    _lesson(
        "P28",
        "Debugging and Python Habits for Odoo Developers",
        [
            "Apply a disciplined debugging workflow.",
            "Use print, logging, pdb, and tests appropriately.",
            "Develop Python habits that fit Odoo's ORM and transaction model.",
            "Turn fixes into maintainable changes.",
        ],
        "evidence-driven debugging and framework-aware habits",
        "debugging is a loop of observing, forming a hypothesis, making a minimal test, and verifying the result",
        "changing code until the symptom disappears without understanding the cause",
        "Odoo code runs inside transactions, environments, caches, access rules, and long-running worker processes",
        "Keep experiments small, keep production changes reversible, and write the regression test when the bug is understood.",
        [
            "Start with the exact error, input, user, company, and database state.",
            "Use logging for server code where print may be hidden or noisy.",
            "pdb is useful locally but dangerous if left in server code.",
            "Respect recordsets: methods may receive zero, one, or many records.",
            "Do not bypass the ORM unless you understand transactions, security, and cache invalidation.",
            "Readable, boring Python is a strength in business systems.",
        ],
        [
            {
                "title": "Use logging instead of print in server code",
                "code": """import logging

_logger = logging.getLogger(__name__)

def confirm_order(order_name, amount_total):
    _logger.info("confirming order %s amount=%s", order_name, amount_total)
    if amount_total <= 0:
        raise ValueError("amount_total must be positive")
    return True""",
                "explain": (
                    "Logging keeps diagnostic output integrated with server log configuration and preserves structured context. "
                    "The message uses lazy formatting so values are formatted only when the log level needs them."
                ),
            },
            {
                "title": "Small reproduction before framework change",
                "code": """def normalize_code(value):
    return value.strip().upper().replace(" ", "_")

assert normalize_code(" sale order ") == "SALE_ORDER"
assert normalize_code("crm") == "CRM"
print("normalization rules understood")""",
                "explain": (
                    "A small pure function lets the team test the rule outside Odoo before connecting it to models or views. "
                    "This reduces the number of moving parts during debugging."
                ),
            },
        ],
        [
            "Leaving breakpoint calls in code that may run on a server.",
            "Debugging as administrator only and missing access-rule failures.",
            "Calling ensure_one reflexively instead of designing for recordsets.",
            "Fixing a symptom without adding a regression test or prevention note.",
        ],
        "Take a failing Python function, write down the expected input and output, add two focused assertions, fix the function, then describe how the same habit applies before changing an Odoo model method.",
        [
            {
                "kind": "bullets",
                "title": "Odoo Python habits",
                "items": [
                    "Use the ORM for business data unless there is a reviewed reason not to.",
                    "Treat recordsets as collections until a method explicitly requires one record.",
                    "Keep imports cheap and module loading predictable.",
                    "Log with context and avoid leaking secrets.",
                    "Write small tests around rules before wiring them into views and actions.",
                ],
            }
        ],
    ),
]

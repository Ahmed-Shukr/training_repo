"""Atomic Python presentation slides for Merit Advisory Odoo training."""

SLIDES = [
    {
        "section": 1,
        "title": "Running Python programs",
        "topics": [
            {
                "id": "P-INTERPRETER",
                "title": "What Python and the interpreter are",
                "points": [
                    "Python is a programming language used to write instructions for a computer.",
                    "The interpreter is the program that reads and runs Python code.",
                    "Odoo server code, automation scripts, and shell experiments all run through Python.",
                ],
                "examples": [
                    {"label": "Check interpreter path", "code": "python3 -c \"import sys; print(sys.executable)\""},
                    {"label": "Run one instruction", "code": "python3 -c \"print('Hello from Python')\""},
                ],
            },
            {
                "id": "P-RUN-PYTHON3",
                "title": "Run python and python3",
                "points": [
                    "On many Linux systems, python3 is the command for modern Python.",
                    "The python command may be missing or may point to a different version.",
                    "Check the version when a server has more than one Python installed.",
                ],
                "examples": [
                    {"label": "Check Python 3 version", "code": "python3 --version"},
                    {"label": "Compare command versions", "code": "python --version || true"},
                ],
            },
            {
                "id": "P-FIRST-PROGRAM",
                "title": "First program",
                "points": [
                    "A Python program is a text file containing Python statements.",
                    "The print function displays output in the terminal.",
                    "Run the file again after each small change to build confidence.",
                ],
                "examples": [
                    {"label": "Create hello.py", "code": "print('Hello, Merit Advisory')"},
                    {"label": "Run the file", "code": "python3 hello.py"},
                ],
            },
            {
                "id": "P-PY2-PY3",
                "title": "Python 2 vs Python 3",
                "points": [
                    "Python 3 is the standard for current Odoo development.",
                    "Old examples on the internet may use Python 2 syntax.",
                    "Version mismatches often appear as syntax errors or missing library behavior.",
                ],
                "examples": [
                    {"label": "Modern print syntax", "code": "print('Odoo uses Python 3')"},
                    {"label": "Show exact runtime", "code": "python3 -c \"import sys; print(sys.version)\""},
                ],
            },
        ],
    },
    {
        "section": 2,
        "title": "Basic values and text",
        "topics": [
            {
                "id": "P-NUMBERS",
                "title": "Numbers",
                "points": [
                    "Python supports integers for whole numbers and floats for decimal values.",
                    "Arithmetic operators include plus, minus, multiply, divide, and exponent.",
                    "Use parentheses when you want to make calculation order obvious.",
                ],
                "examples": [
                    {"label": "Calculate subtotal", "code": "subtotal = 100 + 25\nprint(subtotal)"},
                    {"label": "Calculate tax", "code": "tax = 125 * 0.15\nprint(tax)"},
                ],
            },
            {
                "id": "P-VARIABLES",
                "title": "Variables",
                "points": [
                    "A variable is a name bound to a value.",
                    "Choose names that explain what the value represents.",
                    "Python variables do not need a type written in front of the name.",
                ],
                "examples": [
                    {"label": "Store a customer name", "code": "customer_name = 'Agrolait'\nprint(customer_name)"},
                    {"label": "Update a count", "code": "invoice_count = 3\ninvoice_count = invoice_count + 1\nprint(invoice_count)"},
                ],
            },
            {
                "id": "P-STRINGS",
                "title": "Strings",
                "points": [
                    "A string is text surrounded by quotes.",
                    "Single quotes and double quotes both work when used consistently.",
                    "Strings are common for names, descriptions, XML ids, and messages.",
                ],
                "examples": [
                    {"label": "Create a string", "code": "module_name = 'sale_custom'\nprint(module_name)"},
                    {"label": "Use double quotes", "code": "message = \"Invoice posted\"\nprint(message)"},
                ],
            },
            {
                "id": "P-CONCAT",
                "title": "String concatenation",
                "points": [
                    "Concatenation joins strings together with the plus operator.",
                    "Both sides must be strings or Python raises a type error.",
                    "For larger messages, f-strings are usually easier to read.",
                ],
                "examples": [
                    {"label": "Join two strings", "code": "name = 'Odoo'\nprint('Hello ' + name)"},
                    {"label": "Convert before joining", "code": "count = 3\nprint('Invoices: ' + str(count))"},
                ],
            },
            {
                "id": "P-FSTRINGS",
                "title": "f-strings",
                "points": [
                    "An f-string starts with f before the quote.",
                    "Expressions inside braces are evaluated and inserted into the text.",
                    "Use f-strings for clear messages that include values.",
                ],
                "examples": [
                    {"label": "Format a customer message", "code": "partner = 'Deco Addict'\nprint(f'Customer: {partner}')"},
                    {"label": "Format a total", "code": "total = 149.99\nprint(f'Total due: {total}')"},
                ],
            },
            {
                "id": "P-STRING-INDEX",
                "title": "String indexes",
                "points": [
                    "Indexes select one character from a string.",
                    "Python indexes start at zero.",
                    "Negative indexes count backward from the end.",
                ],
                "examples": [
                    {"label": "First character", "code": "code = 'INV001'\nprint(code[0])"},
                    {"label": "Last character", "code": "code = 'INV001'\nprint(code[-1])"},
                ],
            },
            {
                "id": "P-STRING-SLICE",
                "title": "String slicing",
                "points": [
                    "A slice extracts part of a string.",
                    "The start index is included and the stop index is not included.",
                    "Slicing is useful for prefixes, suffixes, and fixed-format codes.",
                ],
                "examples": [
                    {"label": "Get prefix", "code": "number = 'INV/2026/001'\nprint(number[:3])"},
                    {"label": "Get year", "code": "number = 'INV/2026/001'\nprint(number[4:8])"},
                ],
            },
            {
                "id": "P-IMMUTABILITY",
                "title": "String immutability",
                "points": [
                    "Strings are immutable, so their characters cannot be changed in place.",
                    "String methods return new strings instead of editing the original.",
                    "Assign the result when you want to keep the changed value.",
                ],
                "examples": [
                    {"label": "Create a changed copy", "code": "name = 'odoo'\nupper_name = name.upper()\nprint(upper_name)"},
                    {"label": "Replace text", "code": "code = 'SO001'\ncode = code.replace('SO', 'INV')\nprint(code)"},
                ],
            },
            {
                "id": "P-TYPE-CONVERSION",
                "title": "Type conversion",
                "points": [
                    "Type conversion creates a value of another type.",
                    "Common conversion functions include str, int, float, and bool.",
                    "Convert input data before doing math or comparisons.",
                ],
                "examples": [
                    {"label": "Convert text to integer", "code": "quantity = int('5')\nprint(quantity + 2)"},
                    {"label": "Convert number to text", "code": "order_id = 42\nprint('Order ' + str(order_id))"},
                ],
            },
            {
                "id": "P-BOOLEANS",
                "title": "Booleans",
                "points": [
                    "A boolean is either True or False.",
                    "Booleans are used for decisions and status flags.",
                    "Comparison expressions create boolean results.",
                ],
                "examples": [
                    {"label": "Store active state", "code": "is_active = True\nprint(is_active)"},
                    {"label": "Compare amount", "code": "amount = 250\nprint(amount > 100)"},
                ],
            },
        ],
    },
    {
        "section": 3,
        "title": "Collections of data",
        "topics": [
            {
                "id": "P-LISTS",
                "title": "Lists",
                "points": [
                    "A list stores multiple values in order.",
                    "Lists can grow, shrink, and be changed after creation.",
                    "Use lists when order matters or when you need a sequence of records.",
                ],
                "examples": [
                    {"label": "Create a list", "code": "partners = ['Agrolait', 'Azure Interior']\nprint(partners)"},
                    {"label": "Read by index", "code": "partners = ['Agrolait', 'Azure Interior']\nprint(partners[0])"},
                ],
            },
            {
                "id": "P-LIST-SLICE",
                "title": "List slicing",
                "points": [
                    "List slicing returns a new list containing part of another list.",
                    "The start index is included and the stop index is not included.",
                    "Slicing is useful for paging, previews, and small batches.",
                ],
                "examples": [
                    {"label": "First two items", "code": "ids = [10, 11, 12, 13]\nprint(ids[:2])"},
                    {"label": "Middle items", "code": "ids = [10, 11, 12, 13]\nprint(ids[1:3])"},
                ],
            },
            {
                "id": "P-LIST-APPEND",
                "title": "append - Add to a list",
                "points": [
                    "append adds one item to the end of a list.",
                    "It changes the existing list in place.",
                    "Use append when building a collection step by step.",
                ],
                "examples": [
                    {"label": "Add one customer", "code": "partners = []\npartners.append('Agrolait')\nprint(partners)"},
                    {"label": "Collect ids", "code": "record_ids = [1]\nrecord_ids.append(2)\nprint(record_ids)"},
                ],
            },
            {
                "id": "P-LIST-POP",
                "title": "pop - Remove from a list",
                "points": [
                    "pop removes an item from a list and returns it.",
                    "Without an index, pop removes the last item.",
                    "Use pop when the removed value still needs to be used.",
                ],
                "examples": [
                    {"label": "Remove last item", "code": "tasks = ['check', 'restart']\nnext_task = tasks.pop()\nprint(next_task)"},
                    {"label": "Remove first item", "code": "tasks = ['check', 'restart']\nfirst_task = tasks.pop(0)\nprint(first_task)"},
                ],
            },
            {
                "id": "P-DICTS",
                "title": "Dictionaries",
                "points": [
                    "A dictionary stores key and value pairs.",
                    "Keys are used to look up related values.",
                    "Dictionaries are common in Odoo values, context, and API payloads.",
                ],
                "examples": [
                    {"label": "Create values", "code": "vals = {'name': 'Agrolait', 'active': True}\nprint(vals)"},
                    {"label": "Read a value", "code": "vals = {'name': 'Agrolait'}\nprint(vals['name'])"},
                ],
            },
            {
                "id": "P-DICT-GET",
                "title": "dict.get",
                "points": [
                    "get reads a dictionary value without raising an error for a missing key.",
                    "You can provide a default value as the second argument.",
                    "Use get when missing data is expected and acceptable.",
                ],
                "examples": [
                    {"label": "Get missing value", "code": "vals = {'name': 'Agrolait'}\nprint(vals.get('email'))"},
                    {"label": "Get with default", "code": "vals = {'name': 'Agrolait'}\nprint(vals.get('active', True))"},
                ],
            },
            {
                "id": "P-DICT-KEYS",
                "title": "dict.keys",
                "points": [
                    "keys shows the keys currently stored in a dictionary.",
                    "It is useful when inspecting unfamiliar data.",
                    "Convert to list when you need a simple printable list of keys.",
                ],
                "examples": [
                    {"label": "Show keys", "code": "vals = {'name': 'Agrolait', 'active': True}\nprint(vals.keys())"},
                    {"label": "Print key list", "code": "vals = {'name': 'Agrolait'}\nprint(list(vals.keys()))"},
                ],
            },
            {
                "id": "P-TUPLES",
                "title": "Tuples",
                "points": [
                    "A tuple stores ordered values like a list.",
                    "Tuples are immutable, so their contents cannot be changed in place.",
                    "Use tuples for fixed pairs or values that should stay together.",
                ],
                "examples": [
                    {"label": "Create a tuple", "code": "status = ('draft', 'Draft')\nprint(status)"},
                    {"label": "Unpack a tuple", "code": "code, label = ('posted', 'Posted')\nprint(label)"},
                ],
            },
            {
                "id": "P-SETS",
                "title": "Sets",
                "points": [
                    "A set stores unique values with no guaranteed order.",
                    "Adding a duplicate value keeps only one copy.",
                    "Use sets when uniqueness matters more than order.",
                ],
                "examples": [
                    {"label": "Remove duplicates", "code": "tags = {'vip', 'vip', 'retail'}\nprint(tags)"},
                    {"label": "Find shared items", "code": "a = {'sale', 'stock'}\nb = {'stock', 'account'}\nprint(a & b)"},
                ],
            },
        ],
    },
    {
        "section": 4,
        "title": "Control flow",
        "topics": [
            {
                "id": "P-IF-ELIF-ELSE",
                "title": "if, elif, and else",
                "points": [
                    "if runs code only when a condition is true.",
                    "elif checks another condition when the previous one was false.",
                    "else handles the remaining case.",
                ],
                "examples": [
                    {"label": "Check amount", "code": "amount = 120\nif amount > 100:\n    print('large order')"},
                    {"label": "Choose status message", "code": "state = 'draft'\nif state == 'posted':\n    print('done')\nelif state == 'draft':\n    print('needs review')\nelse:\n    print('unknown')"},
                ],
            },
            {
                "id": "P-TRUTHY-FALSEY",
                "title": "Truthy and falsey values",
                "points": [
                    "Python treats some non-boolean values as true or false in conditions.",
                    "Empty strings, empty lists, empty dictionaries, zero, and None are falsey.",
                    "Non-empty values are usually truthy.",
                ],
                "examples": [
                    {"label": "Check a missing email", "code": "email = ''\nif not email:\n    print('email missing')"},
                    {"label": "Check a list", "code": "invoices = [101]\nif invoices:\n    print('has invoices')"},
                ],
            },
            {
                "id": "P-FOR",
                "title": "for loops",
                "points": [
                    "A for loop repeats code for each item in a sequence.",
                    "The loop variable receives one item at a time.",
                    "Use for loops to process lists of records or values.",
                ],
                "examples": [
                    {"label": "Print names", "code": "for name in ['Agrolait', 'Deco Addict']:\n    print(name)"},
                    {"label": "Total amounts", "code": "total = 0\nfor amount in [10, 20, 30]:\n    total += amount\nprint(total)"},
                ],
            },
            {
                "id": "P-RANGE",
                "title": "range",
                "points": [
                    "range creates a sequence of numbers for looping.",
                    "The stop value is not included.",
                    "Use range when the number of repetitions matters.",
                ],
                "examples": [
                    {"label": "Loop three times", "code": "for i in range(3):\n    print(i)"},
                    {"label": "Start and stop", "code": "for number in range(1, 4):\n    print(number)"},
                ],
            },
            {
                "id": "P-ENUMERATE",
                "title": "enumerate",
                "points": [
                    "enumerate gives both the index and the item during a loop.",
                    "It avoids manually updating a counter.",
                    "Use it when position and value are both useful.",
                ],
                "examples": [
                    {"label": "Number names", "code": "names = ['Agrolait', 'Deco Addict']\nfor index, name in enumerate(names):\n    print(index, name)"},
                    {"label": "Start at one", "code": "lines = ['first', 'second']\nfor number, line in enumerate(lines, start=1):\n    print(number, line)"},
                ],
            },
            {
                "id": "P-WHILE",
                "title": "while loops",
                "points": [
                    "A while loop repeats while a condition stays true.",
                    "The loop must change something or it may run forever.",
                    "Use while loops for retry logic or waiting conditions.",
                ],
                "examples": [
                    {"label": "Count upward", "code": "count = 0\nwhile count < 3:\n    print(count)\n    count += 1"},
                    {"label": "Process queue", "code": "queue = ['a', 'b']\nwhile queue:\n    print(queue.pop(0))"},
                ],
            },
            {
                "id": "P-BREAK",
                "title": "break",
                "points": [
                    "break exits the nearest loop immediately.",
                    "Use it when the work is finished before the loop naturally ends.",
                    "It is common when searching for the first matching value.",
                ],
                "examples": [
                    {"label": "Stop at match", "code": "for name in ['A', 'B', 'C']:\n    if name == 'B':\n        break\n    print(name)"},
                    {"label": "Find first large amount", "code": "for amount in [20, 150, 10]:\n    if amount > 100:\n        print(amount)\n        break"},
                ],
            },
            {
                "id": "P-CONTINUE",
                "title": "continue",
                "points": [
                    "continue skips the rest of the current loop step.",
                    "The loop then moves to the next item.",
                    "Use it to skip values that should not be processed.",
                ],
                "examples": [
                    {"label": "Skip empty names", "code": "for name in ['Agrolait', '', 'Deco']:\n    if not name:\n        continue\n    print(name)"},
                    {"label": "Skip draft records", "code": "for state in ['draft', 'posted']:\n    if state == 'draft':\n        continue\n    print(state)"},
                ],
            },
        ],
    },
    {
        "section": 5,
        "title": "Functions and reusable code",
        "topics": [
            {
                "id": "P-FUNCTIONS",
                "title": "Functions",
                "points": [
                    "A function is a named block of reusable code.",
                    "Use def to create a function.",
                    "Functions make programs easier to read, test, and reuse.",
                ],
                "examples": [
                    {"label": "Define and call", "code": "def greet():\n    print('Hello')\n\ngreet()"},
                    {"label": "Reusable action", "code": "def show_ready():\n    print('Ready for Odoo work')\n\nshow_ready()"},
                ],
            },
            {
                "id": "P-PARAMETERS",
                "title": "Parameters",
                "points": [
                    "Parameters are names that receive values passed into a function.",
                    "They let one function work with different input values.",
                    "Use clear parameter names to describe expected data.",
                ],
                "examples": [
                    {"label": "Pass a name", "code": "def greet(name):\n    print(f'Hello {name}')\n\ngreet('Agrolait')"},
                    {"label": "Pass an amount", "code": "def show_total(amount):\n    print(f'Total: {amount}')\n\nshow_total(250)"},
                ],
            },
            {
                "id": "P-DEFAULTS",
                "title": "Default parameters",
                "points": [
                    "A default parameter value is used when no argument is provided.",
                    "Defaults make common calls shorter.",
                    "Avoid mutable defaults such as empty lists unless you understand the behavior.",
                ],
                "examples": [
                    {"label": "Default greeting", "code": "def greet(name='team'):\n    print(f'Hello {name}')\n\ngreet()"},
                    {"label": "Override default", "code": "def limit_text(text, limit=10):\n    print(text[:limit])\n\nlimit_text('Odoo training', 4)"},
                ],
            },
            {
                "id": "P-RETURN",
                "title": "return",
                "points": [
                    "return sends a result back to the caller.",
                    "Code after return in the same function is not executed.",
                    "Use return when another part of the program needs the computed value.",
                ],
                "examples": [
                    {"label": "Return a total", "code": "def add_tax(amount):\n    return amount * 1.15\n\nprint(add_tax(100))"},
                    {"label": "Return a message", "code": "def invoice_label(number):\n    return f'Invoice {number}'\n\nprint(invoice_label('INV001'))"},
                ],
            },
            {
                "id": "P-ARGS",
                "title": "*args",
                "points": [
                    "*args collects extra positional arguments into a tuple.",
                    "Use it when a function may receive a flexible number of values.",
                    "Keep it simple for beginners and prefer named parameters when possible.",
                ],
                "examples": [
                    {"label": "Sum many amounts", "code": "def total(*amounts):\n    return sum(amounts)\n\nprint(total(10, 20, 30))"},
                    {"label": "Print labels", "code": "def show_labels(*labels):\n    for label in labels:\n        print(label)\n\nshow_labels('draft', 'posted')"},
                ],
            },
            {
                "id": "P-KWARGS",
                "title": "**kwargs",
                "points": [
                    "**kwargs collects extra named arguments into a dictionary.",
                    "It is common in framework code that passes flexible options.",
                    "Read keyword names carefully because misspellings can hide bugs.",
                ],
                "examples": [
                    {"label": "Collect named values", "code": "def show_values(**kwargs):\n    print(kwargs)\n\nshow_values(name='Agrolait', active=True)"},
                    {"label": "Read an option", "code": "def connect(**options):\n    print(options.get('host', 'localhost'))\n\nconnect(host='db01')"},
                ],
            },
            {
                "id": "P-SCOPE",
                "title": "Scope",
                "points": [
                    "Scope describes where a name can be used.",
                    "Names created inside a function are local to that function.",
                    "Pass values into functions instead of relying on hidden outside state.",
                ],
                "examples": [
                    {"label": "Local variable", "code": "def build_name():\n    name = 'Agrolait'\n    return name\n\nprint(build_name())"},
                    {"label": "Pass outside value", "code": "prefix = 'INV'\ndef make_number(number):\n    return f'{prefix}{number}'\n\nprint(make_number('001'))"},
                ],
            },
        ],
    },
    {
        "section": 6,
        "title": "Objects, errors, modules, and Odoo habits",
        "topics": [
            {
                "id": "P-CLASSES-INIT",
                "title": "Classes and __init__",
                "points": [
                    "A class defines a kind of object with data and behavior.",
                    "__init__ runs when a new object is created.",
                    "self refers to the current object inside the class.",
                ],
                "examples": [
                    {"label": "Create a class", "code": "class Partner:\n    def __init__(self, name):\n        self.name = name\n\npartner = Partner('Agrolait')\nprint(partner.name)"},
                    {"label": "Store multiple fields", "code": "class Invoice:\n    def __init__(self, number, amount):\n        self.number = number\n        self.amount = amount\n\nprint(Invoice('INV001', 100).amount)"},
                ],
            },
            {
                "id": "P-METHODS",
                "title": "Methods",
                "points": [
                    "A method is a function defined inside a class.",
                    "Methods use self to read or change object data.",
                    "Odoo models are classes with many framework methods.",
                ],
                "examples": [
                    {"label": "Call a method", "code": "class Partner:\n    def greet(self):\n        return 'Hello'\n\nprint(Partner().greet())"},
                    {"label": "Use object data", "code": "class Partner:\n    def __init__(self, name):\n        self.name = name\n    def label(self):\n        return f'Partner: {self.name}'\n\nprint(Partner('Agrolait').label())"},
                ],
            },
            {
                "id": "P-INHERITANCE",
                "title": "Inheritance",
                "points": [
                    "Inheritance lets one class reuse behavior from another class.",
                    "The child class can add or replace methods.",
                    "Odoo module customization often uses inheritance to extend existing models.",
                ],
                "examples": [
                    {"label": "Create child class", "code": "class Document:\n    def label(self):\n        return 'Document'\n\nclass Invoice(Document):\n    pass\n\nprint(Invoice().label())"},
                    {"label": "Override method", "code": "class Document:\n    def label(self):\n        return 'Document'\n\nclass Invoice(Document):\n    def label(self):\n        return 'Invoice'\n\nprint(Invoice().label())"},
                ],
            },
            {
                "id": "P-SUPER",
                "title": "super",
                "points": [
                    "super calls behavior from a parent class.",
                    "Use it when extending a method instead of replacing everything.",
                    "In Odoo, forgetting super can skip important framework behavior.",
                ],
                "examples": [
                    {"label": "Extend parent method", "code": "class Base:\n    def label(self):\n        return 'Base'\n\nclass Child(Base):\n    def label(self):\n        return super().label() + ' Child'\n\nprint(Child().label())"},
                    {"label": "Extend setup", "code": "class Base:\n    def __init__(self):\n        self.ready = True\n\nclass Child(Base):\n    def __init__(self):\n        super().__init__()\n        self.name = 'custom'\n\nprint(Child().ready)"},
                ],
            },
            {
                "id": "P-TRY-EXCEPT",
                "title": "try and except",
                "points": [
                    "try runs code that may fail.",
                    "except handles a specific error so the program can respond.",
                    "Catch expected errors and avoid hiding problems silently.",
                ],
                "examples": [
                    {"label": "Handle bad number", "code": "try:\n    quantity = int('five')\nexcept ValueError:\n    print('quantity must be a number')"},
                    {"label": "Handle missing key", "code": "vals = {}\ntry:\n    print(vals['name'])\nexcept KeyError:\n    print('name is missing')"},
                ],
            },
            {
                "id": "P-MODULES-IMPORT",
                "title": "Modules and import",
                "points": [
                    "A module is a Python file that can be imported by other code.",
                    "import loads names from modules so you can reuse existing functionality.",
                    "Odoo addons are organized as Python packages and modules.",
                ],
                "examples": [
                    {"label": "Import a standard module", "code": "import datetime\nprint(datetime.date.today())"},
                    {"label": "Import one name", "code": "from pathlib import Path\nprint(Path.cwd())"},
                ],
            },
            {
                "id": "P-VENV",
                "title": "Virtual environments",
                "points": [
                    "A virtual environment keeps Python packages separate for one project.",
                    "It helps avoid conflicts between system packages and project packages.",
                    "Activate the environment before installing or running project code.",
                ],
                "examples": [
                    {"label": "Create environment", "code": "python3 -m venv .venv"},
                    {"label": "Activate environment", "code": "source .venv/bin/activate"},
                ],
            },
            {
                "id": "P-PIP",
                "title": "pip install",
                "points": [
                    "pip installs Python packages into the active environment.",
                    "Use python -m pip so pip belongs to the interpreter you are using.",
                    "For projects, record dependencies in a requirements file.",
                ],
                "examples": [
                    {"label": "Install a package", "code": "python3 -m pip install requests"},
                    {"label": "Install requirements", "code": "python3 -m pip install -r requirements.txt"},
                ],
            },
            {
                "id": "P-READING-ERRORS",
                "title": "Reading Python errors",
                "points": [
                    "Python tracebacks show where an error happened and what type it was.",
                    "Read from the bottom for the final error message.",
                    "Then scan upward to find your code path that led to the error.",
                ],
                "examples": [
                    {"label": "Cause a NameError", "code": "print(missing_name)"},
                    {"label": "Cause a TypeError", "code": "print('Total: ' + 10)"},
                ],
            },
            {
                "id": "P-DEBUGGING",
                "title": "Debugging basics",
                "points": [
                    "Debugging means finding why actual behavior differs from expected behavior.",
                    "Print small facts such as type, value, and branch taken.",
                    "Change one thing at a time so you know what affected the result.",
                ],
                "examples": [
                    {"label": "Print value and type", "code": "amount = '100'\nprint(amount, type(amount))"},
                    {"label": "Use breakpoint", "code": "amount = 100\nbreakpoint()\nprint(amount * 2)"},
                ],
            },
            {
                "id": "P-ODOO-HABITS",
                "title": "Python habits for Odoo",
                "points": [
                    "Write small readable methods that match Odoo model responsibilities.",
                    "Prefer clear names for recordsets, dictionaries, and computed values.",
                    "Restart, upgrade, and read logs when testing server-side code changes.",
                    "Keep framework behavior in mind before overriding methods.",
                ],
                "examples": [
                    {"label": "Name values clearly", "code": "partner_vals = {'name': 'Agrolait', 'customer_rank': 1}"},
                    {"label": "Use a readable helper", "code": "def is_large_invoice(amount):\n    return amount >= 1000"},
                ],
            },
        ],
    },
]

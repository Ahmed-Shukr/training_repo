"""Beginner-friendly PostgreSQL slide content."""

SLIDES = [
    {
        "section": 1,
        "title": "Install PostgreSQL on Ubuntu",
        "topics": [
            {
                "id": "DB-01",
                "title": "Install PostgreSQL on Ubuntu",
                "points": [
                    "Use apt for a standard Ubuntu install.",
                    "Install contrib tools for common extensions.",
                    "Verify the version after installation.",
                ],
                "examples": [
                    {
                        "label": "Install packages",
                        "code": "sudo apt update\nsudo apt install -y postgresql postgresql-contrib",
                    },
                    {
                        "label": "Check installed version",
                        "code": "psql --version\nsudo -u postgres psql -c \"SELECT version();\"",
                    },
                ],
            }
        ],
    },
    {
        "section": 2,
        "title": "Start and Check Service",
        "topics": [
            {
                "id": "DB-02",
                "title": "Start and Check the PostgreSQL Service",
                "points": [
                    "PostgreSQL usually runs as a systemd service.",
                    "Enable the service to start after reboot.",
                    "Check status before testing applications.",
                ],
                "examples": [
                    {
                        "label": "Start service",
                        "code": "sudo systemctl enable --now postgresql",
                    },
                    {
                        "label": "View status",
                        "code": "systemctl status postgresql --no-pager",
                    },
                ],
            }
        ],
    },
    {
        "section": 3,
        "title": "Connect with psql",
        "topics": [
            {
                "id": "DB-03",
                "title": "Connect with psql",
                "points": [
                    "psql is the main PostgreSQL command-line client.",
                    "Local admin access often uses the postgres OS user.",
                    "Use \\conninfo to confirm the connection.",
                ],
                "examples": [
                    {
                        "label": "Connect as postgres",
                        "code": "sudo -u postgres psql",
                    },
                    {
                        "label": "Connect to a database",
                        "code": "psql -h 127.0.0.1 -U odoo17 -d postgres\n\\conninfo",
                    },
                ],
            }
        ],
    },
    {
        "section": 4,
        "title": "Create a Role",
        "topics": [
            {
                "id": "DB-04",
                "title": "Create a PostgreSQL Role",
                "points": [
                    "Roles are database identities.",
                    "LOGIN lets a role connect like a user.",
                    "Give only the privileges the role needs.",
                ],
                "examples": [
                    {
                        "label": "Create login role",
                        "code": "sudo -u postgres createuser --pwprompt app_user",
                    },
                    {
                        "label": "Create role with SQL",
                        "code": "CREATE ROLE app_user LOGIN PASSWORD 'change-me';",
                    },
                ],
            }
        ],
    },
    {
        "section": 5,
        "title": "Create a Database",
        "topics": [
            {
                "id": "DB-05",
                "title": "Create a Database",
                "points": [
                    "A database stores schemas, tables, and data.",
                    "Set the owner when the database is created.",
                    "Use clear names for training and development.",
                ],
                "examples": [
                    {
                        "label": "Create with createdb",
                        "code": "sudo -u postgres createdb -O app_user training_db",
                    },
                    {
                        "label": "Create with SQL",
                        "code": "CREATE DATABASE training_db OWNER app_user;",
                    },
                ],
            }
        ],
    },
    {
        "section": 6,
        "title": "Grant Permissions",
        "topics": [
            {
                "id": "DB-06",
                "title": "Grant Database Permissions",
                "points": [
                    "Grants control what a role can do.",
                    "Database grants are not the same as table grants.",
                    "Review broad privileges before production use.",
                ],
                "examples": [
                    {
                        "label": "Grant database access",
                        "code": "GRANT CONNECT ON DATABASE training_db TO app_user;",
                    },
                    {
                        "label": "Grant schema access",
                        "code": "GRANT USAGE, CREATE ON SCHEMA public TO app_user;",
                    },
                ],
            }
        ],
    },
    {
        "section": 7,
        "title": "List Databases and Tables",
        "topics": [
            {
                "id": "DB-07",
                "title": "List Databases and Tables",
                "points": [
                    "psql meta commands start with a backslash.",
                    "\\l lists databases.",
                    "\\dt lists tables in the current database.",
                ],
                "examples": [
                    {
                        "label": "List databases",
                        "code": "\\l",
                    },
                    {
                        "label": "List tables",
                        "code": "\\c training_db\n\\dt",
                    },
                ],
            }
        ],
    },
    {
        "section": 8,
        "title": "Data Types Overview",
        "topics": [
            {
                "id": "DB-08",
                "title": "Data Types Overview",
                "points": [
                    "Choose types that match the meaning of data.",
                    "Use text types for names and descriptions.",
                    "Use numeric and date types for calculations.",
                ],
                "examples": [
                    {
                        "label": "Common text and number types",
                        "code": "name varchar(100)\nnotes text\nquantity integer\nprice numeric(10, 2)",
                    },
                    {
                        "label": "Common date and flag types",
                        "code": "is_active boolean\ncreated_on date\ncreated_at timestamp",
                    },
                ],
            }
        ],
    },
    {
        "section": 9,
        "title": "Create a Table",
        "topics": [
            {
                "id": "DB-09",
                "title": "Create a Table",
                "points": [
                    "Tables define columns and constraints.",
                    "Use consistent names for columns.",
                    "Start small and add constraints intentionally.",
                ],
                "examples": [
                    {
                        "label": "Simple table",
                        "code": "CREATE TABLE customers (\n    id integer,\n    name text,\n    email text\n);",
                    },
                    {
                        "label": "Table with defaults",
                        "code": "CREATE TABLE notes (\n    id integer,\n    body text,\n    created_at timestamp DEFAULT now()\n);",
                    },
                ],
            }
        ],
    },
    {
        "section": 10,
        "title": "Primary Key",
        "topics": [
            {
                "id": "DB-10",
                "title": "Use a Primary Key",
                "points": [
                    "A primary key uniquely identifies each row.",
                    "It cannot be null.",
                    "Most tables should have one primary key.",
                ],
                "examples": [
                    {
                        "label": "Identity primary key",
                        "code": "CREATE TABLE products (\n    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,\n    name text NOT NULL\n);",
                    },
                    {
                        "label": "Natural primary key",
                        "code": "CREATE TABLE countries (\n    code char(2) PRIMARY KEY,\n    name text NOT NULL\n);",
                    },
                ],
            }
        ],
    },
    {
        "section": 11,
        "title": "Foreign Key",
        "topics": [
            {
                "id": "DB-11",
                "title": "Use a Foreign Key",
                "points": [
                    "A foreign key links one table to another.",
                    "It protects data from broken references.",
                    "Name relationship columns clearly.",
                ],
                "examples": [
                    {
                        "label": "Customer orders",
                        "code": "CREATE TABLE orders (\n    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,\n    customer_id bigint REFERENCES customers(id)\n);",
                    },
                    {
                        "label": "Required relationship",
                        "code": "product_id bigint NOT NULL REFERENCES products(id)",
                    },
                ],
            }
        ],
    },
    {
        "section": 12,
        "title": "Insert Rows",
        "topics": [
            {
                "id": "DB-12",
                "title": "Insert Data",
                "points": [
                    "INSERT adds new rows.",
                    "List columns to avoid order mistakes.",
                    "Use RETURNING to see created values.",
                ],
                "examples": [
                    {
                        "label": "Insert one row",
                        "code": "INSERT INTO customers (name, email)\nVALUES ('Ada', 'ada@example.com');",
                    },
                    {
                        "label": "Insert and return id",
                        "code": "INSERT INTO products (name)\nVALUES ('Keyboard')\nRETURNING id, name;",
                    },
                ],
            }
        ],
    },
    {
        "section": 13,
        "title": "Select Rows",
        "topics": [
            {
                "id": "DB-13",
                "title": "Read Data with SELECT",
                "points": [
                    "SELECT reads rows from tables.",
                    "Choose only the columns you need.",
                    "Use ORDER BY for predictable order.",
                ],
                "examples": [
                    {
                        "label": "Select columns",
                        "code": "SELECT id, name, email\nFROM customers;",
                    },
                    {
                        "label": "Sort results",
                        "code": "SELECT name, price\nFROM products\nORDER BY name;",
                    },
                ],
            }
        ],
    },
    {
        "section": 14,
        "title": "Update Rows",
        "topics": [
            {
                "id": "DB-14",
                "title": "Update Data",
                "points": [
                    "UPDATE changes existing rows.",
                    "Always check the WHERE clause.",
                    "RETURNING can show changed rows.",
                ],
                "examples": [
                    {
                        "label": "Update one customer",
                        "code": "UPDATE customers\nSET email = 'ada.new@example.com'\nWHERE id = 1;",
                    },
                    {
                        "label": "Update and review",
                        "code": "UPDATE products\nSET price = 19.99\nWHERE name = 'Keyboard'\nRETURNING id, name, price;",
                    },
                ],
            }
        ],
    },
    {
        "section": 15,
        "title": "Delete Rows",
        "topics": [
            {
                "id": "DB-15",
                "title": "Delete Data",
                "points": [
                    "DELETE removes rows from a table.",
                    "Use WHERE to target specific rows.",
                    "Test with SELECT before deleting.",
                ],
                "examples": [
                    {
                        "label": "Delete one row",
                        "code": "DELETE FROM customers\nWHERE id = 10;",
                    },
                    {
                        "label": "Preview then delete",
                        "code": "SELECT * FROM products WHERE name = 'Old Item';\nDELETE FROM products WHERE name = 'Old Item';",
                    },
                ],
            }
        ],
    },
    {
        "section": 16,
        "title": "Filter with WHERE",
        "topics": [
            {
                "id": "DB-16",
                "title": "Filter Rows with WHERE",
                "points": [
                    "WHERE limits which rows are returned.",
                    "Combine filters with AND and OR.",
                    "Use parentheses for clear logic.",
                ],
                "examples": [
                    {
                        "label": "One condition",
                        "code": "SELECT * FROM customers\nWHERE email IS NOT NULL;",
                    },
                    {
                        "label": "Multiple conditions",
                        "code": "SELECT * FROM products\nWHERE price > 10 AND is_active = true;",
                    },
                ],
            }
        ],
    },
    {
        "section": 17,
        "title": "LIKE and ILIKE",
        "topics": [
            {
                "id": "DB-17",
                "title": "Search Text with LIKE and ILIKE",
                "points": [
                    "LIKE matches text patterns.",
                    "ILIKE ignores letter case.",
                    "The percent sign matches any text.",
                ],
                "examples": [
                    {
                        "label": "Case-sensitive search",
                        "code": "SELECT name FROM customers\nWHERE name LIKE 'A%';",
                    },
                    {
                        "label": "Case-insensitive search",
                        "code": "SELECT name FROM customers\nWHERE name ILIKE '%smith%';",
                    },
                ],
            }
        ],
    },
    {
        "section": 18,
        "title": "IN and BETWEEN",
        "topics": [
            {
                "id": "DB-18",
                "title": "Filter with IN and BETWEEN",
                "points": [
                    "IN checks a value against a list.",
                    "BETWEEN checks an inclusive range.",
                    "These filters keep SQL readable.",
                ],
                "examples": [
                    {
                        "label": "Use IN",
                        "code": "SELECT * FROM orders\nWHERE status IN ('draft', 'sent');",
                    },
                    {
                        "label": "Use BETWEEN",
                        "code": "SELECT * FROM invoices\nWHERE amount_total BETWEEN 100 AND 500;",
                    },
                ],
            }
        ],
    },
    {
        "section": 19,
        "title": "Inner Join",
        "topics": [
            {
                "id": "DB-19",
                "title": "Combine Rows with INNER JOIN",
                "points": [
                    "INNER JOIN returns matching rows only.",
                    "Join conditions usually compare keys.",
                    "Use table aliases for shorter SQL.",
                ],
                "examples": [
                    {
                        "label": "Orders with customers",
                        "code": "SELECT o.id, c.name\nFROM orders o\nINNER JOIN customers c ON c.id = o.customer_id;",
                    },
                    {
                        "label": "Lines with products",
                        "code": "SELECT l.id, p.name\nFROM order_lines l\nJOIN products p ON p.id = l.product_id;",
                    },
                ],
            }
        ],
    },
    {
        "section": 20,
        "title": "Left Join",
        "topics": [
            {
                "id": "DB-20",
                "title": "Keep Rows with LEFT JOIN",
                "points": [
                    "LEFT JOIN keeps all rows from the left table.",
                    "Missing matches appear as null values.",
                    "It is useful for optional relationships.",
                ],
                "examples": [
                    {
                        "label": "Customers with optional orders",
                        "code": "SELECT c.name, o.id AS order_id\nFROM customers c\nLEFT JOIN orders o ON o.customer_id = c.id;",
                    },
                    {
                        "label": "Products with optional categories",
                        "code": "SELECT p.name, c.name AS category\nFROM products p\nLEFT JOIN categories c ON c.id = p.category_id;",
                    },
                ],
            }
        ],
    },
    {
        "section": 21,
        "title": "Group By",
        "topics": [
            {
                "id": "DB-21",
                "title": "Group Rows with GROUP BY",
                "points": [
                    "GROUP BY collects rows into groups.",
                    "Use aggregates to summarize each group.",
                    "Every selected non-aggregate column must be grouped.",
                ],
                "examples": [
                    {
                        "label": "Orders by status",
                        "code": "SELECT status, COUNT(*)\nFROM orders\nGROUP BY status;",
                    },
                    {
                        "label": "Sales by customer",
                        "code": "SELECT customer_id, SUM(amount_total)\nFROM invoices\nGROUP BY customer_id;",
                    },
                ],
            }
        ],
    },
    {
        "section": 22,
        "title": "Having",
        "topics": [
            {
                "id": "DB-22",
                "title": "Filter Groups with HAVING",
                "points": [
                    "HAVING filters grouped results.",
                    "WHERE filters rows before grouping.",
                    "Use HAVING with aggregate conditions.",
                ],
                "examples": [
                    {
                        "label": "Customers with many orders",
                        "code": "SELECT customer_id, COUNT(*)\nFROM orders\nGROUP BY customer_id\nHAVING COUNT(*) > 3;",
                    },
                    {
                        "label": "Large sales groups",
                        "code": "SELECT customer_id, SUM(amount_total)\nFROM invoices\nGROUP BY customer_id\nHAVING SUM(amount_total) >= 1000;",
                    },
                ],
            }
        ],
    },
    {
        "section": 23,
        "title": "Count Sum Avg",
        "topics": [
            {
                "id": "DB-23",
                "title": "Use COUNT, SUM, and AVG",
                "points": [
                    "COUNT counts rows or values.",
                    "SUM adds numeric values.",
                    "AVG calculates an average.",
                ],
                "examples": [
                    {
                        "label": "Count rows",
                        "code": "SELECT COUNT(*) AS order_count\nFROM orders;",
                    },
                    {
                        "label": "Sales summary",
                        "code": "SELECT SUM(amount_total), AVG(amount_total)\nFROM invoices;",
                    },
                ],
            }
        ],
    },
    {
        "section": 24,
        "title": "Create Index",
        "topics": [
            {
                "id": "DB-24",
                "title": "Create an Index",
                "points": [
                    "Indexes help PostgreSQL find rows faster.",
                    "Index columns used often in filters or joins.",
                    "Too many indexes slow writes.",
                ],
                "examples": [
                    {
                        "label": "Index a search column",
                        "code": "CREATE INDEX idx_customers_email ON customers (email);",
                    },
                    {
                        "label": "Index a foreign key",
                        "code": "CREATE INDEX idx_orders_customer_id ON orders (customer_id);",
                    },
                ],
            }
        ],
    },
    {
        "section": 25,
        "title": "Explain Analyze",
        "topics": [
            {
                "id": "DB-25",
                "title": "Read Plans with EXPLAIN ANALYZE",
                "points": [
                    "EXPLAIN shows how PostgreSQL plans a query.",
                    "ANALYZE runs the query and measures time.",
                    "Use it carefully on changing queries.",
                ],
                "examples": [
                    {
                        "label": "Inspect a select",
                        "code": "EXPLAIN ANALYZE\nSELECT * FROM customers WHERE email = 'ada@example.com';",
                    },
                    {
                        "label": "Inspect a join",
                        "code": "EXPLAIN ANALYZE\nSELECT o.id, c.name\nFROM orders o\nJOIN customers c ON c.id = o.customer_id;",
                    },
                ],
            }
        ],
    },
    {
        "section": 26,
        "title": "Backup with pg_dump",
        "topics": [
            {
                "id": "DB-26",
                "title": "Back Up with pg_dump",
                "points": [
                    "pg_dump creates a logical backup.",
                    "Custom format is flexible for restore.",
                    "Store backups outside the database server.",
                ],
                "examples": [
                    {
                        "label": "Custom format backup",
                        "code": "pg_dump -h 127.0.0.1 -U odoo17 -Fc -f odoo17.dump odoo17_prod",
                    },
                    {
                        "label": "Plain SQL backup",
                        "code": "pg_dump -U odoo17 -f training_db.sql training_db",
                    },
                ],
            }
        ],
    },
    {
        "section": 27,
        "title": "Restore with pg_restore",
        "topics": [
            {
                "id": "DB-27",
                "title": "Restore with pg_restore",
                "points": [
                    "pg_restore reads custom-format dumps.",
                    "Restore into the correct target database.",
                    "Test restores before an emergency.",
                ],
                "examples": [
                    {
                        "label": "Create target database",
                        "code": "createdb -h 127.0.0.1 -U odoo17 odoo17_restore",
                    },
                    {
                        "label": "Restore dump",
                        "code": "pg_restore -h 127.0.0.1 -U odoo17 -d odoo17_restore odoo17.dump",
                    },
                ],
            }
        ],
    },
    {
        "section": 28,
        "title": "pg_hba.conf Idea",
        "topics": [
            {
                "id": "DB-28",
                "title": "Understand the pg_hba.conf Idea",
                "points": [
                    "pg_hba.conf controls client authentication.",
                    "Rules are checked from top to bottom.",
                    "Reload PostgreSQL after safe changes.",
                ],
                "examples": [
                    {
                        "label": "Local password rule",
                        "code": "host    all    odoo17    127.0.0.1/32    scram-sha-256",
                    },
                    {
                        "label": "Reload configuration",
                        "code": "sudo systemctl reload postgresql",
                    },
                ],
            }
        ],
    },
    {
        "section": 29,
        "title": "postgresql.conf Idea",
        "topics": [
            {
                "id": "DB-29",
                "title": "Understand the postgresql.conf Idea",
                "points": [
                    "postgresql.conf controls server behavior.",
                    "Common settings include port and listen address.",
                    "Some changes require restart, not reload.",
                ],
                "examples": [
                    {
                        "label": "Listen locally",
                        "code": "listen_addresses = 'localhost'\nport = 5432",
                    },
                    {
                        "label": "Show config file",
                        "code": "SHOW config_file;\nSHOW listen_addresses;",
                    },
                ],
            }
        ],
    },
    {
        "section": 30,
        "title": "See Connections",
        "topics": [
            {
                "id": "DB-30",
                "title": "See Active Connections",
                "points": [
                    "pg_stat_activity shows current sessions.",
                    "It helps identify users, databases, and queries.",
                    "Filter it when many sessions exist.",
                ],
                "examples": [
                    {
                        "label": "View active sessions",
                        "code": "SELECT pid, usename, datname, state\nFROM pg_stat_activity;",
                    },
                    {
                        "label": "Find Odoo sessions",
                        "code": "SELECT pid, state, query\nFROM pg_stat_activity\nWHERE usename = 'odoo17';",
                    },
                ],
            }
        ],
    },
    {
        "section": 31,
        "title": "Cancel or Terminate Query",
        "topics": [
            {
                "id": "DB-31",
                "title": "Cancel or Terminate a Query",
                "points": [
                    "Cancel asks a query to stop cleanly.",
                    "Terminate closes the whole session.",
                    "Confirm the PID before acting.",
                ],
                "examples": [
                    {
                        "label": "Cancel a query",
                        "code": "SELECT pg_cancel_backend(12345);",
                    },
                    {
                        "label": "Terminate a session",
                        "code": "SELECT pg_terminate_backend(12345);",
                    },
                ],
            }
        ],
    },
    {
        "section": 32,
        "title": "Odoo Database User Habit",
        "topics": [
            {
                "id": "DB-32",
                "title": "Use a Dedicated Odoo Database User",
                "points": [
                    "Do not run Odoo as the postgres superuser.",
                    "Use one clear role for each Odoo environment.",
                    "Grant CREATEDB only when it is needed.",
                ],
                "examples": [
                    {
                        "label": "Development role",
                        "code": "CREATE ROLE odoo17_dev LOGIN CREATEDB PASSWORD 'change-me';",
                    },
                    {
                        "label": "Connection options",
                        "code": "db_user = odoo17_dev\ndb_password = change-me\ndb_host = 127.0.0.1",
                    },
                ],
            }
        ],
    },
    {
        "section": 33,
        "title": "Odoo Backup Habit",
        "topics": [
            {
                "id": "DB-33",
                "title": "Keep a Backup Habit for Odoo",
                "points": [
                    "Back up before upgrades and migrations.",
                    "Keep database and filestore backups together.",
                    "Practice restoring backups regularly.",
                ],
                "examples": [
                    {
                        "label": "Database backup",
                        "code": "pg_dump -U odoo17 -Fc -f before_upgrade.dump odoo17_prod",
                    },
                    {
                        "label": "Filestore backup",
                        "code": "tar -czf filestore_before_upgrade.tgz ~/.local/share/Odoo/filestore/odoo17_prod",
                    },
                ],
            }
        ],
    },
]

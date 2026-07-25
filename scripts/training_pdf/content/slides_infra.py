#!/usr/bin/env python3
"""Atomic beginner-friendly slides for Odoo infrastructure."""


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
        "title": "Docker Fundamentals",
        "topics": [
            _topic(
                "INF-01",
                "Containers vs VMs",
                [
                    "A container packages an app process and its dependencies.",
                    "A VM packages a full guest operating system.",
                    "Containers are lighter, but the host still matters.",
                ],
                [
                    {
                        "label": "Container mental model",
                        "code": """app process + image filesystem + mounted volumes""",
                    },
                    {
                        "label": "VM mental model",
                        "code": """guest OS + virtual disk + virtual network + app""",
                    },
                ],
            ),
            _topic(
                "INF-02",
                "Install Docker",
                [
                    "Install Docker from trusted package sources.",
                    "Verify both the engine and compose plugin.",
                    "Only trusted administrators should use the docker group.",
                ],
                [
                    {
                        "label": "Version checks",
                        "code": """docker --version
docker compose version""",
                    },
                    {
                        "label": "Service check",
                        "code": """sudo systemctl enable --now docker
sudo systemctl status docker""",
                    },
                ],
            ),
            _topic(
                "INF-03",
                "docker run, ps, and logs",
                [
                    "docker run starts a container from an image.",
                    "docker ps shows running containers.",
                    "docker logs is the first place to inspect startup errors.",
                ],
                [
                    {
                        "label": "Run a test container",
                        "code": """docker run --rm hello-world""",
                    },
                    {
                        "label": "Inspect containers",
                        "code": """docker ps
docker logs odoo-web""",
                    },
                ],
            ),
            _topic(
                "INF-04",
                "Images vs Containers",
                [
                    "An image is the reusable blueprint.",
                    "A container is a running or stopped instance.",
                    "Removing a container should not remove persistent data.",
                ],
                [
                    {
                        "label": "List images",
                        "code": """docker images""",
                    },
                    {
                        "label": "List all containers",
                        "code": """docker ps -a""",
                    },
                ],
            ),
            _topic(
                "INF-05",
                "Dockerfile Odoo Idea",
                [
                    "A Dockerfile documents how to build a custom Odoo image.",
                    "Install Python and system dependencies in the image.",
                    "Keep addons and configuration separate from database data.",
                ],
                [
                    {
                        "label": "Minimal base",
                        "code": """FROM odoo:18
USER root
RUN pip3 install --break-system-packages openpyxl
USER odoo""",
                    },
                    {
                        "label": "Copy addons",
                        "code": """COPY ./custom_addons /mnt/extra-addons""",
                    },
                ],
            ),
            _topic(
                "INF-06",
                "Volumes",
                [
                    "Volumes keep data outside disposable containers.",
                    "Odoo needs persistence for filestore and PostgreSQL data.",
                    "Back up volumes before upgrades.",
                ],
                [
                    {
                        "label": "Named volume",
                        "code": """volumes:
  odoo-data:
  pg-data:""",
                    },
                    {
                        "label": "Mount volume",
                        "code": """services:
  web:
    volumes:
      - odoo-data:/var/lib/odoo""",
                    },
                ],
            ),
            _topic(
                "INF-07",
                "Docker Network",
                [
                    "Docker networks let containers reach each other by service name.",
                    "Keep databases off the public internet.",
                    "Expose only the ports users or proxies need.",
                ],
                [
                    {
                        "label": "Compose network",
                        "code": """networks:
  odoo-net:""",
                    },
                    {
                        "label": "Database host name",
                        "code": """db_host = db
db_port = 5432""",
                    },
                ],
            ),
            _topic(
                "INF-08",
                "Compose File",
                [
                    "Compose describes multiple services in one YAML file.",
                    "It is useful for Odoo, PostgreSQL, and helper services.",
                    "Commit safe defaults, not secrets.",
                ],
                [
                    {
                        "label": "Compose command",
                        "code": """docker compose up -d
docker compose ps""",
                    },
                    {
                        "label": "Service skeleton",
                        "code": """services:
  web:
    image: odoo:18
  db:
    image: postgres:16""",
                    },
                ],
            ),
            _topic(
                "INF-09",
                "Odoo and PostgreSQL Compose",
                [
                    "Odoo needs a PostgreSQL database service.",
                    "Use environment variables for database connection settings.",
                    "Persist both Odoo and PostgreSQL data.",
                ],
                [
                    {
                        "label": "Odoo service",
                        "code": """web:
  image: odoo:18
  depends_on:
    - db
  ports:
    - "8069:8069" """,
                    },
                    {
                        "label": "PostgreSQL service",
                        "code": """db:
  image: postgres:16
  environment:
    POSTGRES_DB: postgres
    POSTGRES_USER: odoo""",
                    },
                ],
            ),
            _topic(
                "INF-10",
                ".env File",
                [
                    ".env keeps environment-specific values out of compose YAML.",
                    "Do not commit real production secrets.",
                    "Use clear variable names.",
                ],
                [
                    {
                        "label": "Example .env",
                        "code": """ODOO_PORT=8069
POSTGRES_USER=odoo
POSTGRES_PASSWORD=change_me""",
                    },
                    {
                        "label": "Compose reference",
                        "code": """ports:
  - "${ODOO_PORT}:8069"
environment:
  POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}""",
                    },
                ],
            ),
            _topic(
                "INF-11",
                "Upgrade Containers Safely",
                [
                    "Back up the database and filestore before upgrading.",
                    "Pull new images in staging first.",
                    "Keep a rollback path for the previous version.",
                ],
                [
                    {
                        "label": "Pull and restart",
                        "code": """docker compose pull
docker compose up -d""",
                    },
                    {
                        "label": "Backup first",
                        "code": """pg_dump -Fc odoo_prod > odoo_prod.dump
tar -czf filestore.tgz /var/lib/odoo/filestore""",
                    },
                ],
            ),
        ],
    },
    {
        "section": 2,
        "title": "VPS and Reverse Proxy",
        "topics": [
            _topic(
                "INF-12",
                "Choose VPS Specs",
                [
                    "Size the VPS for users, workers, database, and backups.",
                    "Prefer SSD storage for PostgreSQL.",
                    "Leave room for growth and maintenance tasks.",
                ],
                [
                    {
                        "label": "Small training host",
                        "code": """2 vCPU
4 GB RAM
60 GB SSD""",
                    },
                    {
                        "label": "Busier host",
                        "code": """4 to 8 vCPU
16 GB RAM
separate backup storage""",
                    },
                ],
            ),
            _topic(
                "INF-13",
                "SSH Hardening",
                [
                    "Use SSH keys instead of passwords.",
                    "Disable direct root login when possible.",
                    "Keep a tested recovery path before changing access.",
                ],
                [
                    {
                        "label": "sshd settings",
                        "code": """PasswordAuthentication no
PermitRootLogin no""",
                    },
                    {
                        "label": "Reload SSH",
                        "code": """sudo sshd -t
sudo systemctl reload ssh""",
                    },
                ],
            ),
            _topic(
                "INF-14",
                "/opt/odoo Layout",
                [
                    "A predictable directory layout helps operations.",
                    "Separate config, addons, backups, and logs.",
                    "Document ownership and permissions.",
                ],
                [
                    {
                        "label": "Common layout",
                        "code": """/opt/odoo/
  config/
  custom_addons/
  backups/
  logs/""",
                    },
                    {
                        "label": "Ownership idea",
                        "code": """sudo chown -R odoo:odoo /opt/odoo""",
                    },
                ],
            ),
            _topic(
                "INF-15",
                "Nginx Reverse Proxy",
                [
                    "Nginx receives public HTTP traffic.",
                    "It forwards requests to Odoo on the private port.",
                    "It also handles TLS, headers, and upload limits.",
                ],
                [
                    {
                        "label": "Server block",
                        "code": """server {
    server_name odoo.example.com;
    location / {
        proxy_pass http://127.0.0.1:8069;
    }
}""",
                    },
                    {
                        "label": "Test config",
                        "code": """sudo nginx -t
sudo systemctl reload nginx""",
                    },
                ],
            ),
            _topic(
                "INF-16",
                "Proxy to 8069",
                [
                    "Port 8069 is the normal Odoo HTTP port.",
                    "Expose it only to Nginx on production hosts.",
                    "Set proxy_mode in Odoo when using a proxy.",
                ],
                [
                    {
                        "label": "Nginx proxy",
                        "code": """location / {
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_pass http://127.0.0.1:8069;
}""",
                    },
                    {
                        "label": "Odoo config",
                        "code": """proxy_mode = True
xmlrpc_port = 8069""",
                    },
                ],
            ),
            _topic(
                "INF-17",
                "Longpolling 8072",
                [
                    "Odoo uses a separate longpolling or websocket endpoint.",
                    "Route the longpolling path to port 8072 when configured.",
                    "Chat and live updates depend on this path.",
                ],
                [
                    {
                        "label": "Nginx longpolling",
                        "code": """location /longpolling {
    proxy_pass http://127.0.0.1:8072;
}""",
                    },
                    {
                        "label": "Odoo port",
                        "code": """longpolling_port = 8072""",
                    },
                ],
            ),
            _topic(
                "INF-18",
                "Certbot SSL",
                [
                    "Certbot can issue Let's Encrypt certificates.",
                    "Use HTTPS for every production Odoo site.",
                    "Verify automatic renewal.",
                ],
                [
                    {
                        "label": "Issue certificate",
                        "code": """sudo certbot --nginx -d odoo.example.com""",
                    },
                    {
                        "label": "Renewal check",
                        "code": """sudo certbot renew --dry-run""",
                    },
                ],
            ),
            _topic(
                "INF-19",
                "systemd odoo.service",
                [
                    "systemd keeps an Odoo process running on a VPS.",
                    "It defines the user, command, and restart behavior.",
                    "Logs can be viewed with journalctl.",
                ],
                [
                    {
                        "label": "Service command",
                        "code": """[Service]
User=odoo
ExecStart=/opt/odoo/venv/bin/python /opt/odoo/odoo-bin -c /etc/odoo.conf
Restart=always""",
                    },
                    {
                        "label": "Operate service",
                        "code": """sudo systemctl enable --now odoo
journalctl -u odoo -f""",
                    },
                ],
            ),
            _topic(
                "INF-20",
                "Cron Backup",
                [
                    "Backups should run automatically.",
                    "Include both database dump and filestore.",
                    "Test restores on another host.",
                ],
                [
                    {
                        "label": "Cron line",
                        "code": """0 2 * * * /opt/odoo/scripts/backup.sh""",
                    },
                    {
                        "label": "Backup script idea",
                        "code": """pg_dump -Fc odoo_prod > /backup/odoo_prod.dump
tar -czf /backup/filestore.tgz /var/lib/odoo/filestore""",
                    },
                ],
            ),
        ],
    },
    {
        "section": 3,
        "title": "Odoo Performance Settings",
        "topics": [
            _topic(
                "INF-21",
                "Workers Idea",
                [
                    "Workers let Odoo handle multiple requests in parallel.",
                    "Production deployments usually use workers.",
                    "Cron workers and HTTP workers need enough memory.",
                ],
                [
                    {
                        "label": "Worker setting",
                        "code": """workers = 5
max_cron_threads = 1""",
                    },
                    {
                        "label": "No workers",
                        "code": """workers = 0
# common in simple development setups""",
                    },
                ],
            ),
            _topic(
                "INF-22",
                "Calculate Workers",
                [
                    "A common starting formula is CPU cores * 2 + 1.",
                    "Adjust for memory, long requests, and cron load.",
                    "Measure real traffic before increasing blindly.",
                ],
                [
                    {
                        "label": "Formula",
                        "code": """workers = (cpu_cores * 2) + 1""",
                    },
                    {
                        "label": "Example",
                        "code": """2 CPU cores -> 5 workers
4 CPU cores -> 9 workers""",
                    },
                ],
            ),
            _topic(
                "INF-23",
                "Memory Limits",
                [
                    "Memory limits restart workers that grow too large.",
                    "Set limits based on available RAM and worker count.",
                    "Leave memory for PostgreSQL and the operating system.",
                ],
                [
                    {
                        "label": "Odoo limits",
                        "code": """limit_memory_soft = 2147483648
limit_memory_hard = 2684354560""",
                    },
                    {
                        "label": "Container limit",
                        "code": """deploy:
  resources:
    limits:
      memory: 4G""",
                    },
                ],
            ),
            _topic(
                "INF-24",
                "Time Limits",
                [
                    "Time limits stop requests that run too long.",
                    "They protect workers from being stuck forever.",
                    "Long imports may need a planned temporary setting.",
                ],
                [
                    {
                        "label": "Config values",
                        "code": """limit_time_cpu = 60
limit_time_real = 120""",
                    },
                    {
                        "label": "Import window idea",
                        "code": """# raise limits only during a controlled import
limit_time_real = 600""",
                    },
                ],
            ),
            _topic(
                "INF-25",
                "max_connections",
                [
                    "PostgreSQL max_connections must cover Odoo workers and tools.",
                    "Too many connections can waste memory.",
                    "Use pooling or careful sizing for larger systems.",
                ],
                [
                    {
                        "label": "PostgreSQL setting",
                        "code": """max_connections = 200""",
                    },
                    {
                        "label": "Odoo db setting",
                        "code": """db_maxconn = 64""",
                    },
                ],
            ),
            _topic(
                "INF-26",
                "Missing Indexes",
                [
                    "Missing indexes make common searches slow.",
                    "Look for slow queries before adding indexes.",
                    "Index fields used often in domains, joins, and sorting.",
                ],
                [
                    {
                        "label": "SQL index",
                        "code": """CREATE INDEX training_course_state_idx
ON training_course (state);""",
                    },
                    {
                        "label": "Odoo field index",
                        "code": """state = fields.Selection(
    selection=STATES,
    index=True,
)""",
                    },
                ],
            ),
            _topic(
                "INF-27",
                "pg_stat_statements",
                [
                    "pg_stat_statements records query statistics.",
                    "It helps find slow and frequent SQL.",
                    "Enable it before a performance incident if possible.",
                ],
                [
                    {
                        "label": "Enable extension",
                        "code": """CREATE EXTENSION IF NOT EXISTS pg_stat_statements;""",
                    },
                    {
                        "label": "Find slow queries",
                        "code": """SELECT calls, mean_exec_time, query
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;""",
                    },
                ],
            ),
            _topic(
                "INF-28",
                "Redis Sessions Idea",
                [
                    "Redis can store shared session or cache data in some designs.",
                    "It is useful when multiple Odoo instances need shared state.",
                    "Treat Redis as infrastructure that needs monitoring too.",
                ],
                [
                    {
                        "label": "Redis service",
                        "code": """redis:
  image: redis:7
  restart: unless-stopped""",
                    },
                    {
                        "label": "Session concept",
                        "code": """browser session -> load balancer -> Odoo nodes -> shared Redis""",
                    },
                ],
            ),
            _topic(
                "INF-29",
                "Load Balancing Idea",
                [
                    "Load balancing spreads traffic across Odoo nodes.",
                    "All nodes must share database and filestore strategy.",
                    "Start with one reliable node before adding more.",
                ],
                [
                    {
                        "label": "Upstream block",
                        "code": """upstream odoo_backend {
    server 10.0.0.11:8069;
    server 10.0.0.12:8069;
}""",
                    },
                    {
                        "label": "Proxy to upstream",
                        "code": """location / {
    proxy_pass http://odoo_backend;
}""",
                    },
                ],
            ),
            _topic(
                "INF-30",
                "Monitoring Overview",
                [
                    "Monitoring shows whether the system is healthy.",
                    "Track application, database, disk, and host metrics.",
                    "Alerts should point to an action a person can take.",
                ],
                [
                    {
                        "label": "Useful signals",
                        "code": """CPU, RAM, disk, HTTP errors, slow queries, backup age""",
                    },
                    {
                        "label": "Basic command checks",
                        "code": """df -h
free -m
systemctl status odoo""",
                    },
                ],
            ),
            _topic(
                "INF-31",
                "Logging Overview",
                [
                    "Logs explain what happened before and during failures.",
                    "Keep Odoo, Nginx, and PostgreSQL logs accessible.",
                    "Rotate logs so disks do not fill.",
                ],
                [
                    {
                        "label": "Odoo log config",
                        "code": """logfile = /var/log/odoo/odoo.log
log_level = info""",
                    },
                    {
                        "label": "Journal logs",
                        "code": """journalctl -u odoo --since "1 hour ago" """,
                    },
                ],
            ),
            _topic(
                "INF-32",
                "Restore Testing",
                [
                    "A backup is only useful if it can be restored.",
                    "Restore tests prove database and filestore backups match.",
                    "Schedule restore practice before emergencies.",
                ],
                [
                    {
                        "label": "Restore database",
                        "code": """createdb odoo_restore
pg_restore -d odoo_restore odoo_prod.dump""",
                    },
                    {
                        "label": "Restore filestore",
                        "code": """mkdir -p /var/lib/odoo/filestore/odoo_restore
tar -xzf filestore.tgz -C /var/lib/odoo/filestore/odoo_restore""",
                    },
                ],
            ),
        ],
    },
]

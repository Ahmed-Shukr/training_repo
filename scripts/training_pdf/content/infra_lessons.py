#!/usr/bin/env python3
"""Infrastructure lessons for the Odoo training PDF generator."""


def _explanation(title, theme, design, implementation, verification, production):
    return [
        (
            f"{title} is infrastructure work that directly affects reliability, data "
            f"safety, and developer speed. {theme} Senior engineers treat these topics "
            "as part of the product because users experience slow pages, broken backups, "
            "and unsafe upgrades as product failures."
        ),
        (
            f"The design decision starts by separating local development, staging, and "
            f"production needs. {design} The right architecture is the simplest one that "
            "can be restored, upgraded, monitored, and explained under incident pressure."
        ),
        (
            f"Implementation should be explicit and repeatable. {implementation} Prefer "
            "configuration files committed to the repository, secrets supplied by the "
            "environment, and operational commands that can be run by another engineer."
        ),
        (
            f"Verification must prove behavior, not only syntax. {verification} Test from "
            "a clean host or container, restart services, simulate failure paths, and "
            "confirm that logs and metrics expose enough information to diagnose issues."
        ),
        (
            f"In production, {title.lower()} choices become long-lived operational "
            f"contracts. {production} Document assumptions, keep rollback paths realistic, "
            "and automate the checks that humans are most likely to forget during a late "
            "maintenance window."
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
        "section": "infra",
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
        "I01",
        "Containers vs Virtual Machines",
        [
            "Explain the difference between OS virtualization and process isolation.",
            "Choose an appropriate runtime for Odoo development and deployment.",
            "Identify what containers do not solve.",
        ],
        "Containers package a process with its filesystem and dependencies, while virtual machines package an entire guest operating system.",
        "Use containers to make Odoo services repeatable and portable, but still design the host, network, storage, and backup strategy deliberately.",
        "Run Odoo, PostgreSQL, Nginx, and workers as separate services where appropriate and keep persistent data outside disposable container layers.",
        "Verify isolation assumptions by restarting containers, removing images, and confirming that database and filestore data remain intact.",
        "Containers reduce drift, but they do not replace monitoring, patching, secrets management, or restore testing.",
        [
            "Containers share the host kernel.",
            "VMs provide stronger OS-level separation.",
            "Container filesystems are disposable by design.",
            "Persistent data belongs in volumes or managed storage.",
            "Containers improve repeatability, not application design.",
        ],
        [
            {
                "title": "Mental model comparison",
                "code": '''# Container mindset
app process + image filesystem + mounted volumes + network namespace

# VM mindset
guest OS + kernel + virtual disk + virtual network + app processes''',
                "explain": "The model highlights why containers start quickly but still depend on host and storage decisions.",
            }
        ],
        [
            "Storing database data inside a disposable container layer.",
            "Assuming containers are automatically secure.",
            "Using one giant container for every service.",
            "Forgetting host-level patching and monitoring.",
        ],
        "Draw an architecture for local Odoo using containers and explain which files survive when the Odoo container is deleted.",
    ),
    _lesson(
        "I02",
        "Installing Docker Compose for Odoo Workloads",
        [
            "Install Docker Engine and Compose plugin.",
            "Verify versions and permissions.",
            "Prepare a host for repeatable compose projects.",
        ],
        "Docker Compose is the most common entry point for running Odoo, PostgreSQL, and supporting services together on a single host.",
        "Decide whether the host is for development or production because package sources, user permissions, filesystem paths, and firewall rules differ.",
        "Install Docker from official packages, enable the service, add only trusted operators to the docker group, and verify compose is available as docker compose.",
        "Run hello-world, inspect docker info, and create a minimal compose project to prove the daemon, plugin, network, and volume drivers work.",
        "A clean Docker installation prevents confusing deployment bugs where the application is blamed for host-level package or permission problems.",
        [
            "Use the Compose plugin command: docker compose.",
            "Membership in the docker group is root-equivalent.",
            "Pin host setup in documentation or automation.",
            "Verify daemon and compose versions.",
            "Keep production hosts minimal.",
        ],
        [
            {
                "title": "Ubuntu installation outline",
                "code": '''sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
  | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
docker compose version''',
                "explain": "The commands install Docker Engine and verify that the Compose plugin is available.",
            }
        ],
        [
            "Installing old docker-compose v1 and mixing command syntax.",
            "Adding every user to the docker group casually.",
            "Skipping a reboot or new login after group changes.",
            "Debugging compose files before verifying the daemon works.",
        ],
        "Install Docker and Compose on a disposable VM, run hello-world, and document the exact version output.",
    ),
    _lesson(
        "I03",
        "Docker CLI, Images, Containers, and Docker Hub",
        [
            "Use core Docker CLI commands confidently.",
            "Explain images, containers, tags, and registries.",
            "Inspect running Odoo services.",
        ],
        "The Docker CLI is the operational vocabulary for seeing what is running, what image it came from, and where logs are produced.",
        "Use tags deliberately: latest is convenient for experiments but too ambiguous for production upgrade control.",
        "Pull images, run containers, inspect metadata, read logs, execute shells, and remove unused resources with clear intent.",
        "Verify the image digest, environment, mounts, and network settings when a container behaves differently from another host.",
        "Production operators should be able to answer which image tag is running and how to recreate it before they make changes.",
        [
            "Images are immutable templates.",
            "Containers are running or stopped instances.",
            "Registries store and distribute images.",
            "Tags are names, not guarantees of immutability.",
            "docker inspect is essential for debugging.",
        ],
        [
            {
                "title": "Useful Docker inspection commands",
                "code": '''docker ps
docker images
docker logs --tail=100 odoo-web
docker exec -it odoo-web bash
docker inspect odoo-web --format '{{json .Mounts}}'
docker system df''',
                "explain": "These commands show running services, images, recent logs, interactive access, mounts, and disk usage.",
            }
        ],
        [
            "Using latest tags in production.",
            "Removing volumes while trying to clean images.",
            "Ignoring image provenance.",
            "Debugging from assumptions instead of docker inspect output.",
        ],
        "Run an Odoo container, inspect its environment and mounts, then explain the difference between stopping and removing it.",
    ),
    _lesson(
        "I04",
        "Dockerfile for Odoo",
        [
            "Build a custom Odoo image.",
            "Install Python and system dependencies predictably.",
            "Keep addons and requirements layered for cache efficiency.",
        ],
        "A custom Dockerfile turns an Odoo deployment from a mutable server into a versioned artifact.",
        "Decide which dependencies belong in the image and which configuration belongs at runtime through environment or mounted files.",
        "Start from a trusted Odoo base image, copy requirements before addons for cache efficiency, install packages as root, and run Odoo as the intended user.",
        "Build the image from a clean context and run it without bind mounts to prove the image contains everything needed.",
        "A production image should be reproducible, small enough to deploy quickly, and explicit about every dependency that custom code requires.",
        [
            "Images should include code and dependencies, not secrets.",
            "Layer order affects build cache.",
            "Use requirements.txt for Python dependencies.",
            "Keep runtime config outside the image.",
            "Build and test images in CI.",
        ],
        [
            {
                "title": "Custom Odoo image",
                "code": '''FROM odoo:18.0

USER root
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

USER odoo
COPY --chown=odoo:odoo ./addons /mnt/extra-addons
ENV ODOO_RC=/etc/odoo/odoo.conf''',
                "explain": "The image installs Python dependencies first and then copies custom addons with the correct ownership.",
            }
        ],
        [
            "Copying secrets into the image.",
            "Installing dependencies interactively inside a running container.",
            "Invalidating the build cache by copying the whole repository too early.",
            "Running the final container as root without need.",
        ],
        "Create a Dockerfile for custom addons, build it locally, and run Odoo from the image without mounting addon code.",
    ),
    _lesson(
        "I05",
        "Volumes for PostgreSQL, Filestore, and Addons",
        [
            "Map persistent Odoo data to volumes.",
            "Separate database, filestore, and code storage.",
            "Avoid accidental data loss during container replacement.",
        ],
        "Odoo persistence is split between PostgreSQL rows and the filestore, and both must be backed up together.",
        "Design storage paths so database data, Odoo filestore, configuration, logs, and custom addons have clear ownership and backup policy.",
        "Use named volumes or host bind mounts intentionally, and never rely on the writable container layer for anything important.",
        "Verify by deleting and recreating the application container while confirming that database records and attachments still exist.",
        "Production restore depends on matching database dumps with the correct filestore, so volume layout is a backup design decision.",
        [
            "PostgreSQL data and Odoo filestore are both persistent.",
            "Named volumes are managed by Docker.",
            "Bind mounts expose host paths explicitly.",
            "Container layers are disposable.",
            "Backups must include database and filestore together.",
        ],
        [
            {
                "title": "Compose volumes for Odoo data",
                "code": '''services:
  db:
    image: postgres:16
    volumes:
      - pgdata:/var/lib/postgresql/data
  odoo:
    image: odoo:18.0
    volumes:
      - odoo-data:/var/lib/odoo
      - ./addons:/mnt/extra-addons:ro

volumes:
  pgdata:
  odoo-data:''',
                "explain": "The database and filestore use persistent volumes while custom addons are mounted read-only.",
            }
        ],
        [
            "Backing up only the database and forgetting attachments.",
            "Mounting writable addon code in production.",
            "Using anonymous volumes without knowing their names.",
            "Deleting volumes during image cleanup.",
        ],
        "Attach a PDF to an Odoo record, recreate the Odoo container, and confirm the attachment still opens.",
    ),
    _lesson(
        "I06",
        "Docker Networking for Odoo",
        [
            "Explain service discovery in Docker Compose.",
            "Connect Odoo to PostgreSQL by service name.",
            "Expose only required ports to the host.",
        ],
        "Compose networking gives services DNS names and private connectivity without exposing every port to the outside world.",
        "Decide which services need host access, which only need internal network access, and which should be isolated from public traffic.",
        "Use service names such as db as hostnames, publish only Nginx or Odoo ports needed by the environment, and avoid hard-coded container IP addresses.",
        "Verify connectivity with docker exec, getent hosts, and application logs rather than guessing at network failures.",
        "A clean network design reduces attack surface and makes local, staging, and production compose files easier to compare.",
        [
            "Compose services share a project network by default.",
            "Service names resolve through Docker DNS.",
            "ports publishes to the host; expose documents internal ports.",
            "Do not depend on container IP addresses.",
            "Limit public exposure.",
        ],
        [
            {
                "title": "Internal database network",
                "code": '''services:
  odoo:
    image: odoo:18.0
    environment:
      HOST: db
      USER: odoo
      PASSWORD: odoo
    ports:
      - "8069:8069"
    depends_on:
      - db
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: postgres
      POSTGRES_USER: odoo
      POSTGRES_PASSWORD: odoo''',
                "explain": "Odoo connects to PostgreSQL using the db service name without publishing PostgreSQL to the host.",
            }
        ],
        [
            "Publishing PostgreSQL publicly without a reason.",
            "Using container IPs that change after recreation.",
            "Assuming depends_on means the database is ready for connections.",
            "Mixing unrelated stacks on the same exposed ports.",
        ],
        "Create a compose network where only Odoo is published, then prove PostgreSQL is reachable from Odoo but not from the host port list.",
    ),
    _lesson(
        "I07",
        "Docker Compose Fundamentals",
        [
            "Read and write compose service definitions.",
            "Use environment, volumes, ports, and depends_on.",
            "Operate a compose project safely.",
        ],
        "Compose turns a multi-command deployment into a declarative project that can be started, stopped, inspected, and versioned.",
        "Design compose files so the default command is safe for the target environment and overrides are explicit.",
        "Define services, images or build contexts, environment variables, volumes, networks, healthchecks, and restart policies where appropriate.",
        "Verify with config rendering, logs, service status, and restart tests because valid YAML can still describe a poor deployment.",
        "Production compose usage should be predictable enough that an engineer can recreate the stack from the repository and documented secrets.",
        [
            "docker compose config validates and expands configuration.",
            "Services are the main units.",
            "Environment can come from .env and env_file.",
            "Restart policy controls daemon behavior after failure.",
            "Compose project names affect resource names.",
        ],
        [
            {
                "title": "Common compose operations",
                "code": '''docker compose config
docker compose up -d
docker compose logs -f --tail=100 odoo
docker compose ps
docker compose restart odoo
docker compose down''',
                "explain": "These commands validate, start, inspect, restart, and stop a compose project.",
            }
        ],
        [
            "Editing running containers instead of compose files.",
            "Skipping docker compose config before deployment.",
            "Confusing down with volume removal.",
            "Letting project names change between runs unexpectedly.",
        ],
        "Write a minimal compose file with Odoo and PostgreSQL, run docker compose config, and explain every generated service field.",
    ),
    _lesson(
        "I08",
        "Multi-Container Odoo and PostgreSQL",
        [
            "Run Odoo and PostgreSQL as separate services.",
            "Configure database credentials and health checks.",
            "Understand startup ordering and readiness.",
        ],
        "Separating Odoo and PostgreSQL mirrors the real dependency between an application server and a database server.",
        "Choose explicit database credentials, persistent storage, healthchecks, and restart behavior before adding custom addons or proxy layers.",
        "Use environment variables or config files for db_host, db_user, and db_password, and define a PostgreSQL healthcheck because depends_on is not readiness.",
        "Verify by restarting only the database, then only Odoo, and checking how each service logs reconnection or startup behavior.",
        "A stable two-container baseline is the foundation for adding workers, Nginx, backups, and monitoring later.",
        [
            "Odoo and PostgreSQL should be separate services.",
            "depends_on controls order, not readiness.",
            "Healthchecks make service state visible.",
            "Use persistent PostgreSQL storage.",
            "Restart behavior should be intentional.",
        ],
        [
            {
                "title": "Odoo and PostgreSQL compose stack",
                "code": '''services:
  db:
    image: postgres:16
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: postgres
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

  odoo:
    image: odoo:18.0
    restart: unless-stopped
    depends_on:
      - db
    environment:
      HOST: db
      USER: ${POSTGRES_USER}
      PASSWORD: ${POSTGRES_PASSWORD}''',
                "explain": "The stack separates services and exposes database readiness through a healthcheck.",
            }
        ],
        [
            "Putting PostgreSQL inside the Odoo container.",
            "Using default passwords in shared environments.",
            "Assuming startup order means readiness.",
            "Restarting the whole stack for a single-service issue.",
        ],
        "Run the two-container stack, restart PostgreSQL, and capture the relevant Odoo logs during reconnect.",
    ),
    _lesson(
        "I09",
        ".env Files and Runtime Configuration",
        [
            "Use .env files for non-secret and secret runtime values carefully.",
            "Understand Compose variable substitution.",
            "Separate committed examples from real credentials.",
        ],
        ".env files make compose projects easier to configure, but they also become a common source of leaked secrets.",
        "Decide which variables are safe defaults, which are environment-specific, and which should come from a secret manager in production.",
        "Commit .env.example, ignore real .env files, and use explicit variable names for database credentials, domain names, image tags, and worker settings.",
        "Verify the rendered configuration with docker compose config and check repository status before committing.",
        "A disciplined configuration approach lets staging and production differ without maintaining separate hand-edited compose files.",
        [
            ".env supports Compose variable substitution.",
            "Commit examples, not real secrets.",
            "docker compose config shows resolved values.",
            "Use clear variable names.",
            "Production secrets may need a stronger mechanism.",
        ],
        [
            {
                "title": ".env.example",
                "code": '''ODOO_IMAGE=odoo:18.0
POSTGRES_USER=odoo
POSTGRES_PASSWORD=replace-in-real-env
ODOO_DB_HOST=db
ODOO_WORKERS=4
ODOO_LIMIT_MEMORY_HARD=2684354560
DOMAIN=odoo.example.com''',
                "explain": "The example documents required settings without pretending that the sample password is production-ready.",
            }
        ],
        [
            "Committing real .env files.",
            "Assuming .env variables are automatically available inside containers.",
            "Using vague names such as PASSWORD for multiple services.",
            "Skipping rendered config review before deployment.",
        ],
        "Create .env.example and .gitignore entries for a compose project, then render the final compose config with local values.",
    ),
    _lesson(
        "I10",
        "Upgrading Containers Safely",
        [
            "Plan image and module upgrades.",
            "Back up database and filestore before changes.",
            "Roll forward or roll back from a known state.",
        ],
        "Container upgrades are easy to start and expensive to recover from if database migrations and filestore compatibility are ignored.",
        "Separate base image upgrades, custom addon changes, and database migrations into a planned sequence with a tested backup.",
        "Pull or build the new image, stop traffic, take backups, run Odoo update commands on staging first, and keep the previous image tag available.",
        "Verify module updates, logs, scheduled jobs, reports, and core user journeys before reopening traffic.",
        "Safe upgrades are boring because every step has already been rehearsed on a restored copy of production.",
        [
            "Pin image tags before upgrading.",
            "Back up database and filestore together.",
            "Test migrations on a restored copy.",
            "Keep previous image available for rollback.",
            "Review logs before declaring success.",
        ],
        [
            {
                "title": "Upgrade command sequence",
                "code": '''docker compose pull odoo
docker compose stop odoo
./scripts/backup_odoo.sh
docker compose up -d odoo
docker compose exec odoo odoo -d prod -u training --stop-after-init
docker compose logs --tail=200 odoo''',
                "explain": "The sequence backs up before starting the new image and runs an explicit module update.",
            }
        ],
        [
            "Using latest tags and not knowing what changed.",
            "Upgrading production before staging.",
            "Backing up the database without the filestore.",
            "Skipping post-upgrade functional checks.",
        ],
        "Write a one-page upgrade runbook for an Odoo container stack, including rollback criteria and validation checks.",
    ),
    _lesson(
        "I11",
        "CI/CD with GitHub Actions Basics",
        [
            "Create a basic CI workflow for Odoo modules.",
            "Run linting and tests on pull requests.",
            "Build container images from commits.",
        ],
        "CI/CD turns local confidence into repeatable checks that run before code reaches shared environments.",
        "Start with fast checks that catch common failures: syntax, manifest validity, unit tests, and image build problems.",
        "Use GitHub Actions workflows with pinned action versions, service containers for PostgreSQL where needed, and artifacts for logs or coverage.",
        "Verify that a failing test fails the workflow and that secrets are only available on trusted events.",
        "Production deployment should build on CI results, but the first goal is preventing broken custom addons from being merged unnoticed.",
        [
            "Run checks on pull_request and push.",
            "Use PostgreSQL services for integration tests.",
            "Cache dependencies cautiously.",
            "Protect secrets from untrusted forks.",
            "Keep workflows readable and incremental.",
        ],
        [
            {
                "title": "Basic GitHub Actions workflow",
                "code": '''name: odoo-ci

on:
  pull_request:
  push:
    branches: [main]

jobs:
  python-checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: python -m compileall custom_addons
      - run: python scripts/check_manifests.py custom_addons''',
                "explain": "The workflow starts with lightweight checks that catch syntax and manifest problems.",
            }
        ],
        [
            "Putting deployment secrets in pull_request workflows from forks.",
            "Running huge end-to-end jobs before cheap syntax checks.",
            "Ignoring workflow failure logs.",
            "Letting CI use a different dependency set than production.",
        ],
        "Create a CI workflow that compiles custom addon Python files and intentionally break one file to prove the check fails.",
    ),
    _lesson(
        "I12",
        "VPS Provisioning and Production Directory Layout",
        [
            "Prepare a VPS for Odoo deployment.",
            "Design a clear production directory structure.",
            "Separate app code, config, backups, logs, and secrets.",
        ],
        "A VPS is simple enough for small Odoo deployments but still needs disciplined layout and host preparation.",
        "Provision with a supported OS, enough memory and disk IOPS, a non-root deploy user, firewall rules, time sync, and monitoring access.",
        "Create predictable directories such as /opt/odoo/app, /opt/odoo/config, /opt/odoo/backups, /var/log/odoo, and /srv/odoo/filestore depending on the deployment style.",
        "Verify permissions by running the service as the target user and confirming that backups can write only where intended.",
        "A good layout makes incidents calmer because engineers can find the compose file, config, backups, and logs without searching the whole server.",
        [
            "Use a non-root deploy or odoo user.",
            "Keep configuration and secrets separate from code.",
            "Define backup and log paths explicitly.",
            "Document the directory layout.",
            "Provision disk and memory for growth.",
        ],
        [
            {
                "title": "Production layout example",
                "code": '''/opt/odoo/
  app/                 # compose file or deployment repository
  config/              # odoo.conf, nginx snippets, env files
  backups/             # database and filestore backups
  scripts/             # backup, restore, health checks
/var/log/odoo/          # application logs
/srv/odoo/filestore/    # optional external filestore path''',
                "explain": "The layout keeps operational assets separate and easy to back up or audit.",
            }
        ],
        [
            "Running everything from a developer's home directory.",
            "Mixing backups into the application repository.",
            "Leaving important files owned by root after manual commands.",
            "Not documenting which path is authoritative.",
        ],
        "Provision a small test VPS or VM and create the directory layout with ownership and permissions suitable for an odoo deploy user.",
    ),
    _lesson(
        "I13",
        "SSH Hardening",
        [
            "Reduce common SSH attack surface.",
            "Use key-based authentication.",
            "Protect administrative access without locking out operators.",
        ],
        "SSH is usually the front door to a VPS, so weak SSH posture undermines every application hardening effort.",
        "Design access around named users, public keys, sudo policy, and an emergency recovery path from the VPS provider console.",
        "Disable password login, disable root login, restrict users where practical, install fail2ban or equivalent protection, and keep authorized keys reviewed.",
        "Verify a second session can connect before closing the first and test sudo access for the deploy process.",
        "Good SSH hardening balances security and operability: locked-out administrators cause downtime just as surely as attackers do.",
        [
            "Use public key authentication.",
            "Disable direct root login.",
            "Keep an active session while testing changes.",
            "Limit sudo and user access.",
            "Maintain an emergency recovery path.",
        ],
        [
            {
                "title": "sshd hardening fragment",
                "code": '''# /etc/ssh/sshd_config.d/10-hardening.conf
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
AllowUsers deploy
ClientAliveInterval 300
ClientAliveCountMax 2''',
                "explain": "The fragment disables password and root login while allowing a named deploy user.",
            }
        ],
        [
            "Restarting SSH after changes without an open backup session.",
            "Sharing one private key between operators.",
            "Disabling root login before creating a sudo-capable user.",
            "Forgetting provider console recovery.",
        ],
        "Harden SSH on a disposable VM, prove key login works in a second session, and document the rollback path.",
    ),
    _lesson(
        "I14",
        "Nginx Reverse Proxy for Odoo",
        [
            "Proxy public HTTP traffic to Odoo.",
            "Set headers required for correct URL generation.",
            "Configure timeouts for long Odoo requests.",
        ],
        "Nginx usually terminates public HTTP traffic and forwards application requests to Odoo on an internal port.",
        "Decide where TLS terminates, which hostnames are valid, and whether Odoo runs in proxy_mode so it trusts forwarded headers correctly.",
        "Configure proxy_pass, Host, X-Forwarded headers, body size, buffering, and timeouts appropriate for Odoo imports and reports.",
        "Verify real client IPs, generated URLs, file uploads, long report renders, and backend logs after enabling the proxy.",
        "A correct reverse proxy prevents subtle bugs around redirects, mixed content, incorrect base URLs, and client IP audit logs.",
        [
            "Enable proxy_mode in Odoo when behind a proxy.",
            "Forward Host and X-Forwarded headers.",
            "Set body size for imports and attachments.",
            "Tune timeouts for reports and upgrades.",
            "Keep upstream ports private when possible.",
        ],
        [
            {
                "title": "Nginx Odoo proxy server",
                "code": '''server {
    listen 80;
    server_name odoo.example.com;

    client_max_body_size 100m;

    location / {
        proxy_pass http://127.0.0.1:8069;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 720s;
        proxy_connect_timeout 720s;
    }
}''',
                "explain": "The proxy forwards standard headers and allows long Odoo requests to complete.",
            }
        ],
        [
            "Forgetting proxy_mode in Odoo configuration.",
            "Leaving Odoo publicly exposed when Nginx should be the entry point.",
            "Using low timeouts that break large reports or imports.",
            "Not forwarding X-Forwarded-Proto, causing bad redirects.",
        ],
        "Put Nginx in front of Odoo, enable proxy_mode, and confirm generated web.base.url uses the public hostname.",
    ),
    _lesson(
        "I15",
        "Ports 80 and 443 to 8069, Longpolling 8072, and Let's Encrypt",
        [
            "Route public HTTP and HTTPS traffic to Odoo.",
            "Handle longpolling or websocket-style notification endpoints.",
            "Install TLS certificates with Certbot.",
        ],
        "Users should reach Odoo on standard web ports while the application listens internally on ports such as 8069 and longpolling on 8072.",
        "Plan firewall rules, Nginx server blocks, TLS termination, renewal automation, and the route for bus or longpolling traffic.",
        "Use Certbot for Let's Encrypt certificates, redirect HTTP to HTTPS, and add a separate location for longpolling when the deployment uses a dedicated port.",
        "Verify certificate renewal, live chat or bus notifications, redirect behavior, and firewall exposure from outside the server.",
        "A deployment without reliable TLS and notification routing will look healthy until users report broken chat, Discuss, or real-time updates.",
        [
            "Public users should use 80 and 443.",
            "Odoo backend often listens on 8069 internally.",
            "Longpolling commonly uses 8072 in worker deployments.",
            "Certbot can automate Let's Encrypt certificates.",
            "Test certificate renewal before relying on it.",
        ],
        [
            {
                "title": "Nginx HTTPS and longpolling locations",
                "code": '''server {
    listen 443 ssl http2;
    server_name odoo.example.com;

    ssl_certificate /etc/letsencrypt/live/odoo.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/odoo.example.com/privkey.pem;

    location /longpolling/ {
        proxy_pass http://127.0.0.1:8072;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto https;
    }

    location / {
        proxy_pass http://127.0.0.1:8069;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-Proto https;
    }
}''',
                "explain": "The server routes normal requests to 8069 and longpolling requests to 8072 under HTTPS.",
            }
        ],
        [
            "Opening 8069 and 8072 publicly when only Nginx should be exposed.",
            "Forgetting automatic certificate renewal.",
            "Routing longpolling to the wrong upstream.",
            "Not testing real-time notifications after enabling workers.",
        ],
        "Configure HTTPS for a test hostname, add a longpolling location, and run certbot renew --dry-run.",
    ),
    _lesson(
        "I16",
        "systemd odoo.service",
        [
            "Run Odoo as a systemd service.",
            "Define restart behavior and service user.",
            "Use journalctl for logs and diagnosis.",
        ],
        "Some deployments run Odoo directly on a host instead of containers, and systemd is the standard process supervisor for that model.",
        "Decide the service user, config file path, Python environment, addons path, restart policy, and log destination before writing the unit.",
        "Create a unit file with ExecStart, User, WorkingDirectory, Restart, and dependency on PostgreSQL or network availability as appropriate.",
        "Verify daemon reload, enable, start, restart, failure restart, and journal logs so operations are repeatable.",
        "A clear systemd unit makes a non-container deployment manageable and avoids fragile shell sessions or manual startup commands.",
        [
            "Run Odoo under a dedicated user.",
            "Keep ExecStart explicit.",
            "Use systemctl enable for boot startup.",
            "Use journalctl -u for logs.",
            "Restart policy should match operational expectations.",
        ],
        [
            {
                "title": "Odoo systemd unit",
                "code": '''[Unit]
Description=Odoo Application Server
After=network.target postgresql.service

[Service]
Type=simple
User=odoo
Group=odoo
WorkingDirectory=/opt/odoo/server
ExecStart=/opt/odoo/venv/bin/python3 /opt/odoo/server/odoo-bin -c /etc/odoo/odoo.conf
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target''',
                "explain": "The unit runs Odoo from a virtual environment with a dedicated user and restarts after failures.",
            }
        ],
        [
            "Running Odoo manually in screen or tmux as the production supervisor.",
            "Starting the service as root without need.",
            "Forgetting systemctl daemon-reload after editing the unit.",
            "Hiding logs in an unmanaged file path.",
        ],
        "Create a systemd unit on a test VM, start it, force a failure, and confirm restart behavior in journalctl.",
    ),
    _lesson(
        "I17",
        "Backup Cron for Database and Filestore",
        [
            "Back up PostgreSQL and Odoo filestore together.",
            "Schedule backups with cron.",
            "Test restore, retention, and failure alerts.",
        ],
        "Backups are only useful when they can be restored, and Odoo requires both database and filestore for a complete restore.",
        "Design backup frequency, retention, encryption, offsite storage, and restore objectives before writing the cron line.",
        "Use pg_dump or pg_dumpall as appropriate, archive the filestore matching the database, name backups with timestamps, and prune old files safely.",
        "Verify by restoring to a separate database and opening attachments, not by checking that a backup file exists.",
        "Production backup policy should include alerting because a silent backup failure is discovered at the worst possible time.",
        [
            "Database and filestore must be backed up as a pair.",
            "Timestamp backup names.",
            "Store copies off the application host.",
            "Test restore regularly.",
            "Alert on backup failures.",
        ],
        [
            {
                "title": "Backup script fragment",
                "code": '''#!/usr/bin/env bash
set -euo pipefail

DB=prod
STAMP=$(date +%Y%m%d-%H%M%S)
DEST=/opt/odoo/backups/$STAMP
mkdir -p "$DEST"

pg_dump -Fc "$DB" > "$DEST/$DB.dump"
tar -C /var/lib/odoo/filestore -czf "$DEST/filestore.tgz" "$DB"
find /opt/odoo/backups -mindepth 1 -maxdepth 1 -type d -mtime +14 -exec rm -rf {} +''',
                "explain": "The script writes a timestamped database dump and matching filestore archive, then prunes old local backups.",
            }
        ],
        [
            "Backing up only PostgreSQL.",
            "Never testing restore.",
            "Keeping all backups on the same disk as production.",
            "Writing cron jobs that fail silently.",
        ],
        "Create a backup script and cron entry, then restore the output to a separate test database and open an attachment.",
    ),
    _lesson(
        "I18",
        "Odoo Workers Architecture and Worker Calculation",
        [
            "Explain threaded versus multi-worker Odoo modes.",
            "Calculate an initial worker count.",
            "Reserve capacity for cron and longpolling.",
        ],
        "Odoo workers let the application handle concurrent HTTP requests with multiple processes instead of one threaded development-style server.",
        "Base the initial worker count on CPU cores, memory, traffic profile, cron load, and whether the host also runs PostgreSQL.",
        "Set workers, max_cron_threads, proxy_mode, and gevent or longpolling configuration according to the Odoo version and deployment model.",
        "Verify under load with realistic requests, not only by checking that processes exist, because workers can be CPU-bound, memory-bound, or database-bound.",
        "Worker sizing is an iterative capacity practice: start conservatively, measure, and adjust before users feel saturation.",
        [
            "workers > 0 enables multi-process mode.",
            "A common starting formula is CPU cores * 2 + 1, adjusted for memory.",
            "Cron workers consume capacity.",
            "Longpolling or bus traffic may need separate handling.",
            "Measure before and after changes.",
        ],
        [
            {
                "title": "odoo.conf worker settings",
                "code": '''[options]
workers = 5
max_cron_threads = 1
proxy_mode = True
limit_time_cpu = 120
limit_time_real = 240
limit_memory_soft = 2147483648
limit_memory_hard = 2684354560''',
                "explain": "The settings enable worker mode with conservative time and memory limits for a modest host.",
            }
        ],
        [
            "Using the CPU formula without checking memory.",
            "Forgetting cron capacity.",
            "Running many workers against too few PostgreSQL connections.",
            "Changing workers without load testing.",
        ],
        "Calculate initial workers for a 4-core, 8 GB VPS running Odoo and PostgreSQL, then justify memory reserves.",
    ),
    _lesson(
        "I19",
        "Memory Limits, Time Limits, PostgreSQL Pooling, and max_connections",
        [
            "Configure Odoo request memory and time guards.",
            "Relate Odoo workers to PostgreSQL connections.",
            "Plan pooling or max_connections changes safely.",
        ],
        "Odoo and PostgreSQL capacity problems often appear together because more workers can mean more database connections and more memory pressure.",
        "Design limits from the host resources, request profile, scheduled jobs, and PostgreSQL memory settings instead of copying values from another deployment.",
        "Set limit_memory_soft, limit_memory_hard, limit_time_cpu, limit_time_real, db_maxconn, and PostgreSQL max_connections with enough headroom for maintenance sessions.",
        "Verify by monitoring worker recycling, slow requests, database connection counts, and out-of-memory events under realistic load.",
        "Production tuning is a balancing act: too loose risks host instability, too tight kills legitimate reports and imports.",
        [
            "Odoo workers consume memory independently.",
            "db_maxconn controls Odoo's database connection pool per process.",
            "PostgreSQL max_connections must cover all clients.",
            "Memory limits recycle runaway workers.",
            "Long reports may need time limit review.",
        ],
        [
            {
                "title": "Connection budget example",
                "code": '''# Example budget
workers = 5
max_cron_threads = 1
db_maxconn = 16

# Potential Odoo connections: (workers + cron + main process) * db_maxconn
# Add admin tools, monitoring, backup jobs, and migration sessions before
# setting PostgreSQL max_connections.''',
                "explain": "The calculation reminds operators to budget for all database clients, not only HTTP workers.",
            }
        ],
        [
            "Increasing workers without increasing database capacity.",
            "Setting max_connections high without enough PostgreSQL memory.",
            "Disabling time limits to hide slow code.",
            "Ignoring cron and migration connections.",
        ],
        "Create a connection and memory budget for an 8-worker Odoo deployment and propose safe PostgreSQL max_connections.",
    ),
    _lesson(
        "I20",
        "Indexes, pg_stat_statements, Redis Sessions, Load Balancing, and Prometheus Grafana",
        [
            "Identify slow SQL with pg_stat_statements.",
            "Explain when missing indexes hurt Odoo.",
            "Describe Redis sessions, load balancing, and monitoring basics.",
        ],
        "At scale, Odoo performance is usually constrained by database queries, worker saturation, cache behavior, or lack of visibility.",
        "Design observability before firefighting: know which metrics, logs, and query statistics reveal the difference between slow Python, slow SQL, and overloaded infrastructure.",
        "Enable pg_stat_statements, inspect high-total-time queries, add indexes only after understanding domains, and consider Redis-backed sessions or sticky load balancing for multi-node deployments.",
        "Verify every performance change with before-and-after measurements, because indexes can slow writes and load balancers can break session assumptions.",
        "Prometheus and Grafana provide the operational feedback loop: collect metrics, create dashboards, alert on symptoms, and use traces or logs for root cause.",
        [
            "pg_stat_statements shows expensive query patterns.",
            "Indexes should match frequent domains and joins.",
            "Redis sessions can help multi-node session consistency.",
            "Load balancing requires shared filestore and session strategy.",
            "Prometheus and Grafana turn metrics into alerts and dashboards.",
        ],
        [
            {
                "title": "Inspect slow queries",
                "code": '''CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

SELECT calls,
       total_exec_time,
       mean_exec_time,
       rows,
       query
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;

CREATE INDEX IF NOT EXISTS training_course_state_start_idx
    ON training_course (state, start_date);''',
                "explain": "The query identifies expensive SQL patterns; the example index matches a common state and date domain.",
            }
        ],
        [
            "Adding indexes blindly for every slow query.",
            "Load balancing without shared filestore or session planning.",
            "Creating dashboards with no alert thresholds.",
            "Ignoring write overhead from extra indexes.",
        ],
        "Enable pg_stat_statements on a staging database, identify one slow query pattern, and propose a measured index or code change.",
        [
            {
                "kind": "table",
                "title": "Observability layers",
                "headers": ["Layer", "Signal"],
                "rows": [
                    ["Odoo", "Request latency, worker count, errors"],
                    ["PostgreSQL", "Slow queries, locks, connections"],
                    ["Host", "CPU, memory, disk IO"],
                    ["Proxy", "Status codes, upstream time"],
                ],
            }
        ],
    ),
]

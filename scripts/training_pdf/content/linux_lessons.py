"""Linux lesson content for the Odoo training PDF generator."""


def _explanation(topic, focus, details, risk, odoo_context, senior_advice):
    return [
        (
            f"{topic} matters because Odoo servers are ordinary Linux systems before they are application servers. "
            f"A developer who understands {focus} can reason from first principles instead of copying commands blindly."
        ),
        (
            f"The practical workflow is to observe the current state, make one controlled change, and verify the result. "
            f"For this lesson, that means paying attention to {details} and keeping the command output as evidence."
        ),
        (
            f"Linux rewards precision: paths, users, permissions, units, and sockets all have exact meanings. "
            f"When those details are treated casually, the common failure is {risk}, which is harder to diagnose after several unrelated changes."
        ),
        (
            f"In an Odoo deployment, {odoo_context} connects this topic directly to uptime, data safety, and predictable releases. "
            f"The same command can be harmless on a test VM and dangerous on a production database host, so context always comes first."
        ),
        (
            f"Senior engineers build small repeatable checks around this area instead of relying on memory. "
            f"They record the expected command, the expected output pattern, and the rollback step before changing a shared server."
        ),
        (
            f"The goal is not to memorize every flag, but to understand the model well enough to choose the right tool. "
            f"{senior_advice} turns Linux from a source of surprises into a stable operating base for Odoo work."
        ),
    ]


def _lesson(
    lesson_id,
    title,
    objectives,
    focus,
    details,
    risk,
    odoo_context,
    senior_advice,
    key_points,
    examples,
    common_mistakes,
    lab,
    slide_extras=None,
):
    return {
        "section": "linux",
        "id": lesson_id,
        "title": title,
        "objectives": objectives,
        "explanation": _explanation(title, focus, details, risk, odoo_context, senior_advice),
        "key_points": key_points,
        "examples": examples,
        "common_mistakes": common_mistakes,
        "lab": lab,
        "slide_extras": slide_extras or [],
    }


LESSONS = [
    _lesson(
        "L01",
        "OS Fundamentals and Kernel Basics",
        [
            "Explain the relationship between hardware, kernel, system libraries, and user processes.",
            "Identify where the shell, services, and Odoo workers fit in the operating system model.",
            "Use basic inspection commands to confirm kernel and distribution details.",
            "Describe why kernel resources affect application performance.",
        ],
        "the kernel boundary and the role of user space",
        "kernel version, distribution release, CPU architecture, memory, and process ownership",
        "debugging symptoms at the application layer while ignoring resource or kernel limits",
        "Odoo workers, PostgreSQL, Nginx, and cron all compete for CPU time, memory, file descriptors, and network sockets",
        "Start investigations by naming the layer you are testing: hardware, kernel, service manager, process, or application.",
        [
            "The kernel manages CPU scheduling, memory, devices, filesystems, and network stacks.",
            "User space contains shells, package managers, systemd, Python, PostgreSQL, Nginx, and Odoo.",
            "A distribution combines the Linux kernel with tools, defaults, repositories, and service policies.",
            "Applications fail when kernel limits are exhausted even if their own code is correct.",
            "Version and architecture details matter when installing drivers, Python wheels, and database packages.",
            "Good incident notes separate facts observed from assumptions about root cause.",
        ],
        [
            {
                "title": "Inspect the operating system baseline",
                "code": """uname -a
cat /etc/os-release
lscpu | sed -n '1,8p'
free -h""",
                "explain": (
                    "These commands establish the kernel, distribution, CPU, and memory baseline before troubleshooting. "
                    "Capture this information in support tickets because package names, service defaults, and binary compatibility vary by distribution and version."
                ),
            },
            {
                "title": "See user-space processes",
                "code": """ps -eo pid,ppid,user,stat,comm --sort=pid | head -20
pstree -ap | head -30""",
                "explain": (
                    "The process tree shows that every running program is a child of an existing process and has a user identity. "
                    "For Odoo, this makes it clear whether work is running under systemd, an interactive shell, or an accidental manual start."
                ),
            },
        ],
        [
            "Treating Linux as a black box and jumping directly into Odoo configuration.",
            "Assuming two Ubuntu releases behave identically because the commands look similar.",
            "Ignoring kernel limits such as open files, memory pressure, and socket backlog.",
            "Changing production settings without first recording the current system state.",
        ],
        "On a lab VM, record kernel, distribution, CPU, memory, and top-level process information. Write a short note explaining which layer would own a network failure, a Python import failure, and an out-of-memory crash.",
        [
            {
                "kind": "table",
                "title": "Linux layers",
                "headers": ["Layer", "Examples", "Why Odoo developers care"],
                "rows": [
                    ["Hardware", "CPU, RAM, disk, NIC", "Defines capacity and failure boundaries"],
                    ["Kernel", "scheduler, memory, TCP, filesystems", "Controls resources used by workers"],
                    ["User space", "systemd, Python, PostgreSQL, Nginx", "Runs the actual Odoo stack"],
                ],
            }
        ],
    ),
    _lesson(
        "L02",
        "Terminal Navigation with pwd, cd, ls, and tree",
        [
            "Navigate absolute and relative paths confidently.",
            "Use directory listings to understand an unfamiliar server.",
            "Distinguish the current shell directory from service working directories.",
            "Build safe habits before editing production files.",
        ],
        "filesystem navigation and situational awareness",
        "current directory, hidden files, symlinks, ownership, and directory depth",
        "editing or deleting the wrong file because the shell was in an unexpected directory",
        "Odoo source, custom addons, logs, configuration, and backups usually live in different directories with different owners",
        "Say the path out loud, print it with pwd, and list it before running a destructive command.",
        [
            "pwd prints the shell's current working directory; it does not tell you where a service runs.",
            "cd changes directory for the current shell session only.",
            "ls -la shows hidden files, permissions, owners, sizes, and timestamps.",
            "tree is useful for understanding project shape but should be limited with -L on large directories.",
            "Absolute paths start at /, while relative paths start from the current directory.",
            "Symlinks are common in deployments and should be inspected before editing through them.",
        ],
        [
            {
                "title": "Build a safe navigation habit",
                "code": """pwd
cd /opt/odoo
pwd
ls -la
tree -L 2 /opt/odoo""",
                "explain": (
                    "This sequence confirms the starting point, moves to the expected application directory, and inspects contents before making changes. "
                    "The limited tree depth gives a useful overview without flooding the terminal on a large addons directory."
                ),
            },
            {
                "title": "Compare absolute and relative paths",
                "code": """cd /etc/odoo
ls -l odoo.conf
ls -l /etc/odoo/odoo.conf
cd /
ls -l etc/odoo/odoo.conf""",
                "explain": (
                    "The same file can be referenced through different path forms, but only the absolute form is independent of the current directory. "
                    "Scripts and service files should prefer absolute paths so they behave consistently."
                ),
            },
        ],
        [
            "Running rm, mv, or chmod before checking pwd.",
            "Forgetting that hidden dotfiles affect shell and application behavior.",
            "Using tree without a depth limit on large production directories.",
            "Editing a symlink target without realizing where the real file lives.",
        ],
        "Create a small directory tree under /tmp/odoo-navigation-lab, navigate it using absolute and relative paths, then produce a one-screen map with tree -L 3 and annotations for config, logs, and addons.",
    ),
    _lesson(
        "L03",
        "File Manipulation: Create, Copy, Move, Link, and Remove",
        [
            "Create and inspect files safely from the terminal.",
            "Copy and move files while preserving important metadata when needed.",
            "Understand hard links, symbolic links, and backup naming.",
            "Use cautious deletion practices on servers.",
        ],
        "safe manipulation of files and directories",
        "destination paths, overwrite behavior, timestamps, ownership, and symbolic links",
        "destroying the only known-good configuration during a rushed fix",
        "Odoo configuration files, custom modules, attachment filestore data, and backup archives require different handling",
        "Make reversible changes: copy first, edit second, verify third, and delete only after the replacement is proven.",
        [
            "touch creates an empty file or updates timestamps.",
            "cp copies data; cp -a preserves mode, owner, timestamps, and symlinks where permissions allow.",
            "mv renames within a filesystem and moves across filesystems by copying then removing.",
            "ln -s creates a symbolic link, which stores a path reference rather than file content.",
            "rm is permanent at the shell level; production cleanup should be explicit and reviewed.",
            "Backups need names that show what changed, when, and why.",
        ],
        [
            {
                "title": "Back up and edit a configuration file",
                "code": """sudo cp -a /etc/odoo/odoo.conf /etc/odoo/odoo.conf.bak.$(date +%Y%m%d-%H%M%S)
sudo nano /etc/odoo/odoo.conf
sudo diff -u /etc/odoo/odoo.conf.bak.* /etc/odoo/odoo.conf | tail -40""",
                "explain": (
                    "The archive copy preserves the original metadata and embeds a timestamp in the backup name. "
                    "A diff after editing keeps the review focused on exactly what changed before the service is restarted."
                ),
            },
            {
                "title": "Use a symlink for active custom addons",
                "code": """sudo mkdir -p /opt/odoo/custom-addons/releases/2026-07-24
sudo ln -sfn /opt/odoo/custom-addons/releases/2026-07-24 /opt/odoo/custom-addons/current
ls -l /opt/odoo/custom-addons/current""",
                "explain": (
                    "A stable symlink such as current lets service configuration point at one path while releases change underneath it. "
                    "The -n and -f flags replace the link itself rather than following an existing link as a directory."
                ),
            },
        ],
        [
            "Copying config files without preserving permissions, then wondering why services cannot read them.",
            "Using wildcard deletes without first listing what the wildcard expands to.",
            "Confusing a symlink with a physical copy of a directory.",
            "Leaving backup files in locations where applications accidentally load them.",
        ],
        "Create a fake /tmp/odoo-file-lab config file, back it up with a timestamp, edit one setting, compare with diff, then replace a current symlink to point at a new fake release directory.",
    ),
    _lesson(
        "L04",
        "Permissions with chmod, chown, and chgrp",
        [
            "Read Unix permission bits and ownership from ls output.",
            "Apply chmod using symbolic and numeric modes.",
            "Change file owners and groups safely with chown and chgrp.",
            "Choose permissions suitable for Odoo configuration, source code, and logs.",
        ],
        "ownership and permission enforcement",
        "read, write, execute bits, owner, group, others, directories, and recursive changes",
        "masking an ownership problem by making sensitive files world-writable",
        "Odoo should run as a dedicated user that can read its code and config but does not own everything on the server",
        "Prefer the smallest permission change that makes the intended actor able to do the intended action.",
        [
            "Permission triplets apply to owner, group, and others in that order.",
            "Execute on a directory means the user can traverse it; read means the user can list names.",
            "chmod 640 is common for private configuration files readable by owner and group only.",
            "chown changes owner and optionally group; chgrp changes only the group.",
            "Recursive chmod and chown are high-risk operations on production systems.",
            "The service user, not the admin's interactive user, must have the required access.",
        ],
        [
            {
                "title": "Set safe Odoo configuration permissions",
                "code": """sudo chown root:odoo /etc/odoo/odoo.conf
sudo chmod 640 /etc/odoo/odoo.conf
ls -l /etc/odoo/odoo.conf
sudo -u odoo test -r /etc/odoo/odoo.conf && echo "odoo can read config" """,
                "explain": (
                    "The root user owns the file so the service cannot silently rewrite it, while the odoo group can read it. "
                    "Testing as the odoo user is more reliable than assuming permissions are correct from an admin shell."
                ),
            },
            {
                "title": "Repair ownership of a custom addon",
                "code": """sudo chown -R odoo:odoo /opt/odoo/custom-addons/my_module
find /opt/odoo/custom-addons/my_module -type d -exec chmod 750 {} \\;
find /opt/odoo/custom-addons/my_module -type f -exec chmod 640 {} \\;""",
                "explain": (
                    "Directories and files often need different execute bits, so a single recursive chmod is rarely ideal. "
                    "This pattern keeps source readable by the service while avoiding broad write access."
                ),
            },
        ],
        [
            "Using chmod 777 as a troubleshooting shortcut and leaving it in place.",
            "Forgetting execute permission on parent directories.",
            "Changing ownership of system directories recursively from the wrong path.",
            "Testing access as root instead of the service user.",
        ],
        "In /tmp/odoo-permission-lab, create a config file and addon directory. Set ownership and permissions so a simulated odoo user can read them but an unrelated user cannot modify them.",
        [
            {
                "kind": "callout",
                "title": "Production rule",
                "text": "If the fix requires chmod 777, the real problem has not been understood yet.",
            }
        ],
    ),
    _lesson(
        "L05",
        "Users, Groups, and sudo",
        [
            "Explain why services should run under dedicated users.",
            "Inspect users, groups, and sudo privileges.",
            "Use sudo intentionally without hiding ownership problems.",
            "Separate human admin access from application runtime access.",
        ],
        "identity and privilege separation",
        "user IDs, group memberships, service accounts, sudo rules, and command auditing",
        "running application processes as root and widening the blast radius of a compromise",
        "Odoo service users need predictable file access while administrators need controlled elevation for maintenance",
        "Use sudo to perform administrative tasks, not to make normal application operations depend on root.",
        [
            "Each process runs with a user ID and group IDs that determine access checks.",
            "A service account should own only the files it must manage.",
            "sudo records administrative intent and can restrict which users may run privileged commands.",
            "Group membership is a clean way to grant shared read or write access.",
            "Human users should log in individually instead of sharing one admin password.",
            "Root-owned runtime files often reveal that a command was run with the wrong identity.",
        ],
        [
            {
                "title": "Inspect identity and group membership",
                "code": """id
id odoo
getent passwd odoo
getent group odoo
sudo -l""",
                "explain": (
                    "These commands answer who you are, who the service user is, and what privileged commands are allowed. "
                    "The output is essential when a file is readable in your shell but not by the Odoo service."
                ),
            },
            {
                "title": "Run a check as the service user",
                "code": """sudo -u odoo -H bash -lc 'whoami; pwd; python3 --version'
sudo -u odoo -H test -x /opt/odoo/venv/bin/python && echo "venv executable" """,
                "explain": (
                    "Running a command as the service user reproduces the environment and access rules that systemd will use. "
                    "The -H flag sets HOME consistently so user-specific configuration does not leak from the admin account."
                ),
            },
        ],
        [
            "Running Odoo manually with sudo and creating root-owned cache files.",
            "Sharing one SSH account among administrators.",
            "Adding broad passwordless sudo rules without command boundaries.",
            "Changing service file ownership instead of fixing group membership.",
        ],
        "Create a lab service user, place it in a project group, and demonstrate a file that the group can read but cannot write. Then run a Python version check as that service user.",
    ),
    _lesson(
        "L06",
        "Processes with top, htop, ps, and kill",
        [
            "List processes and interpret PID, parent PID, state, CPU, and memory columns.",
            "Use top or htop to observe live server pressure.",
            "Terminate processes with the least disruptive signal first.",
            "Connect process behavior to Odoo worker and cron performance.",
        ],
        "runtime process observation and control",
        "PIDs, process states, parent-child relationships, CPU use, RSS memory, and signals",
        "killing the wrong worker or masking the underlying cause of resource exhaustion",
        "Odoo may run multiple HTTP workers, longpolling workers, cron workers, PostgreSQL sessions, and background jobs",
        "A kill command is a last step in an investigation, not the investigation itself.",
        [
            "ps gives a point-in-time process list; top and htop show live changes.",
            "PID identifies a process instance, while command names may repeat many times.",
            "SIGTERM asks a process to stop cleanly; SIGKILL stops it immediately and prevents cleanup.",
            "High CPU, high memory, and uninterruptible IO wait suggest different root causes.",
            "Parent PID helps distinguish systemd-managed services from manual shells.",
            "Repeatedly killing processes without logs creates unstable systems and lost evidence.",
        ],
        [
            {
                "title": "Find Odoo-related processes",
                "code": """ps -eo pid,ppid,user,stat,%cpu,%mem,etime,cmd --sort=-%mem | head -20
pgrep -a -u odoo python
top -o %MEM""",
                "explain": (
                    "Sorting by memory and filtering by the odoo user quickly reveals whether application workers dominate the server. "
                    "Elapsed time helps separate a fresh runaway process from a long-running service."
                ),
            },
            {
                "title": "Signal a process deliberately",
                "code": """sudo kill -TERM 12345
sleep 3
ps -p 12345 -o pid,stat,cmd
sudo kill -KILL 12345  # only if the process ignored TERM and impact is understood""",
                "explain": (
                    "TERM gives the process a chance to close files and database connections cleanly. "
                    "KILL should be explicit and documented because it can interrupt transactions or leave temporary files behind."
                ),
            },
        ],
        [
            "Using kill -9 as the first response.",
            "Matching processes by a vague name and terminating unrelated commands.",
            "Ignoring parent processes that will immediately restart the child.",
            "Confusing memory percent with actual RSS on large-memory servers.",
        ],
        "Start a harmless sleep process, find it with ps and pgrep, send TERM, confirm it exited, then repeat with a Python process that prints its PID and handles KeyboardInterrupt.",
    ),
    _lesson(
        "L07",
        "systemd Services",
        [
            "Explain systemd units, service states, and restart policies.",
            "Inspect and manage Odoo service lifecycle with systemctl.",
            "Understand unit files, drop-ins, and daemon reloads.",
            "Use systemd status output as a first troubleshooting artifact.",
        ],
        "service supervision and repeatable startup",
        "unit names, active state, main PID, ExecStart, environment, dependencies, and restart behavior",
        "starting Odoo manually and leaving production outside the service manager",
        "systemd keeps Odoo, PostgreSQL, and Nginx predictable across reboots and failures",
        "If systemd is responsible for the service, always ask systemd what it thinks before changing files.",
        [
            "A service unit describes how a daemon starts, stops, reloads, and restarts.",
            "systemctl status combines state, main PID, recent logs, and exit code context.",
            "After editing unit files or drop-ins, run systemctl daemon-reload.",
            "Restart policies should match the failure mode and avoid tight crash loops.",
            "EnvironmentFile and WorkingDirectory affect how Python and Odoo locate resources.",
            "Manual starts should be used only for controlled diagnostics and then stopped.",
        ],
        [
            {
                "title": "Inspect and restart an Odoo service",
                "code": """sudo systemctl status odoo --no-pager
sudo systemctl cat odoo
sudo systemctl restart odoo
sudo systemctl is-active odoo""",
                "explain": (
                    "status answers whether the service is active and shows the immediate failure context if it is not. "
                    "cat displays the effective unit content, including drop-ins, which prevents debugging the wrong file."
                ),
            },
            {
                "title": "Create a safe override directory",
                "code": """sudo systemctl edit odoo
# Add only the changed settings in the editor, for example:
# [Service]
# Restart=on-failure
sudo systemctl daemon-reload
sudo systemctl restart odoo""",
                "explain": (
                    "Drop-ins preserve vendor or deployment unit files while making local changes explicit. "
                    "daemon-reload is required because systemd caches unit definitions."
                ),
            },
        ],
        [
            "Editing a unit file and restarting without daemon-reload.",
            "Debugging an old service name while the active unit has a different name.",
            "Running Odoo manually and assuming systemd uses the same environment.",
            "Setting Restart=always without understanding a crash loop.",
        ],
        "Inspect a sample odoo.service unit, identify ExecStart, User, Group, WorkingDirectory, and EnvironmentFile, then create a hypothetical drop-in that changes only the restart policy.",
    ),
    _lesson(
        "L08",
        "journalctl and Log Files",
        [
            "Read systemd journal entries for a service.",
            "Filter logs by unit, time range, priority, and boot.",
            "Combine journal output with application log files.",
            "Preserve useful evidence during Odoo incidents.",
        ],
        "log-based investigation",
        "unit filters, timestamps, boot IDs, priority levels, application log paths, and rotation",
        "losing the first failure message by only looking at the last repeated error",
        "Odoo logs often show Python tracebacks while systemd logs show process exit, restart, and environment failures",
        "Start with the first error in the relevant time window, then follow the chain forward.",
        [
            "journalctl -u filters logs for a systemd unit.",
            "The --since and --until options keep searches tied to the incident window.",
            "The current boot can be selected with -b, and previous boots with -b -1.",
            "Application logs may live in /var/log/odoo or another configured path.",
            "Tracebacks should be read from top context to final exception, not just the last line.",
            "Log rotation can move older evidence into compressed files.",
        ],
        [
            {
                "title": "Read recent service logs",
                "code": """sudo journalctl -u odoo --since "30 minutes ago" --no-pager
sudo journalctl -u odoo -p warning..alert --since today --no-pager
sudo journalctl -u odoo -b --no-pager | tail -80""",
                "explain": (
                    "The first command establishes recent context, the second focuses on warnings and errors, and the third stays within the current boot. "
                    "Time filters prevent unrelated old failures from confusing the incident timeline."
                ),
            },
            {
                "title": "Follow application logs during restart",
                "code": """sudo tail -F /var/log/odoo/odoo.log
# In another terminal:
sudo systemctl restart odoo""",
                "explain": (
                    "Following the application log during a restart shows startup module loading, database connection failures, and Python exceptions as they happen. "
                    "Use this with journalctl status so you see both Odoo's view and systemd's view."
                ),
            },
        ],
        [
            "Searching logs without a time window.",
            "Reading only the final traceback line and missing the real cause above it.",
            "Ignoring systemd restart messages when the application log is empty.",
            "Overwriting logs during cleanup before preserving the incident evidence.",
        ],
        "Restart a harmless sample service or timer, collect journal entries for the last 10 minutes, identify the first and last relevant lines, and write a five-line incident timeline.",
    ),
    _lesson(
        "L09",
        "Editing Files with nano and vim",
        [
            "Choose nano or vim based on task complexity and operator comfort.",
            "Open, edit, save, and exit safely in both editors.",
            "Avoid accidental configuration damage while editing as root.",
            "Validate edits before restarting services.",
        ],
        "terminal editing discipline",
        "editor modes, save behavior, sudo usage, temporary files, syntax visibility, and post-edit validation",
        "making an invisible typo in a production configuration file",
        "Odoo and Nginx configuration changes often need exact key names, indentation, and path values",
        "The best editor is the one you can exit reliably during an incident.",
        [
            "nano is approachable for small edits and displays common shortcuts.",
            "vim is modal, powerful, and widely available on servers.",
            "Always back up important files before editing them as root.",
            "Use validation commands before restarting services that depend on edited config.",
            "sudoedit can be safer than running a full editor process as root.",
            "Editor swap and backup files should not be left where applications will load them.",
        ],
        [
            {
                "title": "Safe edit sequence",
                "code": """sudo cp -a /etc/odoo/odoo.conf /etc/odoo/odoo.conf.pre-edit
sudoedit /etc/odoo/odoo.conf
sudo diff -u /etc/odoo/odoo.conf.pre-edit /etc/odoo/odoo.conf""",
                "explain": (
                    "sudoedit copies the file to a temporary location, opens it with your editor, and writes it back with elevated permissions. "
                    "The diff provides a review checkpoint before the changed service is restarted."
                ),
            },
            {
                "title": "Essential vim commands",
                "code": """vim /tmp/example.conf
# i        enter insert mode
# Esc      return to normal mode
# :w       write file
# :q       quit
# :wq      write and quit
# :q!      quit without saving""",
                "explain": (
                    "Most vim emergencies come from not recognizing insert mode versus normal mode. "
                    "Knowing these commands is enough to make a controlled edit or escape safely."
                ),
            },
        ],
        [
            "Opening a root editor without a backup.",
            "Saving editor temporary files in a directory that is scanned by Odoo.",
            "Restarting services before checking a diff or validation command.",
            "Panicking in vim instead of pressing Esc and using :q! to exit without saving.",
        ],
        "Edit a copied sample config with both nano and vim. Change one value, save it, show the diff, then intentionally abandon a second change without saving.",
    ),
    _lesson(
        "L10",
        "Networking with ip, ping, and ss",
        [
            "Inspect IP addresses, routes, and listening sockets.",
            "Use ping for basic reachability without overinterpreting it.",
            "Use ss to confirm which process owns a port.",
            "Troubleshoot Odoo, PostgreSQL, and reverse proxy connectivity.",
        ],
        "network observation from the host",
        "interfaces, addresses, routes, DNS assumptions, TCP ports, process ownership, and listening bind addresses",
        "assuming the application is broken when the port is not listening or traffic is routed elsewhere",
        "Odoo typically listens on localhost or a private interface while Nginx exposes HTTP and HTTPS to users",
        "Separate reachability, name resolution, listening state, firewall policy, and application response.",
        [
            "ip addr shows interface addresses; ip route shows where packets will go.",
            "ping tests ICMP reachability, not whether TCP application ports are open.",
            "ss -ltnp shows listening TCP sockets and owning processes.",
            "A service bound to 127.0.0.1 is reachable locally but not from another host.",
            "PostgreSQL and Odoo ports should usually be private, with Nginx handling public HTTP.",
            "Network troubleshooting improves when each layer is tested independently.",
        ],
        [
            {
                "title": "Inspect addresses, routes, and ports",
                "code": """ip addr show
ip route show
ping -c 3 8.8.8.8
ss -ltnp | grep -E ':(8069|8072|80|443|5432)\\b'""",
                "explain": (
                    "The commands move from host addressing to routing, reachability, and listening sockets. "
                    "For Odoo, the socket list often reveals whether the service is bound only to localhost or exposed more broadly."
                ),
            },
            {
                "title": "Test an Odoo port locally",
                "code": """curl -I http://127.0.0.1:8069
curl -I http://localhost:8069
ss -ltnp 'sport = :8069'""",
                "explain": (
                    "A local HTTP check proves the application responds before investigating DNS, load balancers, or public firewalls. "
                    "The ss filter confirms which process owns the port."
                ),
            },
        ],
        [
            "Treating a successful ping as proof that HTTP or PostgreSQL works.",
            "Forgetting that localhost from one container or VM is not another host's localhost.",
            "Leaving Odoo bound to a public interface unnecessarily.",
            "Ignoring DNS and testing only raw IP addresses.",
        ],
        "Draw a simple network path from browser to Nginx to Odoo to PostgreSQL. On a lab host, collect ip addr, ip route, and ss output and label which ports should be public.",
    ),
    _lesson(
        "L11",
        "SSH Keys and Hardening",
        [
            "Explain public-key SSH authentication.",
            "Generate and install SSH keys safely.",
            "Apply basic sshd hardening for production servers.",
            "Avoid locking yourself out during access changes.",
        ],
        "secure remote administration",
        "key pairs, authorized_keys, sshd_config, password login, root login, ports, and active sessions",
        "weakening or breaking the only administrative access path to a production host",
        "Odoo servers need secure admin access because shell access often implies database, file, and secret access",
        "Make SSH changes with a second session open and a rollback path ready.",
        [
            "The private key stays on the client; the public key is placed on the server.",
            "authorized_keys controls which public keys can log in as a user.",
            "PasswordAuthentication no reduces brute-force risk after keys are confirmed.",
            "PermitRootLogin no encourages named users and sudo auditability.",
            "sshd configuration should be tested before reload or restart.",
            "Firewall and cloud security group rules must match the chosen SSH port.",
        ],
        [
            {
                "title": "Create and install a key",
                "code": """ssh-keygen -t ed25519 -C "admin@example.com"
ssh-copy-id admin@odoo-server.example.com
ssh admin@odoo-server.example.com 'whoami; hostname'""",
                "explain": (
                    "Ed25519 keys are compact and strong for modern SSH clients. "
                    "The final command proves the key works before password login is disabled."
                ),
            },
            {
                "title": "Test sshd configuration before reload",
                "code": """sudo cp -a /etc/ssh/sshd_config /etc/ssh/sshd_config.pre-hardening
sudoedit /etc/ssh/sshd_config
sudo sshd -t
sudo systemctl reload ssh""",
                "explain": (
                    "sshd -t validates syntax without applying the configuration. "
                    "Reload keeps existing sessions alive, which is safer than a restart while verifying access."
                ),
            },
        ],
        [
            "Disabling password login before confirming key login works.",
            "Closing the only active session immediately after changing sshd_config.",
            "Sharing one private key across administrators.",
            "Changing the SSH port without updating firewall or cloud rules.",
        ],
        "On a disposable VM, create a new SSH key, install it for a non-root user, test login, then draft a hardened sshd_config snippet with comments explaining each setting.",
    ),
    _lesson(
        "L12",
        "Environment Variables and bashrc",
        [
            "Read and set environment variables in a shell.",
            "Distinguish shell startup files from systemd service environments.",
            "Use PATH, HOME, and application variables intentionally.",
            "Avoid hiding production settings in interactive-only files.",
        ],
        "process environment configuration",
        "exported variables, shell startup order, PATH lookup, virtual environments, and systemd EnvironmentFile usage",
        "testing with variables from .bashrc that the Odoo service never receives",
        "Odoo configuration may depend on PATH, Python virtual environments, locale, addons paths, and database connection variables",
        "If a service needs a value, put it in the service configuration path, not only in an interactive shell profile.",
        [
            "Environment variables are inherited from parent process to child process.",
            "export makes a shell variable available to child processes.",
            ".bashrc affects interactive bash shells, not all services.",
            "PATH controls command lookup order and can explain different Python binaries.",
            "systemd units can use Environment and EnvironmentFile for service-specific values.",
            "Secrets in environment files need strict ownership and permissions.",
        ],
        [
            {
                "title": "Inspect shell environment",
                "code": """echo "$PATH"
printenv | sort | grep -E '^(HOME|LANG|PATH|VIRTUAL_ENV)='
command -v python3
python3 -c 'import sys; print(sys.executable)'""",
                "explain": (
                    "These commands show which executable the shell will run and which inherited values are visible. "
                    "A mismatch between command -v and service ExecStart is a frequent source of deployment confusion."
                ),
            },
            {
                "title": "Use an EnvironmentFile with systemd",
                "code": """sudo install -m 640 -o root -g odoo /dev/null /etc/odoo/odoo.env
echo 'ODOO_RC=/etc/odoo/odoo.conf' | sudo tee -a /etc/odoo/odoo.env
sudo systemctl edit odoo
# [Service]
# EnvironmentFile=/etc/odoo/odoo.env""",
                "explain": (
                    "An environment file makes service configuration explicit and auditable. "
                    "The permissions allow the odoo group to read values while preventing broad disclosure."
                ),
            },
        ],
        [
            "Adding production variables only to ~/.bashrc and expecting systemd to see them.",
            "Modifying PATH globally when only one service needs a specific executable.",
            "Storing secrets in world-readable environment files.",
            "Assuming sudo preserves the caller's full environment.",
        ],
        "Create a shell variable and an exported variable, run a child Python command that prints os.environ, and explain why only one value is visible. Then draft a service EnvironmentFile for a sample Odoo variable.",
    ),
    _lesson(
        "L13",
        "Cron Jobs",
        [
            "Understand cron timing syntax and execution environment.",
            "Create safe scheduled maintenance tasks.",
            "Redirect cron output for observability.",
            "Avoid conflicts between cron and Odoo's internal scheduler.",
        ],
        "scheduled command execution",
        "minute, hour, day fields, user crontabs, system crontabs, PATH, working directory, and output handling",
        "running a maintenance command with a minimal cron environment and no logs",
        "Odoo has its own scheduled actions, but server tasks such as backups, cleanup, and certificate checks may use cron",
        "Every cron job should state who runs it, what environment it expects, where output goes, and how failure is noticed.",
        [
            "User crontabs run as that user; /etc/cron.d entries include a user field.",
            "Cron has a small environment and often a different PATH from interactive shells.",
            "Use absolute paths for commands and files in cron jobs.",
            "Redirect stdout and stderr to logs or monitoring hooks.",
            "Locking prevents overlapping runs when a previous job is slow.",
            "Odoo database backups should be tested for restore, not just scheduled for creation.",
        ],
        [
            {
                "title": "A safe backup cron pattern",
                "code": """# /etc/cron.d/odoo-backup
SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

15 2 * * * postgres flock -n /var/lock/odoo-backup.lock /usr/local/bin/backup-odoo-db >> /var/log/odoo/backup.log 2>&1""",
                "explain": (
                    "This system cron entry declares its shell and PATH, runs as postgres, prevents overlap with flock, and captures output. "
                    "The command still needs a tested script and restore procedure before it is considered production-ready."
                ),
            },
            {
                "title": "Preview a cron schedule",
                "code": """crontab -l
systemctl list-timers --all
grep -R "backup-odoo" /etc/cron* 2>/dev/null""",
                "explain": (
                    "Servers may use both cron and systemd timers, so list both before assuming how scheduling works. "
                    "Searching cron directories identifies system-wide jobs that are not visible in a user's crontab."
                ),
            },
        ],
        [
            "Using relative paths in cron commands.",
            "Ignoring stderr so failures disappear into local mail or nowhere.",
            "Scheduling backups without restore tests.",
            "Letting slow jobs overlap and overload the database server.",
        ],
        "Write a cron entry that runs a harmless script every five minutes, logs stdout and stderr, and uses flock. Then intentionally remove PATH from the script and explain the failure.",
    ),
    _lesson(
        "L14",
        "APT Package Management",
        [
            "Update package metadata and install packages with apt.",
            "Understand repositories, package versions, and upgrades.",
            "Inspect installed packages and service changes.",
            "Apply package changes safely on Odoo servers.",
        ],
        "Debian and Ubuntu package lifecycle",
        "apt update, apt install, apt upgrade, repositories, package holds, service restarts, and changelog awareness",
        "upgrading core packages during business hours without understanding service impact",
        "Odoo servers depend on OS packages for Python, PostgreSQL clients, Nginx, wkhtmltopdf alternatives, fonts, and build tools",
        "Treat package changes like deployments: review, schedule, apply, verify, and record.",
        [
            "apt update refreshes metadata; it does not upgrade installed packages.",
            "apt install changes the system and may start or restart services.",
            "apt-cache policy shows candidate versions and repositories.",
            "apt-mark hold can prevent a sensitive package from upgrading unexpectedly.",
            "Security updates are important but still need operational timing.",
            "Build dependencies should be removed or minimized on hardened production hosts.",
        ],
        [
            {
                "title": "Inspect and install a package",
                "code": """sudo apt update
apt-cache policy nginx
sudo apt install nginx
dpkg -l | grep '^ii' | grep nginx
systemctl status nginx --no-pager""",
                "explain": (
                    "The policy command shows where the package will come from before installation. "
                    "After installing, verify both package state and the service that the package may have started."
                ),
            },
            {
                "title": "Review pending upgrades",
                "code": """sudo apt update
apt list --upgradable
sudo apt -s upgrade""",
                "explain": (
                    "The simulated upgrade shows planned actions without changing the server. "
                    "Use it before maintenance windows to identify packages that may restart services or require reboots."
                ),
            },
        ],
        [
            "Confusing apt update with apt upgrade.",
            "Installing from random third-party repositories without trust or maintenance review.",
            "Upgrading PostgreSQL-related packages without checking database compatibility.",
            "Leaving build tools installed on minimal production machines unnecessarily.",
        ],
        "On a lab Ubuntu system, inspect the candidate version of nginx, run a simulated upgrade, install a small package, and record which services changed state.",
    ),
    _lesson(
        "L15",
        "Disk and Memory Usage with df, du, and free",
        [
            "Measure filesystem capacity with df.",
            "Find large directories and files with du.",
            "Interpret memory and swap information with free.",
            "Connect disk and memory pressure to Odoo failures.",
        ],
        "capacity and pressure diagnosis",
        "mounted filesystems, inode use, directory growth, cache memory, swap use, and database storage paths",
        "cleaning the wrong directory while the full filesystem remains full",
        "Odoo attachments, logs, PostgreSQL data, backups, and temporary exports can grow independently",
        "Always identify the full mount point before deleting data.",
        [
            "df -h shows filesystem capacity by mount point.",
            "df -ih shows inode usage, which can be exhausted even when space remains.",
            "du -sh summarizes directory size; sort helps find the largest consumers.",
            "free -h separates used memory from available memory and filesystem cache.",
            "Swap activity can indicate memory pressure but is not automatically bad.",
            "Database and filestore cleanup require application-aware retention rules.",
        ],
        [
            {
                "title": "Find the full mount and largest directories",
                "code": """df -h
df -ih
sudo du -xhd1 /var | sort -h
sudo du -xhd1 /opt | sort -h""",
                "explain": (
                    "The -x flag keeps du on one filesystem, which prevents chasing data across mounted volumes. "
                    "Checking inodes helps diagnose failures caused by too many small files, such as excessive sessions or attachments."
                ),
            },
            {
                "title": "Inspect memory pressure",
                "code": """free -h
vmstat 1 5
ps -eo pid,user,%mem,rss,cmd --sort=-rss | head -15""",
                "explain": (
                    "free shows available memory, vmstat shows activity over time, and ps identifies the largest resident processes. "
                    "Together they distinguish a busy but healthy cache from a server that is swapping heavily."
                ),
            },
        ],
        [
            "Deleting files from a different mount point than the one that is full.",
            "Ignoring inode exhaustion.",
            "Clearing application data without retention approval.",
            "Mistaking Linux filesystem cache for wasted memory.",
        ],
        "Fill a small lab directory with test files, use du to find the largest path, then remove only the test data. Record df output before and after and explain why the numbers changed.",
    ),
    _lesson(
        "L16",
        "UFW Firewall",
        [
            "Explain host firewall allow and deny rules.",
            "Use UFW to expose only required services.",
            "Verify firewall status before and after changes.",
            "Design firewall policy for an Odoo server behind a reverse proxy.",
        ],
        "host-level network policy",
        "default policies, allowed ports, source restrictions, IPv4 and IPv6, ordering, and rollback",
        "locking out SSH or exposing internal Odoo and PostgreSQL ports publicly",
        "a typical Odoo host should expose SSH and HTTPS while keeping PostgreSQL and backend Odoo ports private",
        "Before enabling a firewall, confirm the active SSH rule in the same session.",
        [
            "UFW is a friendly interface over Linux firewall rules.",
            "Default deny incoming and allow outgoing is common for application hosts.",
            "Rules can restrict source IPs for SSH or administrative ports.",
            "Nginx should usually expose 80 and 443; Odoo 8069 should stay private.",
            "IPv6 must be considered if the host has public IPv6 addresses.",
            "Firewall changes need verification from both local and remote perspectives.",
        ],
        [
            {
                "title": "Enable a conservative Odoo firewall",
                "code": """sudo ufw status verbose
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
sudo ufw status numbered""",
                "explain": (
                    "This allows administration and public web traffic while denying other incoming connections. "
                    "OpenSSH should be allowed before enabling UFW to avoid cutting off the active session."
                ),
            },
            {
                "title": "Restrict SSH to an admin network",
                "code": """sudo ufw delete allow OpenSSH
sudo ufw allow from 203.0.113.0/24 to any port 22 proto tcp
sudo ufw status numbered""",
                "explain": (
                    "Source-restricted SSH reduces attack surface when administrators connect from known networks. "
                    "Apply this only after confirming the actual admin source ranges and any VPN paths."
                ),
            },
        ],
        [
            "Enabling UFW before allowing SSH.",
            "Exposing PostgreSQL or Odoo backend ports to the entire internet.",
            "Forgetting IPv6 rules on dual-stack hosts.",
            "Deleting numbered rules without rechecking numbers after each deletion.",
        ],
        "Design a UFW policy for a single-server Odoo deployment with Nginx, PostgreSQL local only, and SSH from a VPN range. Explain every allowed port.",
    ),
    _lesson(
        "L17",
        "Production Directory Layout for Odoo",
        [
            "Map common Odoo directories by responsibility.",
            "Separate source code, configuration, logs, data, backups, and virtual environments.",
            "Choose ownership and permissions for each area.",
            "Make deployments understandable for future maintainers.",
        ],
        "filesystem organization for maintainable deployments",
        "config paths, addons paths, virtualenvs, logs, filestore, backups, releases, and ownership boundaries",
        "mixing code, data, and backups until upgrades and restores become unsafe",
        "Odoo deployments require clear paths for core source, custom addons, enterprise addons, Python environment, configuration, logs, and filestore",
        "A directory layout is operational documentation; if it is surprising, it will fail during incidents.",
        [
            "/etc/odoo is a natural place for root-owned configuration.",
            "/opt/odoo often holds application source, releases, addons, and virtual environments.",
            "/var/log/odoo should contain logs with rotation configured.",
            "/var/lib/odoo holds runtime data such as filestore when using packaged conventions.",
            "Backups should be isolated from live code and tested for restore.",
            "Symlinked release directories make rollback easier when used carefully.",
        ],
        [
            {
                "title": "Example directory map",
                "code": """/etc/odoo/odoo.conf
/opt/odoo/src/odoo
/opt/odoo/enterprise
/opt/odoo/custom-addons/current
/opt/odoo/venv
/var/lib/odoo/.local/share/Odoo/filestore
/var/log/odoo/odoo.log
/srv/backups/odoo""",
                "explain": (
                    "This layout separates configuration, source, virtual environment, runtime data, logs, and backups. "
                    "The exact paths may vary, but the responsibilities should remain explicit."
                ),
            },
            {
                "title": "Check ownership boundaries",
                "code": """sudo namei -l /etc/odoo/odoo.conf
sudo namei -l /opt/odoo/custom-addons/current
sudo -u odoo test -r /etc/odoo/odoo.conf && echo readable
sudo -u odoo test -w /etc/odoo/odoo.conf || echo not writable""",
                "explain": (
                    "namei shows permissions on each path component, which catches parent-directory traversal problems. "
                    "The tests confirm the service can read configuration but cannot casually rewrite it."
                ),
            },
        ],
        [
            "Storing backups inside the live addons path.",
            "Letting the service user own root-level configuration.",
            "Putting virtual environments in home directories tied to human users.",
            "Using undocumented paths that only one administrator understands.",
        ],
        "Design a directory layout for a production Odoo server. Include owner, group, permission mode, backup policy, and which paths are referenced by the systemd service.",
        [
            {
                "kind": "table",
                "title": "Directory responsibilities",
                "headers": ["Path", "Typical owner", "Responsibility"],
                "rows": [
                    ["/etc/odoo", "root:odoo", "Service configuration"],
                    ["/opt/odoo", "odoo:odoo", "Source, addons, and virtualenv"],
                    ["/var/log/odoo", "odoo:adm", "Application logs"],
                    ["/srv/backups/odoo", "root:backup", "Restore-tested backups"],
                ],
            }
        ],
    ),
    _lesson(
        "L18",
        "Troubleshooting Checklist for Odoo Servers",
        [
            "Apply a structured checklist during Odoo outages.",
            "Collect evidence before changing the server.",
            "Move from infrastructure checks to application checks logically.",
            "Write concise incident notes and next actions.",
        ],
        "systematic production troubleshooting",
        "symptom scope, recent changes, service state, logs, ports, resources, database reachability, and rollback options",
        "making multiple untracked changes and losing the ability to identify the fix",
        "Odoo availability depends on systemd, Python, Odoo configuration, PostgreSQL, Nginx, disk, memory, and network policy",
        "A checklist is not bureaucracy; it is how you keep judgment available under pressure.",
        [
            "Start by defining the user-visible symptom and scope.",
            "Check recent changes before assuming random failure.",
            "Inspect service state, logs, ports, disk, memory, and database connectivity.",
            "Make one change at a time and record its result.",
            "Prefer rollback when a recent deployment caused the incident.",
            "Close the loop with prevention work, not just restoration.",
        ],
        [
            {
                "title": "First five minutes of an Odoo outage",
                "code": """date -Is
sudo systemctl status odoo nginx postgresql --no-pager
sudo journalctl -u odoo --since "20 minutes ago" --no-pager | tail -120
ss -ltnp | grep -E ':(80|443|8069|5432)\\b'
df -h
free -h""",
                "explain": (
                    "This captures time, service state, recent Odoo logs, listening ports, disk, and memory in a repeatable order. "
                    "It avoids the common mistake of restarting first and destroying useful failure context."
                ),
            },
            {
                "title": "Check database reachability as Odoo",
                "code": """sudo -u odoo -H bash -lc '
  source /opt/odoo/venv/bin/activate
  python - <<PY
import psycopg2
conn = psycopg2.connect(dbname="postgres", user="odoo", host="127.0.0.1")
print("database connection ok")
conn.close()
PY
'""",
                "explain": (
                    "Testing from the service user's Python environment verifies more than raw network connectivity. "
                    "It checks that the expected library, credentials path, and database access all work together."
                ),
            },
        ],
        [
            "Restarting every service before collecting evidence.",
            "Changing several variables at once during an incident.",
            "Ignoring recent deployments, package upgrades, or certificate renewals.",
            "Stopping after recovery without writing the prevention task.",
        ],
        "Use the checklist against a deliberately broken lab Odoo-like service. Record observations, identify the failing layer, make one fix, verify recovery, and write a brief post-incident note.",
        [
            {
                "kind": "bullets",
                "title": "Incident order",
                "items": [
                    "State the symptom and time window.",
                    "Collect systemd, logs, ports, disk, memory, and database facts.",
                    "Form one hypothesis and test it.",
                    "Apply one reversible change.",
                    "Verify user impact and document prevention.",
                ],
            }
        ],
    ),
]

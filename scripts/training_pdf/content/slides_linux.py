"""Atomic Linux presentation slides for Merit Advisory Odoo training."""

SLIDES = [
    {
        "section": 1,
        "title": "Getting oriented in the terminal",
        "topics": [
            {
                "id": "L-PWD",
                "title": "pwd - Print Working Directory",
                "points": [
                    "Stands for Print Working Directory and shows the full path of your current folder.",
                    "Use it before running file commands so you know exactly where you are.",
                    "In scripts, capture it when you need to reuse the current path.",
                ],
                "examples": [
                    {"label": "Show current path", "code": "pwd"},
                    {"label": "Print path in a message", "code": "echo \"You are in: $(pwd)\""},
                ],
            },
            {
                "id": "L-CD-HOME",
                "title": "cd - Go to your home folder",
                "points": [
                    "The cd command changes the folder your shell is working in.",
                    "Running cd with no path takes you back to your home folder.",
                    "The tilde character is a shortcut for your home folder.",
                ],
                "examples": [
                    {"label": "Return home", "code": "cd"},
                    {"label": "Open home downloads", "code": "cd ~/Downloads"},
                ],
            },
            {
                "id": "L-CD-PARENT",
                "title": "cd .. - Move up one folder",
                "points": [
                    "Two dots mean the parent folder of your current location.",
                    "Use cd .. when you need to move one level higher in the folder tree.",
                    "Check with pwd after moving if you are not sure where you landed.",
                ],
                "examples": [
                    {"label": "Move up one level", "code": "cd .."},
                    {"label": "Move up twice", "code": "cd ../.."},
                ],
            },
            {
                "id": "L-CD-ABSOLUTE",
                "title": "cd with absolute paths",
                "points": [
                    "An absolute path starts with a slash and works from anywhere.",
                    "Use absolute paths when you want commands to be unambiguous.",
                    "Production commands are safer when the path is written completely.",
                ],
                "examples": [
                    {"label": "Open Odoo directory", "code": "cd /opt/odoo"},
                    {"label": "Open log directory", "code": "cd /var/log"},
                ],
            },
            {
                "id": "L-CD-RELATIVE",
                "title": "cd with relative paths",
                "points": [
                    "A relative path starts from the folder you are currently in.",
                    "Relative paths are short and useful while working inside a project.",
                    "They can be risky if you forget your current folder.",
                ],
                "examples": [
                    {"label": "Open a child folder", "code": "cd addons"},
                    {"label": "Move to a sibling folder", "code": "cd ../custom_addons"},
                ],
            },
            {
                "id": "L-LS",
                "title": "ls - List files",
                "points": [
                    "The ls command shows files and folders in the current location.",
                    "Use it after cd to confirm what is available before opening or editing files.",
                    "Plain ls is quick when you only need names.",
                ],
                "examples": [
                    {"label": "List current folder", "code": "ls"},
                    {"label": "List a specific folder", "code": "ls /opt/odoo"},
                ],
            },
            {
                "id": "L-LS-L",
                "title": "ls -l - Long listing",
                "points": [
                    "The -l option shows permissions, owner, group, size, and date.",
                    "Use it when checking who owns a file or whether it is executable.",
                    "Long listings are useful before changing permissions.",
                ],
                "examples": [
                    {"label": "Show details", "code": "ls -l"},
                    {"label": "Check an Odoo config", "code": "ls -l /etc/odoo.conf"},
                ],
            },
            {
                "id": "L-LS-AH",
                "title": "ls -a -h - Hidden and readable sizes",
                "points": [
                    "The -a option shows hidden files that start with a dot.",
                    "The -h option makes sizes easier to read when used with -l.",
                    "Use these flags to inspect shell files and large folders clearly.",
                ],
                "examples": [
                    {"label": "Show hidden files", "code": "ls -a"},
                    {"label": "Show readable details", "code": "ls -lah /var/log"},
                ],
            },
            {
                "id": "L-TREE",
                "title": "tree - View folder structure",
                "points": [
                    "The tree command displays folders and files as a visual hierarchy.",
                    "It helps beginners understand project layouts faster than repeated ls commands.",
                    "Limit the depth when a project has many files.",
                ],
                "examples": [
                    {"label": "Show current structure", "code": "tree"},
                    {"label": "Show two levels", "code": "tree -L 2 /opt/odoo"},
                ],
            },
        ],
    },
    {
        "section": 2,
        "title": "Working with files and folders",
        "topics": [
            {
                "id": "L-MKDIR",
                "title": "mkdir - Create folders",
                "points": [
                    "The mkdir command creates a new directory.",
                    "Use -p when parent folders may not exist yet.",
                    "Choose clear folder names so maintenance is easier later.",
                ],
                "examples": [
                    {"label": "Create one folder", "code": "mkdir reports"},
                    {"label": "Create nested folders", "code": "mkdir -p backups/2026/July"},
                ],
            },
            {
                "id": "L-TOUCH",
                "title": "touch - Create empty files",
                "points": [
                    "The touch command creates an empty file if it does not exist.",
                    "If the file already exists, touch updates its timestamp.",
                    "It is useful for quick notes, markers, and test files.",
                ],
                "examples": [
                    {"label": "Create a note file", "code": "touch notes.txt"},
                    {"label": "Create a log marker", "code": "touch /tmp/odoo-restart.marker"},
                ],
            },
            {
                "id": "L-CP-FILE",
                "title": "cp - Copy a file",
                "points": [
                    "The cp command copies a file to a new path.",
                    "Use it before editing important configuration files.",
                    "Give backups names that include the date or reason.",
                ],
                "examples": [
                    {"label": "Copy a file", "code": "cp odoo.conf odoo.conf.bak"},
                    {"label": "Copy into backup folder", "code": "cp /etc/odoo.conf ~/backups/odoo.conf"},
                ],
            },
            {
                "id": "L-CP-R",
                "title": "cp -r - Copy folders",
                "points": [
                    "The -r option copies directories recursively.",
                    "Recursive copy includes files and folders inside the source folder.",
                    "Confirm the destination before copying large project folders.",
                ],
                "examples": [
                    {"label": "Copy an addon folder", "code": "cp -r custom_addons/sale_report backups/"},
                    {"label": "Copy a config directory", "code": "cp -r /etc/nginx/sites-available ~/nginx-backup"},
                ],
            },
            {
                "id": "L-MV-RENAME",
                "title": "mv - Rename files",
                "points": [
                    "The mv command can rename a file in the same folder.",
                    "Renaming does not create a second copy.",
                    "Use clear names so old and new versions are easy to identify.",
                ],
                "examples": [
                    {"label": "Rename a draft", "code": "mv draft.txt meeting-notes.txt"},
                    {"label": "Rename a config backup", "code": "mv odoo.conf.bak odoo.conf.before-port-change"},
                ],
            },
            {
                "id": "L-MV-MOVE",
                "title": "mv - Move files",
                "points": [
                    "The mv command also moves files into another folder.",
                    "Moving changes the file path but keeps the same file content.",
                    "Check the destination folder before moving production files.",
                ],
                "examples": [
                    {"label": "Move a report", "code": "mv report.pdf archive/"},
                    {"label": "Move a downloaded addon", "code": "mv ~/Downloads/my_addon /opt/odoo/custom_addons/"},
                ],
            },
            {
                "id": "L-RM-FILE",
                "title": "rm - Remove files",
                "points": [
                    "The rm command deletes files.",
                    "Deleted files usually do not go to a recycle bin on servers.",
                    "Use ls first when the file name contains wildcards.",
                ],
                "examples": [
                    {"label": "Remove one file", "code": "rm old-notes.txt"},
                    {"label": "Preview before removing logs", "code": "ls *.tmp"},
                ],
            },
            {
                "id": "L-RM-R",
                "title": "rm -r - Remove folders carefully",
                "points": [
                    "The -r option deletes folders and everything inside them.",
                    "Use recursive deletion only after confirming the exact path.",
                    "On production systems, prefer moving a folder aside before deleting it.",
                ],
                "examples": [
                    {"label": "Remove a test folder", "code": "rm -r test-output"},
                    {"label": "Safer first step", "code": "mv old_addon old_addon.remove_after_backup"},
                ],
            },
            {
                "id": "L-CAT",
                "title": "cat - Print file contents",
                "points": [
                    "The cat command prints a whole file to the terminal.",
                    "Use it for short files such as simple notes or small config snippets.",
                    "Avoid cat for very large logs because it can flood the screen.",
                ],
                "examples": [
                    {"label": "Read a short file", "code": "cat README.md"},
                    {"label": "View Odoo config", "code": "cat /etc/odoo.conf"},
                ],
            },
            {
                "id": "L-LESS-MORE",
                "title": "less and more - Page through files",
                "points": [
                    "less opens a file one screen at a time.",
                    "Use slash inside less to search within the file.",
                    "more is simpler, but less is usually more comfortable for logs.",
                ],
                "examples": [
                    {"label": "Open a log", "code": "less /var/log/odoo/odoo.log"},
                    {"label": "Page through config", "code": "more /etc/odoo.conf"},
                ],
            },
            {
                "id": "L-HEAD-TAIL",
                "title": "head and tail - Start or end of files",
                "points": [
                    "head shows the beginning of a file.",
                    "tail shows the end of a file, which is useful for recent logs.",
                    "Use tail -f to follow new log lines while a service runs.",
                ],
                "examples": [
                    {"label": "Show first lines", "code": "head -20 /var/log/odoo/odoo.log"},
                    {"label": "Follow recent logs", "code": "tail -f /var/log/odoo/odoo.log"},
                ],
            },
            {
                "id": "L-GREP",
                "title": "grep - Search text",
                "points": [
                    "The grep command finds lines that contain matching text.",
                    "Use -i for case-insensitive searches.",
                    "Use grep to find errors, ports, usernames, or configuration keys.",
                ],
                "examples": [
                    {"label": "Search for errors", "code": "grep -i error /var/log/odoo/odoo.log"},
                    {"label": "Find a config setting", "code": "grep xmlrpc_port /etc/odoo.conf"},
                ],
            },
            {
                "id": "L-FIND",
                "title": "find - Locate files",
                "points": [
                    "The find command searches folders by name, type, size, or time.",
                    "Start with a specific folder so the search stays fast.",
                    "Quote patterns that contain wildcard characters.",
                ],
                "examples": [
                    {"label": "Find Python files", "code": "find /opt/odoo/custom_addons -name \"*.py\""},
                    {"label": "Find log files", "code": "find /var/log -type f -name \"*.log\""},
                ],
            },
        ],
    },
    {
        "section": 3,
        "title": "Users, groups, and permissions",
        "topics": [
            {
                "id": "L-CHMOD-NUMERIC",
                "title": "chmod numeric - Set permissions",
                "points": [
                    "chmod changes read, write, and execute permissions.",
                    "Numeric modes use 4 for read, 2 for write, and 1 for execute.",
                    "Common modes are 644 for files and 755 for executable folders.",
                ],
                "examples": [
                    {"label": "Set a normal file mode", "code": "chmod 644 odoo.conf"},
                    {"label": "Make a script executable", "code": "chmod 755 deploy.sh"},
                ],
            },
            {
                "id": "L-CHMOD-SYMBOLIC",
                "title": "chmod symbolic - Adjust permissions",
                "points": [
                    "Symbolic modes change permissions by user, group, or others.",
                    "Use + to add a permission and - to remove one.",
                    "Symbolic chmod is readable when making a small change.",
                ],
                "examples": [
                    {"label": "Add execute for owner", "code": "chmod u+x backup.sh"},
                    {"label": "Remove write from others", "code": "chmod o-w shared.conf"},
                ],
            },
            {
                "id": "L-CHOWN",
                "title": "chown - Change owner",
                "points": [
                    "chown changes which user owns a file or folder.",
                    "The owner controls permissions marked for user access.",
                    "Odoo files should usually be owned by the service user, not root.",
                ],
                "examples": [
                    {"label": "Change file owner", "code": "sudo chown odoo /etc/odoo.conf"},
                    {"label": "Change folder owner recursively", "code": "sudo chown -R odoo /opt/odoo/custom_addons"},
                ],
            },
            {
                "id": "L-CHGRP",
                "title": "chgrp - Change group",
                "points": [
                    "chgrp changes the group assigned to a file or folder.",
                    "Group permissions help teams share access without using one account.",
                    "Use groups to separate application access from administrator access.",
                ],
                "examples": [
                    {"label": "Change file group", "code": "sudo chgrp odoo /etc/odoo.conf"},
                    {"label": "Change addon group recursively", "code": "sudo chgrp -R odoo /opt/odoo/custom_addons"},
                ],
            },
            {
                "id": "L-USERS-GROUPS",
                "title": "Users and groups overview",
                "points": [
                    "A Linux user is an identity that owns processes and files.",
                    "A group collects users so permissions can be shared.",
                    "Service accounts such as odoo should run applications with limited access.",
                ],
                "examples": [
                    {"label": "List current user's groups", "code": "groups"},
                    {"label": "Show an account entry", "code": "getent passwd odoo"},
                ],
            },
            {
                "id": "L-SUDO",
                "title": "sudo - Run with administrator rights",
                "points": [
                    "sudo runs a command with elevated privileges.",
                    "Use it only for commands that really need administrator access.",
                    "Read the command twice before using sudo on production servers.",
                ],
                "examples": [
                    {"label": "Edit a system config", "code": "sudo nano /etc/odoo.conf"},
                    {"label": "Restart a service", "code": "sudo systemctl restart odoo"},
                ],
            },
            {
                "id": "L-WHOAMI-ID",
                "title": "whoami and id - Check identity",
                "points": [
                    "whoami prints the username of the current shell.",
                    "id shows the user id, group id, and group memberships.",
                    "Check identity before changing files or running service commands.",
                ],
                "examples": [
                    {"label": "Show current user", "code": "whoami"},
                    {"label": "Show full identity", "code": "id"},
                ],
            },
        ],
    },
    {
        "section": 4,
        "title": "Processes, services, logs, and editors",
        "topics": [
            {
                "id": "L-PS",
                "title": "ps - List processes",
                "points": [
                    "A process is a running program.",
                    "ps shows processes and their process ids.",
                    "Use ps to confirm whether Odoo, PostgreSQL, or Nginx is running.",
                ],
                "examples": [
                    {"label": "Show your processes", "code": "ps"},
                    {"label": "Find Odoo processes", "code": "ps aux | grep odoo"},
                ],
            },
            {
                "id": "L-TOP-HTOP",
                "title": "top and htop - Watch system activity",
                "points": [
                    "top shows live CPU, memory, and process activity.",
                    "htop is an easier interactive version when installed.",
                    "Use these tools when users report slowness or high load.",
                ],
                "examples": [
                    {"label": "Open top", "code": "top"},
                    {"label": "Open htop", "code": "htop"},
                ],
            },
            {
                "id": "L-KILL",
                "title": "kill - Stop a process by id",
                "points": [
                    "kill sends a signal to a process id.",
                    "The default signal asks the process to stop cleanly.",
                    "Use service commands before kill when systemd manages the process.",
                ],
                "examples": [
                    {"label": "Stop a process", "code": "kill 12345"},
                    {"label": "Force stop only if needed", "code": "kill -9 12345"},
                ],
            },
            {
                "id": "L-PKILL",
                "title": "pkill - Stop processes by name",
                "points": [
                    "pkill matches processes by name or pattern.",
                    "It is faster than finding each process id manually.",
                    "Use careful patterns so you do not stop unrelated work.",
                ],
                "examples": [
                    {"label": "Stop matching worker", "code": "pkill -f odoo-bin"},
                    {"label": "Preview matches first", "code": "pgrep -af odoo-bin"},
                ],
            },
            {
                "id": "L-SYSTEMCTL-STATUS",
                "title": "systemctl status - Check services",
                "points": [
                    "systemctl manages services on systemd-based Linux systems.",
                    "The status command shows whether a service is active and healthy.",
                    "Check status before and after service changes.",
                ],
                "examples": [
                    {"label": "Check Odoo", "code": "systemctl status odoo"},
                    {"label": "Check PostgreSQL", "code": "systemctl status postgresql"},
                ],
            },
            {
                "id": "L-SYSTEMCTL-START-STOP",
                "title": "systemctl start and stop",
                "points": [
                    "start launches a service managed by systemd.",
                    "stop asks systemd to shut the service down.",
                    "Use these commands during planned maintenance windows.",
                ],
                "examples": [
                    {"label": "Start Odoo", "code": "sudo systemctl start odoo"},
                    {"label": "Stop Odoo", "code": "sudo systemctl stop odoo"},
                ],
            },
            {
                "id": "L-SYSTEMCTL-ENABLE",
                "title": "systemctl enable - Start on boot",
                "points": [
                    "enable configures a service to start automatically after reboot.",
                    "disable prevents automatic startup without deleting the service.",
                    "Use status to confirm both enabled state and active state.",
                ],
                "examples": [
                    {"label": "Enable Odoo at boot", "code": "sudo systemctl enable odoo"},
                    {"label": "Check enabled state", "code": "systemctl is-enabled odoo"},
                ],
            },
            {
                "id": "L-JOURNALCTL",
                "title": "journalctl - Read service logs",
                "points": [
                    "journalctl reads logs collected by systemd.",
                    "Use -u to focus on one service.",
                    "Use -f to follow new log entries during testing.",
                ],
                "examples": [
                    {"label": "Read recent Odoo logs", "code": "journalctl -u odoo -n 50"},
                    {"label": "Follow Odoo logs", "code": "journalctl -u odoo -f"},
                ],
            },
            {
                "id": "L-NANO",
                "title": "nano - Beginner-friendly editor",
                "points": [
                    "nano is a simple terminal text editor.",
                    "The most important shortcuts are shown at the bottom of the screen.",
                    "Use nano when you need a quick safe edit and are still learning terminal editors.",
                ],
                "examples": [
                    {"label": "Edit a note", "code": "nano notes.txt"},
                    {"label": "Edit Odoo config", "code": "sudo nano /etc/odoo.conf"},
                ],
            },
            {
                "id": "L-VIM",
                "title": "vim - Modal editor intro",
                "points": [
                    "vim is a powerful editor with separate normal and insert modes.",
                    "Press i to insert text, Esc to return to normal mode, and :wq to save and quit.",
                    "Learn the basics because many servers include vi or vim by default.",
                ],
                "examples": [
                    {"label": "Open a file", "code": "vim notes.txt"},
                    {"label": "Save and quit", "code": ":wq"},
                ],
            },
        ],
    },
    {
        "section": 5,
        "title": "Networking, SSH, shell setup, and scheduling",
        "topics": [
            {
                "id": "L-IP",
                "title": "ip - Inspect network addresses",
                "points": [
                    "The ip command shows network interfaces, addresses, and routes.",
                    "Use it to confirm the server address before testing access.",
                    "Modern Linux systems prefer ip over older ifconfig commands.",
                ],
                "examples": [
                    {"label": "Show addresses", "code": "ip addr"},
                    {"label": "Show default route", "code": "ip route"},
                ],
            },
            {
                "id": "L-PING",
                "title": "ping - Test basic reachability",
                "points": [
                    "ping sends small network packets to test whether a host responds.",
                    "It helps separate network reachability from application problems.",
                    "Some servers block ping, so a failed ping is not always final proof.",
                ],
                "examples": [
                    {"label": "Ping a hostname", "code": "ping -c 4 example.com"},
                    {"label": "Ping a gateway", "code": "ping -c 4 192.168.1.1"},
                ],
            },
            {
                "id": "L-SS",
                "title": "ss - Check listening ports",
                "points": [
                    "ss shows network sockets and listening ports.",
                    "Use it to confirm whether Odoo is listening on its expected port.",
                    "The -tulpn options are common for TCP, UDP, listening, process, and numeric output.",
                ],
                "examples": [
                    {"label": "Show listening services", "code": "sudo ss -tulpn"},
                    {"label": "Check Odoo port", "code": "sudo ss -tulpn | grep 8069"},
                ],
            },
            {
                "id": "L-SSH-KEYS",
                "title": "SSH keys - Safer server login",
                "points": [
                    "SSH keys let you log in without sending a password each time.",
                    "A private key stays on your machine and a public key goes on the server.",
                    "Protect private keys because they prove your identity.",
                ],
                "examples": [
                    {"label": "Create a key", "code": "ssh-keygen -t ed25519 -C \"odoo-admin\""},
                    {"label": "Copy public key", "code": "ssh-copy-id ubuntu@server.example.com"},
                ],
            },
            {
                "id": "L-SSH-HARDEN",
                "title": "SSH hardening basics",
                "points": [
                    "SSH hardening reduces the chance of unauthorized server access.",
                    "Common basics include key-based login, disabling root login, and limiting users.",
                    "Always keep a working session open while testing SSH changes.",
                ],
                "examples": [
                    {"label": "Edit SSH config", "code": "sudo nano /etc/ssh/sshd_config"},
                    {"label": "Test and reload SSH", "code": "sudo sshd -t && sudo systemctl reload ssh"},
                ],
            },
            {
                "id": "L-ENV",
                "title": "Environment variables",
                "points": [
                    "Environment variables are named values available to commands and scripts.",
                    "They often hold settings such as paths, modes, or connection details.",
                    "Use printenv to inspect them without changing anything.",
                ],
                "examples": [
                    {"label": "Show all variables", "code": "printenv"},
                    {"label": "Set one for this shell", "code": "export ODOO_CONF=/etc/odoo.conf"},
                ],
            },
            {
                "id": "L-BASHRC",
                "title": ".bashrc - Shell startup settings",
                "points": [
                    ".bashrc runs when an interactive Bash shell starts.",
                    "Use it for aliases, prompts, and personal environment defaults.",
                    "Avoid putting production service secrets in a personal shell file.",
                ],
                "examples": [
                    {"label": "Edit bashrc", "code": "nano ~/.bashrc"},
                    {"label": "Reload bashrc", "code": "source ~/.bashrc"},
                ],
            },
            {
                "id": "L-CRON",
                "title": "cron - Schedule recurring commands",
                "points": [
                    "cron runs commands on a time schedule.",
                    "Each crontab line includes timing fields and a command.",
                    "Redirect output to a log file so scheduled jobs can be checked later.",
                ],
                "examples": [
                    {"label": "Edit user cron", "code": "crontab -e"},
                    {"label": "Nightly backup example", "code": "0 2 * * * /usr/local/bin/backup-odoo.sh >> /var/log/odoo-backup.log 2>&1"},
                ],
            },
        ],
    },
    {
        "section": 6,
        "title": "Packages, resources, firewall, and Odoo operations",
        "topics": [
            {
                "id": "L-APT-UPDATE",
                "title": "apt update - Refresh package lists",
                "points": [
                    "apt update downloads the latest package index from configured repositories.",
                    "It does not install upgrades by itself.",
                    "Run it before installing packages on Debian or Ubuntu systems.",
                ],
                "examples": [
                    {"label": "Refresh package lists", "code": "sudo apt update"},
                    {"label": "Update then inspect policy", "code": "sudo apt update && apt policy postgresql"},
                ],
            },
            {
                "id": "L-APT-INSTALL-REMOVE",
                "title": "apt install and remove",
                "points": [
                    "apt install adds packages from configured repositories.",
                    "apt remove uninstalls packages while usually leaving config files behind.",
                    "Read the package list before confirming installation or removal.",
                ],
                "examples": [
                    {"label": "Install tree", "code": "sudo apt install tree"},
                    {"label": "Remove a package", "code": "sudo apt remove tree"},
                ],
            },
            {
                "id": "L-DF",
                "title": "df - Check filesystem space",
                "points": [
                    "df shows free and used space on mounted filesystems.",
                    "Use -h for human-readable units.",
                    "Check disk space when Odoo logs, backups, or attachments stop working.",
                ],
                "examples": [
                    {"label": "Show disk space", "code": "df -h"},
                    {"label": "Check root filesystem", "code": "df -h /"},
                ],
            },
            {
                "id": "L-DU",
                "title": "du - Check folder size",
                "points": [
                    "du shows how much space files and folders use.",
                    "Use -s for a summary and -h for readable sizes.",
                    "It helps find which folder is filling a disk.",
                ],
                "examples": [
                    {"label": "Size of Odoo logs", "code": "du -sh /var/log/odoo"},
                    {"label": "Largest items in current folder", "code": "du -h --max-depth=1 | sort -h"},
                ],
            },
            {
                "id": "L-FREE",
                "title": "free - Check memory",
                "points": [
                    "free shows system memory and swap usage.",
                    "Use -h to make the numbers easier to read.",
                    "High memory pressure can slow Odoo or cause workers to restart.",
                ],
                "examples": [
                    {"label": "Show memory", "code": "free -h"},
                    {"label": "Watch memory changes", "code": "watch free -h"},
                ],
            },
            {
                "id": "L-UFW",
                "title": "ufw - Basic firewall management",
                "points": [
                    "ufw is a simpler firewall tool used on many Ubuntu servers.",
                    "Allow only the ports the server actually needs.",
                    "Check status before changing firewall rules over SSH.",
                ],
                "examples": [
                    {"label": "Show firewall status", "code": "sudo ufw status verbose"},
                    {"label": "Allow SSH", "code": "sudo ufw allow OpenSSH"},
                ],
            },
            {
                "id": "L-ODOO-DIRS",
                "title": "Production directories for Odoo",
                "points": [
                    "Common Odoo deployments place application files under /opt/odoo.",
                    "Configuration often lives in /etc and logs usually live under /var/log.",
                    "Know these locations before editing code or troubleshooting services.",
                ],
                "examples": [
                    {"label": "Inspect Odoo application files", "code": "ls -lah /opt/odoo"},
                    {"label": "Check common config path", "code": "ls -l /etc/odoo.conf"},
                ],
            },
            {
                "id": "L-ODOO-LOGS",
                "title": "Odoo logs in production",
                "points": [
                    "Odoo logs record startup messages, errors, warnings, and request details.",
                    "Logs may be written to /var/log/odoo or collected by journalctl.",
                    "Start troubleshooting by reading the newest relevant log lines.",
                ],
                "examples": [
                    {"label": "Follow file logs", "code": "tail -f /var/log/odoo/odoo.log"},
                    {"label": "Read service journal", "code": "journalctl -u odoo -n 100"},
                ],
            },
            {
                "id": "L-SAFE-TROUBLESHOOT",
                "title": "Safe troubleshooting checklist",
                "points": [
                    "Observe the current state before making changes.",
                    "Change one thing at a time and record what changed.",
                    "Verify the result with commands, logs, and user-facing behavior.",
                    "Keep a rollback path for production fixes.",
                ],
                "examples": [
                    {"label": "Capture service state", "code": "systemctl status odoo && journalctl -u odoo -n 50"},
                    {"label": "Backup before editing", "code": "sudo cp /etc/odoo.conf /etc/odoo.conf.before-fix"},
                ],
            },
        ],
    },
]

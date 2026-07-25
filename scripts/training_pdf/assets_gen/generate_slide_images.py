#!/usr/bin/env python3
"""Generate terminal screenshots and teaching diagrams for lecture slides."""

from __future__ import annotations

import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
OUT_TERM = os.path.join(ROOT, "training_materials", "slide_assets", "terminal")
OUT_DIAG = os.path.join(ROOT, "training_materials", "slide_assets", "diagrams")
CONTENT_MOD = os.path.join(ROOT, "scripts", "training_pdf", "content", "slide_images.py")

# Colors
TERM_BG = (30, 30, 30)
TERM_BAR = (55, 55, 55)
TERM_GREEN = (80, 250, 123)
TERM_WHITE = (248, 248, 242)
TERM_GRAY = (180, 180, 180)
TERM_CYAN = (139, 233, 253)
TERM_YELLOW = (241, 250, 140)
WHITE = (255, 255, 255)
INK = (31, 41, 55)
BLUE = (53, 106, 230)
ORANGE = (234, 88, 12)
GREEN = (16, 185, 129)
PURPLE = (124, 58, 237)
LIGHT_BLUE = (191, 219, 254)
LIGHT_GREEN = (187, 247, 208)
LIGHT_PURPLE = (221, 214, 254)


def font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/noto/NotoSansMono-SemiCondensedBold.ttf" if bold else "/usr/share/fonts/truetype/noto/NotoSansMono-SemiCondensed.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-SemiCondensedBold.ttf" if bold else "/usr/share/fonts/truetype/noto/NotoSans-SemiCondensed.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def sans(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/noto/NotoSans-SemiCondensedBold.ttf" if bold else "/usr/share/fonts/truetype/noto/NotoSans-SemiCondensed.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def draw_terminal(path, lines, title="user@odoo-lab:~/project", width=980, height=300):
    """lines: list of (text, color) or plain strings."""
    img = Image.new("RGB", (width, height), TERM_BG)
    d = ImageDraw.Draw(img)
    # title bar
    d.rectangle([0, 0, width, 36], fill=TERM_BAR)
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([12 + i * 18, 11, 24 + i * 18, 23], fill=c)
    d.text((70, 10), title, fill=TERM_GRAY, font=font(14))

    y = 52
    f = font(15)
    for item in lines:
        if isinstance(item, tuple):
            text, color = item
        else:
            text, color = item, TERM_WHITE
        d.text((18, y), text, fill=color, font=f)
        y += 24
        if y > height - 20:
            break
    img.save(path)
    return path


def diagram_permissions(path):
    """Educational chmod string diagram similar to the shared sample."""
    w, h = 1000, 420
    img = Image.new("RGB", (w, h), WHITE)
    d = ImageDraw.Draw(img)
    f_big = font(42, bold=True)
    f = sans(18)
    f_b = sans(18, bold=True)
    f_sm = sans(15)

    # central permission string
    chars = list("-rwxrwxrwx")
    start_x = 160
    y = 210
    spacing = 62
    positions = []
    for i, ch in enumerate(chars):
        x = start_x + i * spacing
        d.text((x, y), ch, fill=INK, font=f_big)
        positions.append((x + 10, y))

    # File type brace (left/top)
    d.line([(positions[0][0] + 8, y - 10), (positions[0][0] + 8, 70)], fill=ORANGE, width=3)
    d.polygon(
        [(positions[0][0] + 8, 70), (positions[0][0] + 2, 82), (positions[0][0] + 14, 82)],
        fill=ORANGE,
    )
    d.text((30, 30), "File Type", fill=ORANGE, font=f_b)
    box = [(20, 55), (150, 145)]
    d.rounded_rectangle(box, radius=10, outline=ORANGE, width=2)
    d.text((32, 68), "d = Directory", fill=INK, font=f_sm)
    d.text((32, 92), "- = Regular File", fill=INK, font=f_sm)
    d.text((32, 116), "l = Symbolic Link", fill=INK, font=f_sm)

    # Meaning brace (right)
    d.rounded_rectangle([(760, 40), (970, 160)], radius=10, outline=BLUE, width=2)
    d.text((780, 52), "r = Readable", fill=INK, font=f_sm)
    d.text((780, 76), "w = Writeable", fill=INK, font=f_sm)
    d.text((780, 100), "x = Executable", fill=INK, font=f_sm)
    d.text((780, 124), "- = Denied", fill=INK, font=f_sm)

    # User / Group / Others brackets
    groups = [
        (1, 3, LIGHT_BLUE, BLUE, "User"),
        (4, 6, LIGHT_GREEN, GREEN, "Group"),
        (7, 9, LIGHT_PURPLE, PURPLE, "Others"),
    ]
    for a, b, fill, stroke, label in groups:
        x1 = positions[a][0] - 8
        x2 = positions[b][0] + 28
        top = y + 70
        d.line([(x1, top), (x1, top + 18), (x2, top + 18), (x2, top)], fill=stroke, width=3)
        cx = (x1 + x2) // 2
        d.line([(cx, top + 18), (cx, top + 48)], fill=stroke, width=3)
        tw = d.textlength(label, font=f_b)
        d.rounded_rectangle([cx - tw / 2 - 12, top + 50, cx + tw / 2 + 12, top + 82], radius=8, fill=fill, outline=stroke, width=2)
        d.text((cx - tw / 2, top + 56), label, fill=stroke, font=f_b)

    d.text((30, 390), "Merit Advisory  ·  Linux permissions visual", fill=(100, 116, 139), font=f_sm)
    img.save(path)
    return path


def diagram_path_tree(path):
    """Simple directory tree for cd/pwd lessons."""
    w, h = 920, 420
    img = Image.new("RGB", (w, h), WHITE)
    d = ImageDraw.Draw(img)
    f = font(16)
    f_b = font(16, bold=True)
    f_title = sans(20, bold=True)
    d.text((24, 18), "Where am I in the filesystem?", fill=BLUE, font=f_title)

    tree = [
        (0, "/home/trainee", False),
        (1, "project/", False),
        (2, "addons/", False),
        (2, "odoo.conf", True),
        (1, "Downloads/", False),
        (0, "/opt/odoo", False),
        (1, "custom_addons/", False),
    ]
    y = 70
    for depth, name, is_file in tree:
        x = 40 + depth * 36
        prefix = "📄 " if is_file else "📁 "
        color = INK if not (depth == 1 and name == "project/") else BLUE
        d.text((x, y), prefix + name, fill=color, font=f_b if depth == 0 else f)
        if depth == 1 and name == "project/":
            d.text((x + 160, y), "← pwd shows this path when you are here", fill=ORANGE, font=sans(14))
        y += 36
    d.rounded_rectangle([(40, 340), (880, 395)], radius=8, fill=(241, 245, 249), outline=BLUE, width=2)
    d.text((56, 356), "Tip: run pwd after every cd until the path feels natural.", fill=INK, font=sans(16))
    img.save(path)
    return path


def main():
    os.makedirs(OUT_TERM, exist_ok=True)
    os.makedirs(OUT_DIAG, exist_ok=True)

    assets = {}

    # pwd
    assets["L-PWD"] = draw_terminal(
        os.path.join(OUT_TERM, "pwd.png"),
        [
            ("trainee@odoo-lab:~$ pwd", TERM_GREEN),
            ("/home/trainee", TERM_WHITE),
            ("trainee@odoo-lab:~$ cd project", TERM_GREEN),
            ("trainee@odoo-lab:~/project$ pwd", TERM_GREEN),
            ("/home/trainee/project", TERM_WHITE),
            ("trainee@odoo-lab:~/project$ echo \"You are in: $(pwd)\"", TERM_GREEN),
            ("You are in: /home/trainee/project", TERM_CYAN),
        ],
    )

    # cd home
    assets["L-CD-HOME"] = draw_terminal(
        os.path.join(OUT_TERM, "cd_home.png"),
        [
            ("trainee@odoo-lab:~/project/addons$ cd", TERM_GREEN),
            ("trainee@odoo-lab:~$ pwd", TERM_GREEN),
            ("/home/trainee", TERM_WHITE),
            ("trainee@odoo-lab:~$ cd ~/Downloads", TERM_GREEN),
            ("trainee@odoo-lab:~/Downloads$ pwd", TERM_GREEN),
            ("/home/trainee/Downloads", TERM_WHITE),
        ],
    )

    # cd ..
    assets["L-CD-PARENT"] = draw_terminal(
        os.path.join(OUT_TERM, "cd_parent.png"),
        [
            ("trainee@odoo-lab:~/project/addons$ pwd", TERM_GREEN),
            ("/home/trainee/project/addons", TERM_WHITE),
            ("trainee@odoo-lab:~/project/addons$ cd ..", TERM_GREEN),
            ("trainee@odoo-lab:~/project$ pwd", TERM_GREEN),
            ("/home/trainee/project", TERM_WHITE),
            ("trainee@odoo-lab:~/project$ cd ../..", TERM_GREEN),
            ("trainee@odoo-lab:~$ pwd", TERM_GREEN),
            ("/home/trainee", TERM_WHITE),
        ],
    )

    # cd absolute
    assets["L-CD-ABSOLUTE"] = draw_terminal(
        os.path.join(OUT_TERM, "cd_absolute.png"),
        [
            ("trainee@odoo-lab:~$ cd /opt/odoo", TERM_GREEN),
            ("trainee@odoo-lab:/opt/odoo$ pwd", TERM_GREEN),
            ("/opt/odoo", TERM_WHITE),
            ("trainee@odoo-lab:/opt/odoo$ cd /var/log", TERM_GREEN),
            ("trainee@odoo-lab:/var/log$ pwd", TERM_GREEN),
            ("/var/log", TERM_WHITE),
        ],
    )

    # cd relative
    assets["L-CD-RELATIVE"] = draw_terminal(
        os.path.join(OUT_TERM, "cd_relative.png"),
        [
            ("trainee@odoo-lab:~/project$ ls", TERM_GREEN),
            ("addons  odoo.conf", TERM_WHITE),
            ("trainee@odoo-lab:~/project$ cd addons", TERM_GREEN),
            ("trainee@odoo-lab:~/project/addons$ cd ../custom_addons", TERM_GREEN),
            ("trainee@odoo-lab:~/project/custom_addons$ pwd", TERM_GREEN),
            ("/home/trainee/project/custom_addons", TERM_WHITE),
        ],
    )

    # ls
    assets["L-LS"] = draw_terminal(
        os.path.join(OUT_TERM, "ls.png"),
        [
            ("trainee@odoo-lab:~/project$ ls", TERM_GREEN),
            ("addons  custom_addons  odoo.conf  README.md", TERM_WHITE),
            ("trainee@odoo-lab:~/project$ ls -lah", TERM_GREEN),
            ("drwxr-xr-x  5 trainee trainee 4.0K Jul 25 09:10 .", TERM_GRAY),
            ("drwxr-x--- 18 trainee trainee 4.0K Jul 25 08:01 ..", TERM_GRAY),
            ("drwxr-xr-x  3 trainee trainee 4.0K Jul 25 09:10 addons", TERM_CYAN),
            ("-rw-r--r--  1 trainee trainee  812 Jul 25 09:08 odoo.conf", TERM_WHITE),
        ],
    )

    # mkdir / touch
    assets["L-MKDIR"] = draw_terminal(
        os.path.join(OUT_TERM, "mkdir.png"),
        [
            ("trainee@odoo-lab:~/project$ mkdir -p custom_addons/wl_student", TERM_GREEN),
            ("trainee@odoo-lab:~/project$ touch custom_addons/wl_student/__init__.py", TERM_GREEN),
            ("trainee@odoo-lab:~/project$ ls custom_addons/wl_student", TERM_GREEN),
            ("__init__.py", TERM_WHITE),
        ],
    )

    # chmod
    perm = os.path.join(OUT_DIAG, "permissions.png")
    diagram_permissions(perm)
    assets["L-CHMOD-NUMERIC"] = perm
    assets["L-CHMOD-SYMBOLIC"] = perm
    assets["L-CHMOD-NUM"] = perm
    assets["L-CHMOD-SYM"] = perm

    # path tree diagram for orientation / pwd
    assets["L-PWD-DIAGRAM"] = diagram_path_tree(os.path.join(OUT_DIAG, "path_tree.png"))

    # cp / mv / rm
    cp_img = draw_terminal(
        os.path.join(OUT_TERM, "cp.png"),
        [
            ("trainee@odoo-lab:~/project$ cp odoo.conf odoo.conf.bak", TERM_GREEN),
            ("trainee@odoo-lab:~/project$ ls odoo.conf*", TERM_GREEN),
            ("odoo.conf  odoo.conf.bak", TERM_WHITE),
            ("trainee@odoo-lab:~/project$ cp -r addons addons_copy", TERM_GREEN),
            ("trainee@odoo-lab:~/project$ ls -d addons*", TERM_GREEN),
            ("addons  addons_copy", TERM_WHITE),
        ],
    )
    assets["L-CP"] = cp_img
    assets["L-CP-FILE"] = cp_img
    assets["L-CP-R"] = cp_img

    mv_img = draw_terminal(
        os.path.join(OUT_TERM, "mv.png"),
        [
            ("trainee@odoo-lab:~/project$ mkdir -p configs", TERM_GREEN),
            ("trainee@odoo-lab:~/project$ mv odoo.conf.bak configs/odoo.conf.bak", TERM_GREEN),
            ("trainee@odoo-lab:~/project$ ls configs", TERM_GREEN),
            ("odoo.conf.bak", TERM_WHITE),
        ],
    )
    assets["L-MV"] = mv_img
    assets["L-MV-RENAME"] = mv_img
    assets["L-MV-MOVE"] = mv_img

    rm_img = draw_terminal(
        os.path.join(OUT_TERM, "rm.png"),
        [
            ("trainee@odoo-lab:~/project$ rm odoo.conf.tmp", TERM_GREEN),
            ("trainee@odoo-lab:~/project$ rm -r addons_copy", TERM_GREEN),
            ("trainee@odoo-lab:~/project$ ls -d addons*", TERM_GREEN),
            ("addons", TERM_WHITE),
        ],
    )
    assets["L-RM-FILE"] = rm_img
    assets["L-RM-R"] = rm_img

    # cat / grep / find / ls variants
    assets["L-CAT"] = draw_terminal(
        os.path.join(OUT_TERM, "cat.png"),
        [
            ("trainee@odoo-lab:~/project$ cat odoo.conf | head -n 5", TERM_GREEN),
            ("[options]", TERM_WHITE),
            ("admin_passwd = strong-password", TERM_WHITE),
            ("db_host = False", TERM_WHITE),
            ("db_port = False", TERM_WHITE),
            ("db_user = odoo", TERM_WHITE),
        ],
    )
    assets["L-LS-L"] = assets["L-LS"]
    assets["L-LS-AH"] = assets["L-LS"]

    assets["L-GREP"] = draw_terminal(
        os.path.join(OUT_TERM, "grep.png"),
        [
            ("trainee@odoo-lab:~/project$ grep -n \"addons_path\" odoo.conf", TERM_GREEN),
            ("12:addons_path = /home/trainee/project/addons,/opt/odoo/addons", TERM_YELLOW),
        ],
    )
    assets["L-FIND"] = draw_terminal(
        os.path.join(OUT_TERM, "find.png"),
        [
            ("trainee@odoo-lab:~/project$ find . -name \"*.py\" | head", TERM_GREEN),
            ("./addons/wl_student/__init__.py", TERM_WHITE),
            ("./addons/wl_student/models/student.py", TERM_WHITE),
        ],
    )
    assets["L-HEAD-TAIL"] = draw_terminal(
        os.path.join(OUT_TERM, "head_tail.png"),
        [
            ("trainee@odoo-lab:~/project$ head -n 3 odoo.conf", TERM_GREEN),
            ("[options]", TERM_WHITE),
            ("admin_passwd = strong-password", TERM_WHITE),
            ("db_host = False", TERM_WHITE),
            ("trainee@odoo-lab:~/project$ tail -n 2 odoo.conf", TERM_GREEN),
            ("logfile = /var/log/odoo/odoo.log", TERM_WHITE),
            ("log_level = info", TERM_WHITE),
        ],
    )
    assets["L-TREE"] = draw_terminal(
        os.path.join(OUT_TERM, "tree.png"),
        [
            ("trainee@odoo-lab:~/project$ tree -L 2", TERM_GREEN),
            (".", TERM_WHITE),
            ("├── addons", TERM_CYAN),
            ("│   └── wl_student", TERM_CYAN),
            ("├── custom_addons", TERM_CYAN),
            ("└── odoo.conf", TERM_WHITE),
        ],
    )

    # systemctl variants
    sys_img = draw_terminal(
        os.path.join(OUT_TERM, "systemctl.png"),
        [
            ("trainee@odoo-lab:~$ sudo systemctl status postgresql", TERM_GREEN),
            ("● postgresql.service - PostgreSQL RDBMS", TERM_WHITE),
            ("     Loaded: loaded (/lib/systemd/system/postgresql.service; enabled)", TERM_GRAY),
            ("     Active: active (exited) since Fri 2026-07-24 08:01:12 UTC", TERM_CYAN),
            ("trainee@odoo-lab:~$ sudo systemctl start postgresql", TERM_GREEN),
            ("trainee@odoo-lab:~$ sudo systemctl enable postgresql", TERM_GREEN),
        ],
    )
    assets["L-SYSTEMCTL"] = sys_img
    assets["L-SYSTEMCTL-STATUS"] = sys_img
    assets["L-SYSTEMCTL-START-STOP"] = sys_img
    assets["L-SYSTEMCTL-ENABLE"] = sys_img

    # permissions owners
    assets["L-CHOWN"] = draw_terminal(
        os.path.join(OUT_TERM, "chown.png"),
        [
            ("trainee@odoo-lab:/opt$ sudo chown -R odoo:odoo /opt/odoo", TERM_GREEN),
            ("trainee@odoo-lab:/opt$ ls -ld /opt/odoo", TERM_GREEN),
            ("drwxr-xr-x 8 odoo odoo 4096 Jul 24 09:00 /opt/odoo", TERM_WHITE),
        ],
    )
    assets["L-CHGRP"] = assets["L-CHOWN"]
    assets["L-SUDO"] = draw_terminal(
        os.path.join(OUT_TERM, "sudo.png"),
        [
            ("trainee@odoo-lab:~$ whoami", TERM_GREEN),
            ("trainee", TERM_WHITE),
            ("trainee@odoo-lab:~$ sudo whoami", TERM_GREEN),
            ("root", TERM_YELLOW),
        ],
    )
    assets["L-WHOAMI-ID"] = assets["L-SUDO"]

    # More Linux result screenshots for beginner clarity
    assets["L-SSH-KEYS"] = draw_terminal(
        os.path.join(OUT_TERM, "ssh_keys.png"),
        [
            ("trainee@odoo-lab:~$ ssh-keygen -t ed25519 -C \"odoo-admin\"", TERM_GREEN),
            ("Generating public/private ed25519 key pair.", TERM_WHITE),
            ("Your identification has been saved in /home/trainee/.ssh/id_ed25519", TERM_CYAN),
            ("trainee@odoo-lab:~$ ssh-copy-id ubuntu@server.example.com", TERM_GREEN),
            ("Number of key(s) added: 1", TERM_WHITE),
        ],
    )
    assets["L-DF"] = draw_terminal(
        os.path.join(OUT_TERM, "df.png"),
        [
            ("trainee@odoo-lab:~$ df -h", TERM_GREEN),
            ("Filesystem      Size  Used Avail Use% Mounted on", TERM_GRAY),
            ("/dev/sda1        98G   42G   52G  45% /", TERM_WHITE),
            ("trainee@odoo-lab:~$ du -sh /opt/odoo", TERM_GREEN),
            ("3.8G    /opt/odoo", TERM_CYAN),
        ],
    )
    assets["L-DU"] = assets["L-DF"]
    assets["L-APT-UPDATE"] = draw_terminal(
        os.path.join(OUT_TERM, "apt.png"),
        [
            ("trainee@odoo-lab:~$ sudo apt update", TERM_GREEN),
            ("Hit:1 http://archive.ubuntu.com/ubuntu jammy InRelease", TERM_GRAY),
            ("Reading package lists... Done", TERM_WHITE),
            ("trainee@odoo-lab:~$ sudo apt install -y htop", TERM_GREEN),
            ("Setting up htop (3.0.5-7build2) ...", TERM_CYAN),
        ],
    )
    assets["L-APT-INSTALL-REMOVE"] = assets["L-APT-UPDATE"]
    assets["L-PING"] = draw_terminal(
        os.path.join(OUT_TERM, "ping.png"),
        [
            ("trainee@odoo-lab:~$ ping -c 2 8.8.8.8", TERM_GREEN),
            ("64 bytes from 8.8.8.8: icmp_seq=1 ttl=117 time=12.4 ms", TERM_WHITE),
            ("64 bytes from 8.8.8.8: icmp_seq=2 ttl=117 time=11.9 ms", TERM_WHITE),
            ("--- 8.8.8.8 ping statistics ---", TERM_GRAY),
            ("2 packets transmitted, 2 received, 0% packet loss", TERM_CYAN),
        ],
    )
    assets["L-CRON"] = draw_terminal(
        os.path.join(OUT_TERM, "cron.png"),
        [
            ("trainee@odoo-lab:~$ crontab -l", TERM_GREEN),
            ("0 2 * * * /opt/odoo/scripts/backup.sh", TERM_WHITE),
            ("trainee@odoo-lab:~$ crontab -e", TERM_GREEN),
            ("# edit schedule, save, then verify with crontab -l", TERM_GRAY),
        ],
    )
    assets["L-ODOO-LOGS"] = draw_terminal(
        os.path.join(OUT_TERM, "odoo_logs.png"),
        [
            ("trainee@odoo-lab:~$ sudo tail -n 20 /var/log/odoo/odoo.log", TERM_GREEN),
            ("INFO mydb odoo.modules.loading: Modules loaded.", TERM_WHITE),
            ("INFO mydb odoo.service.server: HTTP service (werkzeug) running", TERM_CYAN),
        ],
    )

    # Python terminal results
    assets["P-INTERPRETER"] = draw_terminal(
        os.path.join(OUT_TERM, "py_interpreter.png"),
        [
            ("trainee@odoo-lab:~$ python3 --version", TERM_GREEN),
            ("Python 3.10.12", TERM_WHITE),
            ("trainee@odoo-lab:~$ which python3", TERM_GREEN),
            ("/usr/bin/python3", TERM_CYAN),
        ],
        title="python3",
    )
    assets["P-FIRST"] = draw_terminal(
        os.path.join(OUT_TERM, "py_first.png"),
        [
            ("trainee@odoo-lab:~$ cat hello.py", TERM_GREEN),
            ("print('Hello, Merit Advisory')", TERM_WHITE),
            ("trainee@odoo-lab:~$ python3 hello.py", TERM_GREEN),
            ("Hello, Merit Advisory", TERM_CYAN),
        ],
        title="python3 hello.py",
    )
    assets["P-VARS"] = draw_terminal(
        os.path.join(OUT_TERM, "py_vars.png"),
        [
            (">>> customer_name = 'Agrolait'", TERM_GREEN),
            (">>> invoice_count = 3", TERM_GREEN),
            (">>> invoice_count = invoice_count + 1", TERM_GREEN),
            (">>> print(customer_name, invoice_count)", TERM_GREEN),
            ("Agrolait 4", TERM_CYAN),
        ],
        title="python3",
    )
    assets["P-LIST"] = draw_terminal(
        os.path.join(OUT_TERM, "py_list.png"),
        [
            (">>> partners = ['Agrolait', 'Azure Interior']", TERM_GREEN),
            (">>> partners.append('Deco Addict')", TERM_GREEN),
            (">>> print(partners[0], len(partners))", TERM_GREEN),
            ("Agrolait 3", TERM_CYAN),
        ],
        title="python3",
    )
    assets["P-DICT"] = draw_terminal(
        os.path.join(OUT_TERM, "py_dict.png"),
        [
            (">>> person = {'name': 'Ada', 'role': 'Admin'}", TERM_GREEN),
            (">>> print(person['name'])", TERM_GREEN),
            ("Ada", TERM_CYAN),
            (">>> print(person.get('email', 'missing'))", TERM_GREEN),
            ("missing", TERM_WHITE),
        ],
        title="python3",
    )
    assets["P-IF"] = draw_terminal(
        os.path.join(OUT_TERM, "py_if.png"),
        [
            (">>> score = 85", TERM_GREEN),
            (">>> if score >= 50:", TERM_GREEN),
            ("...     print('Pass')", TERM_GREEN),
            ("Pass", TERM_CYAN),
        ],
        title="python3",
    )
    assets["P-FOR"] = draw_terminal(
        os.path.join(OUT_TERM, "py_for.png"),
        [
            (">>> for n in [1, 2, 3]:", TERM_GREEN),
            ("...     print(n)", TERM_GREEN),
            ("1", TERM_CYAN),
            ("2", TERM_CYAN),
            ("3", TERM_CYAN),
        ],
        title="python3",
    )
    assets["P-FUNC"] = draw_terminal(
        os.path.join(OUT_TERM, "py_func.png"),
        [
            (">>> def greet(name):", TERM_GREEN),
            ("...     return f'Hello, {name}'", TERM_GREEN),
            (">>> print(greet('Ada'))", TERM_GREEN),
            ("Hello, Ada", TERM_CYAN),
        ],
        title="python3",
    )
    assets["P-EXCEPT"] = draw_terminal(
        os.path.join(OUT_TERM, "py_except.png"),
        [
            (">>> try:", TERM_GREEN),
            ("...     int('abc')", TERM_GREEN),
            ("... except ValueError:", TERM_GREEN),
            ("...     print('Bad number')", TERM_GREEN),
            ("Bad number", TERM_YELLOW),
        ],
        title="python3",
    )
    assets["P-CLASS"] = draw_terminal(
        os.path.join(OUT_TERM, "py_class.png"),
        [
            (">>> class User:", TERM_GREEN),
            ("...     def __init__(self, name):", TERM_GREEN),
            ("...         self.name = name", TERM_GREEN),
            (">>> print(User('Ada').name)", TERM_GREEN),
            ("Ada", TERM_CYAN),
        ],
        title="python3",
    )
    assets["P-VENV"] = draw_terminal(
        os.path.join(OUT_TERM, "py_venv.png"),
        [
            ("trainee@odoo-lab:~/project$ python3 -m venv .venv", TERM_GREEN),
            ("trainee@odoo-lab:~/project$ source .venv/bin/activate", TERM_GREEN),
            ("(.venv) trainee@odoo-lab:~/project$ pip install requests", TERM_GREEN),
            ("Successfully installed requests-2.32.3", TERM_CYAN),
        ],
    )

    # PostgreSQL / Odoo shell visuals for early lessons
    assets["DB-01"] = draw_terminal(
        os.path.join(OUT_TERM, "pg_install.png"),
        [
            ("trainee@odoo-lab:~$ sudo apt install -y postgresql postgresql-contrib", TERM_GREEN),
            ("Setting up postgresql (16.x) ...", TERM_WHITE),
            ("trainee@odoo-lab:~$ psql --version", TERM_GREEN),
            ("psql (PostgreSQL) 16.3", TERM_CYAN),
        ],
    )
    assets["DB-02"] = draw_terminal(
        os.path.join(OUT_TERM, "pg_service.png"),
        [
            ("trainee@odoo-lab:~$ sudo systemctl enable --now postgresql", TERM_GREEN),
            ("trainee@odoo-lab:~$ systemctl is-active postgresql", TERM_GREEN),
            ("active", TERM_CYAN),
        ],
    )
    assets["DB-SELECT"] = draw_terminal(
        os.path.join(OUT_TERM, "pg_select.png"),
        [
            ("training=# SELECT id, name FROM partners;", TERM_GREEN),
            (" id | name", TERM_GRAY),
            ("----+------", TERM_GRAY),
            ("  1 | Ada", TERM_WHITE),
            ("(1 row)", TERM_CYAN),
        ],
        title="psql -d training",
    )
    assets["ODOO-SHELL"] = draw_terminal(
        os.path.join(OUT_TERM, "odoo_shell.png"),
        [
            ("trainee@odoo-lab:/opt/odoo$ ./odoo-bin shell -d mydb", TERM_GREEN),
            (">>> env['res.partner'].search_count([])", TERM_GREEN),
            ("42", TERM_CYAN),
        ],
    )

    # write manifest for generator
    mod_path = CONTENT_MOD
    lines = ["# Auto-generated image map for lecture slides\n", "IMAGES = {\n"]
    for k, v in assets.items():
        rel = os.path.relpath(v, ROOT).replace("\\", "/")
        lines.append(f'    "{k}": "{rel}",\n')
    aliases = {
        "L-LS-LONG": "L-LS",
        "L-TOUCH": "L-MKDIR",
        "L-RM": "L-RM-FILE",
        "L-CHMOD": "L-CHMOD-NUMERIC",
        "L-LESS-MORE": "L-CAT",
        "L-USERS-GROUPS": "L-SUDO",
        "L-PS": "L-SYSTEMCTL-STATUS",
        "L-TOP-HTOP": "L-SYSTEMCTL-STATUS",
        "L-KILL": "L-SYSTEMCTL-STATUS",
        "L-PKILL": "L-SYSTEMCTL-STATUS",
        "L-JOURNALCTL": "L-SYSTEMCTL-STATUS",
        "L-SSH-HARDEN": "L-SSH-KEYS",
        "L-FREE": "L-DF",
        "L-ODOO-DIRS": "L-ODOO-LOGS",
        # Python topic ids -> visual keys
        "P-RUN-PYTHON3": "P-INTERPRETER",
        "P-FIRST-PROGRAM": "P-FIRST",
        "P-PY2-PY3": "P-INTERPRETER",
        "P-VARIABLES": "P-VARS",
        "P-NUMBERS": "P-VARS",
        "P-STRINGS": "P-VARS",
        "P-CONCAT": "P-VARS",
        "P-FSTRINGS": "P-VARS",
        "P-LISTS": "P-LIST",
        "P-LIST-SLICE": "P-LIST",
        "P-LIST-APPEND": "P-LIST",
        "P-LIST-POP": "P-LIST",
        "P-DICTS": "P-DICT",
        "P-DICT-GET": "P-DICT",
        "P-DICT-KEYS": "P-DICT",
        "P-IF-ELIF-ELSE": "P-IF",
        "P-TRUTHY-FALSEY": "P-IF",
        "P-FOR": "P-FOR",
        "P-RANGE": "P-FOR",
        "P-ENUMERATE": "P-FOR",
        "P-WHILE": "P-FOR",
        "P-FUNCTIONS": "P-FUNC",
        "P-PARAMETERS": "P-FUNC",
        "P-DEFAULTS": "P-FUNC",
        "P-RETURN": "P-FUNC",
        "P-ARGS": "P-FUNC",
        "P-KWARGS": "P-FUNC",
        "P-TRY-EXCEPT": "P-EXCEPT",
        "P-READING-ERRORS": "P-EXCEPT",
        "P-CLASSES-INIT": "P-CLASS",
        "P-METHODS": "P-CLASS",
        "P-INHERITANCE": "P-CLASS",
        "P-SUPER": "P-CLASS",
        "P-VENV": "P-VENV",
        "P-PIP": "P-VENV",
        # Postgres / Odoo aliases (partial coverage)
        "DB-03": "DB-SELECT",
        "DB-04": "DB-SELECT",
        "DB-05": "DB-SELECT",
        "DB-06": "DB-SELECT",
        "DB-07": "DB-SELECT",
        "DB-08": "DB-SELECT",
        "ODOO-01": "ODOO-SHELL",
        "ODOO-02": "ODOO-SHELL",
        "ODOO-03": "ODOO-SHELL",
    }
    lines.append("}\n\n")
    lines.append("ALIASES = {\n")
    for a, b in aliases.items():
        lines.append(f'    "{a}": "{b}",\n')
    lines.append("}\n\n")
    lines.append(
        "def image_for(topic_id):\n"
        "    key = ALIASES.get(topic_id, topic_id)\n"
        "    return IMAGES.get(key) or IMAGES.get(topic_id)\n"
    )
    with open(mod_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"Wrote {len(assets)} assets")
    for k, v in sorted(assets.items()):
        print(" ", k, "->", os.path.relpath(v, ROOT))


if __name__ == "__main__":
    main()

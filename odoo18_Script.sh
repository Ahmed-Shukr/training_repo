#!/bin/bash
set -e

### VARIABLES
OE_USER="odoo"
OE_HOME="/opt/$OE_USER"
OE_HOME_EXT="$OE_HOME/odoo-server"
OE_VERSION="18.0"
OE_PORT="8069"
OE_CONFIG="odoo18"
OE_SUPERADMIN="admin"
GENERATE_RANDOM_PASSWORD="True"

INSTALL_NGINX="False"
INSTALL_WKHTMLTOPDF="True"

### SYSTEM UPDATE
echo "---- Updating system ----"
sudo apt update && sudo apt upgrade -y

### INSTALL DEPENDENCIES
echo "---- Installing dependencies ----"
sudo apt install -y \
  python3 python3-venv python3-dev python3-pip \
  build-essential git wget curl \
  libxslt1-dev libzip-dev libldap2-dev libsasl2-dev \
  libjpeg-dev libpq-dev libpng-dev \
  nodejs npm gdebi

### POSTGRESQL 16
echo "---- Installing PostgreSQL 16 ----"
sudo curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc \
  | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg

echo "deb http://apt.postgresql.org/pub/repos/apt jammy-pgdg main" \
  | sudo tee /etc/apt/sources.list.d/pgdg.list

sudo apt update
sudo apt install -y postgresql-16 postgresql-client-16

sudo su - postgres -c "createuser -s $OE_USER" || true

### NODEJS 18
echo "---- Installing NodeJS 18 ----"
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
sudo npm install -g rtlcss

### WKHTMLTOPDF
if [ "$INSTALL_WKHTMLTOPDF" = "True" ]; then
  echo "---- Installing wkhtmltopdf ----"
  sudo apt install -y wkhtmltopdf
fi

### CREATE ODOO USER
echo "---- Creating Odoo system user ----"
sudo adduser --system --home=$OE_HOME --group $OE_USER

### CLONE ODOO 18
echo "---- Cloning Odoo 18 ----"
sudo git clone --depth 1 --branch $OE_VERSION https://github.com/odoo/odoo $OE_HOME_EXT
sudo chown -R $OE_USER:$OE_USER $OE_HOME

### PYTHON VIRTUAL ENV
echo "---- Creating Python virtual environment ----"
sudo -u $OE_USER python3 -m venv $OE_HOME/venv
sudo -u $OE_USER $OE_HOME/venv/bin/pip install --upgrade pip wheel
sudo -u $OE_USER $OE_HOME/venv/bin/pip install -r $OE_HOME_EXT/requirements.txt

### CONFIG FILE
echo "---- Creating config file ----"
sudo mkdir -p /etc/odoo
sudo touch /etc/odoo/$OE_CONFIG.conf

if [ "$GENERATE_RANDOM_PASSWORD" = "True" ]; then
  OE_SUPERADMIN=$(openssl rand -hex 16)
fi

sudo tee /etc/odoo/$OE_CONFIG.conf > /dev/null <<EOF
[options]
admin_passwd = $OE_SUPERADMIN
http_port = $OE_PORT
addons_path = $OE_HOME_EXT/addons
logfile = /var/log/odoo/$OE_CONFIG.log
EOF

sudo chown $OE_USER:$OE_USER /etc/odoo/$OE_CONFIG.conf
sudo chmod 640 /etc/odoo/$OE_CONFIG.conf

### LOG DIR
sudo mkdir -p /var/log/odoo
sudo chown $OE_USER:$OE_USER /var/log/odoo

### SYSTEMD SERVICE
echo "---- Creating systemd service ----"
sudo tee /etc/systemd/system/$OE_CONFIG.service > /dev/null <<EOF
[Unit]
Description=Odoo 18
After=network.target postgresql.service

[Service]
Type=simple
User=$OE_USER
ExecStart=$OE_HOME/venv/bin/python3 $OE_HOME_EXT/odoo-bin -c /etc/odoo/$OE_CONFIG.conf
StandardOutput=journal+console

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable $OE_CONFIG
sudo systemctl start $OE_CONFIG

### DONE
echo "--------------------------------------------------"
echo "Odoo 18 installed successfully"
echo "Port: $OE_PORT"
echo "Config: /etc/odoo/$OE_CONFIG.conf"
echo "Log: /var/log/odoo/"
echo "Admin password: $OE_SUPERADMIN"
echo "Start: sudo systemctl start $OE_CONFIG"
echo "Stop: sudo systemctl stop $OE_CONFIG"
echo "Status: sudo systemctl status $OE_CONFIG"
echo "--------------------------------------------------"

#!/bin/bash

# Butler Platform - Deployment Script für Production
# Dieses Skript deployed die Anwendung auf einem frischen Ubuntu/Debian Server

set -e  # Exit bei Fehler

echo "🚀 Butler Platform - Production Deployment"
echo "==========================================="
echo ""

# Farben für Output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Variablen
APP_NAME="butler-platform"
APP_USER="butler"
APP_DIR="/home/${APP_USER}/${APP_NAME}"
VENV_DIR="${APP_DIR}/venv"

# Funktionen
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}➜ $1${NC}"
}

# 1. System-Update
print_info "Aktualisiere System-Pakete..."
sudo apt update
sudo apt upgrade -y
print_success "System aktualisiert"

# 2. Benötigte Pakete installieren
print_info "Installiere benötigte Pakete..."
sudo apt install -y \
    python3.12 \
    python3.12-venv \
    python3-pip \
    postgresql \
    postgresql-contrib \
    nginx \
    git \
    certbot \
    python3-certbot-nginx \
    supervisor
print_success "Pakete installiert"

# 3. Butler-User erstellen
if id "${APP_USER}" &>/dev/null; then
    print_info "User ${APP_USER} existiert bereits"
else
    print_info "Erstelle User ${APP_USER}..."
    sudo useradd -m -s /bin/bash ${APP_USER}
    sudo usermod -aG www-data ${APP_USER}
    print_success "User ${APP_USER} erstellt"
fi

# 4. PostgreSQL Datenbank einrichten
print_info "Richte PostgreSQL-Datenbank ein..."
sudo -u postgres psql <<EOF
CREATE DATABASE butler_platform_prod;
CREATE USER butler_user WITH PASSWORD 'CHANGE_THIS_PASSWORD';
ALTER ROLE butler_user SET client_encoding TO 'utf8';
ALTER ROLE butler_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE butler_user SET timezone TO 'Europe/Berlin';
GRANT ALL PRIVILEGES ON DATABASE butler_platform_prod TO butler_user;
\q
EOF
print_success "Datenbank eingerichtet"

# 5. Repository klonen (falls noch nicht vorhanden)
if [ -d "${APP_DIR}" ]; then
    print_info "Repository existiert bereits, aktualisiere..."
    cd ${APP_DIR}
    sudo -u ${APP_USER} git pull
else
    print_info "Klone Repository..."
    sudo -u ${APP_USER} git clone https://github.com/neubuot/butler-platform.git ${APP_DIR}
fi
print_success "Repository bereit"

# 6. Virtual Environment einrichten
print_info "Richte Virtual Environment ein..."
cd ${APP_DIR}
sudo -u ${APP_USER} python3.12 -m venv ${VENV_DIR}
sudo -u ${APP_USER} ${VENV_DIR}/bin/pip install --upgrade pip
sudo -u ${APP_USER} ${VENV_DIR}/bin/pip install -r requirements.txt
print_success "Virtual Environment eingerichtet"

# 7. Logs-Verzeichnis erstellen
print_info "Erstelle Logs-Verzeichnis..."
sudo -u ${APP_USER} mkdir -p ${APP_DIR}/logs
print_success "Logs-Verzeichnis erstellt"

# 8. .env Datei einrichten (interaktiv)
if [ ! -f "${APP_DIR}/.env" ]; then
    print_info "Erstelle .env Datei..."
    sudo -u ${APP_USER} cp ${APP_DIR}/.env.production.example ${APP_DIR}/.env
    print_error "WICHTIG: Bearbeite jetzt die .env Datei:"
    echo "  sudo nano ${APP_DIR}/.env"
    echo ""
    read -p "Drücke Enter wenn du die .env Datei bearbeitet hast..."
else
    print_info ".env Datei existiert bereits"
fi

# 9. Django-Setup
print_info "Führe Django-Migrationen aus..."
cd ${APP_DIR}
sudo -u ${APP_USER} ${VENV_DIR}/bin/python manage.py migrate
sudo -u ${APP_USER} ${VENV_DIR}/bin/python manage.py collectstatic --noinput
print_success "Django-Setup abgeschlossen"

# 10. Superuser erstellen (optional)
read -p "Möchtest du einen Django-Superuser erstellen? (j/n): " create_super
if [ "$create_super" = "j" ] || [ "$create_super" = "J" ]; then
    sudo -u ${APP_USER} ${VENV_DIR}/bin/python manage.py createsuperuser
fi

# 11. Systemd Services einrichten
print_info "Richte systemd Services ein..."
sudo cp ${APP_DIR}/deployment/butler-platform.socket /etc/systemd/system/
sudo cp ${APP_DIR}/deployment/butler-platform.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable butler-platform.socket
sudo systemctl start butler-platform.socket
sudo systemctl enable butler-platform.service
sudo systemctl start butler-platform.service
print_success "Systemd Services gestartet"

# 12. Nginx einrichten
print_info "Richte Nginx ein..."
sudo cp ${APP_DIR}/deployment/nginx-butler-platform.conf /etc/nginx/sites-available/butler-platform
sudo ln -sf /etc/nginx/sites-available/butler-platform /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
print_success "Nginx konfiguriert"

# 13. SSL Zertifikat (Let's Encrypt)
read -p "Möchtest du jetzt ein SSL-Zertifikat mit Let's Encrypt erstellen? (j/n): " setup_ssl
if [ "$setup_ssl" = "j" ] || [ "$setup_ssl" = "J" ]; then
    read -p "Deine Domain (z.B. butler.example.com): " domain
    sudo certbot --nginx -d ${domain}
    print_success "SSL-Zertifikat erstellt"
fi

# 14. Firewall einrichten
print_info "Richte Firewall ein..."
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable
print_success "Firewall konfiguriert"

echo ""
echo "==========================================="
print_success "Deployment abgeschlossen!"
echo ""
echo "Nächste Schritte:"
echo "1. Überprüfe die .env Datei: sudo nano ${APP_DIR}/.env"
echo "2. Teste die Anwendung: https://deine-domain.de"
echo "3. Logs überprüfen:"
echo "   - Gunicorn: tail -f ${APP_DIR}/logs/gunicorn-error.log"
echo "   - Nginx: sudo tail -f /var/log/nginx/butler-platform-error.log"
echo "   - Django: tail -f ${APP_DIR}/logs/django.log"
echo ""
echo "Services verwalten:"
echo "   - Status: sudo systemctl status butler-platform"
echo "   - Neustart: sudo systemctl restart butler-platform"
echo "   - Logs: sudo journalctl -u butler-platform -f"
echo ""

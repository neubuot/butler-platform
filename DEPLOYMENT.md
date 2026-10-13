# 🚀 Production Deployment - Butler Platform

Komplette Anleitung zum Deployment der Butler Platform auf einem Hetzner Cloud Server (oder anderen Ubuntu/Debian VPS).

---

## 📋 Voraussetzungen

### Server-Anforderungen (Minimum)
- **CPU**: 2 vCPUs
- **RAM**: 4 GB
- **Disk**: 40 GB SSD
- **OS**: Ubuntu 22.04 LTS oder 24.04 LTS
- **Domain**: Eine registrierte Domain (z.B. butler.deine-firma.de)

### Empfohlener Hetzner Server
**Hetzner Cloud CX21** (~5-6 €/Monat)
- 2 vCPU (AMD)
- 4 GB RAM
- 40 GB SSD
- 20 TB Traffic
- Rechenzentrum: Falkenstein oder Nürnberg (Deutschland)

---

## 🛠 Teil 1: Server bei Hetzner erstellen

### Schritt 1: Hetzner Cloud Account
1. Gehe zu https://www.hetzner.com/cloud
2. Erstelle einen Account (falls noch nicht vorhanden)
3. Verifiziere deine E-Mail und Zahlungsmethode

### Schritt 2: Projekt erstellen
1. Klicke auf "New Project"
2. Name: "Butler Platform"
3. Projekt öffnen

### Schritt 3: Server erstellen
1. Klicke auf "Add Server"
2. **Location**: Falkenstein (Deutschland) oder Nürnberg
3. **Image**: Ubuntu 24.04
4. **Type**: CX21 (Shared vCPU, 2 vCPUs, 4GB RAM)
5. **Networking**: 
   - ✅ Public IPv4 & IPv6
   - Optional: Private Network (später)
6. **SSH Key**: 
   - Erstelle einen neuen SSH-Key oder
   - Nutze Passwort-Login (weniger sicher, später ändern!)
7. **Name**: butler-platform-prod
8. **Create & Buy now**

### Schritt 4: Server-IP notieren
Nach ~60 Sekunden ist der Server bereit:
- Notiere die **IPv4-Adresse** (z.B. 88.198.123.45)
- Diese brauchst du für SSH-Zugriff und DNS

---

## 🌐 Teil 2: Domain einrichten

### DNS-Einträge bei deinem Domain-Provider

Erstelle folgende A-Records:

```
Typ    Name              Wert (IP-Adresse)    TTL
A      butler            88.198.123.45        3600
A      www.butler        88.198.123.45        3600
```

Beispiel für verschiedene Provider:
- **Hetzner DNS**: https://dns.hetzner.com
- **Cloudflare**: Dashboard → DNS → Records
- **Strato/1&1/etc**: DNS-Verwaltung im Kundenportal

⏱ **Wartezeit**: DNS-Änderungen brauchen 10 Min - 24 Std

---

## 🔐 Teil 3: SSH-Verbindung herstellen

### Von Windows (PowerShell oder CMD):
```powershell
ssh root@88.198.123.45
```

### Von Mac/Linux:
```bash
ssh root@88.198.123.45
```

Beim ersten Mal:
```
The authenticity of host '88.198.123.45' can't be established.
Are you sure you want to continue connecting (yes/no)? yes
```

Du bist jetzt als **root** auf dem Server eingeloggt!

---

## ⚡ Teil 4: Automatisches Deployment

### Option A: Automatisches Setup-Skript (Empfohlen)

```bash
# 1. Repository klonen
cd /opt
git clone https://github.com/neubuot/butler-platform.git
cd butler-platform

# 2. Deployment-Skript ausführen
chmod +x deployment/deploy.sh
./deployment/deploy.sh
```

Das Skript führt automatisch aus:
- ✅ System-Update
- ✅ Installation aller Pakete (Python, PostgreSQL, Nginx, etc.)
- ✅ Butler-User erstellen
- ✅ PostgreSQL-Datenbank einrichten
- ✅ Virtual Environment erstellen
- ✅ Django-Migrationen
- ✅ Gunicorn Service einrichten
- ✅ Nginx konfigurieren
- ✅ SSL-Zertifikat (Let's Encrypt)
- ✅ Firewall einrichten

**Während des Skripts:**
1. Bearbeite die `.env` Datei wenn aufgefordert
2. Erstelle optional einen Django-Superuser
3. Gib deine Domain ein für SSL-Zertifikat

---

### Option B: Manuelles Setup (Schritt für Schritt)

Falls du jeden Schritt selbst kontrollieren möchtest, siehe: **DEPLOYMENT_MANUAL.md**

---

## 🔧 Teil 5: Konfiguration

### .env Datei anpassen

```bash
nano /home/butler/butler-platform/.env
```

**Wichtige Einstellungen:**

```bash
# UNBEDINGT ÄNDERN!
SECRET_KEY=GENERIERE-EINEN-LANGEN-ZUFÄLLIGEN-STRING
ALLOWED_HOSTS=deine-domain.de,www.deine-domain.de,88.198.123.45

# Datenbank-Passwort (wurde beim Setup generiert)
DB_PASSWORD=DAS-PASSWORT-AUS-DEM-SETUP

# E-Mail (für Benachrichtigungen)
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=deine-email@gmail.com
EMAIL_HOST_PASSWORD=app-spezifisches-passwort
```

**SECRET_KEY generieren:**
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Speichern: `CTRL + X`, dann `Y`, dann `Enter`

### Django-Migrationen & Static Files

```bash
cd /home/butler/butler-platform
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
```

### Superuser erstellen

```bash
python manage.py createsuperuser
```

---

## 🎯 Teil 6: Services starten

### Gunicorn Service

```bash
# Service aktivieren und starten
sudo systemctl enable butler-platform.socket
sudo systemctl start butler-platform.socket
sudo systemctl enable butler-platform
sudo systemctl start butler-platform

# Status überprüfen
sudo systemctl status butler-platform
```

**Erwartete Ausgabe:**
```
● butler-platform.service - Butler Platform Gunicorn daemon
   Loaded: loaded
   Active: active (running)
```

### Nginx

```bash
# Nginx neu starten
sudo systemctl restart nginx

# Status überprüfen
sudo systemctl status nginx
```

---

## 🔒 Teil 7: SSL-Zertifikat (HTTPS)

### Let's Encrypt mit Certbot

```bash
# SSL-Zertifikat für deine Domain
sudo certbot --nginx -d butler.deine-firma.de -d www.butler.deine-firma.de
```

Fragen beantworten:
1. **E-Mail**: Deine E-Mail für wichtige Benachrichtigungen
2. **Terms of Service**: `Y` (Ja)
3. **Newsletter**: `N` (optional)
4. **Redirect HTTP to HTTPS**: `2` (Ja, empfohlen)

**Auto-Renewal testen:**
```bash
sudo certbot renew --dry-run
```

Certbot richtet automatisch einen Cronjob ein, der das Zertifikat alle 60 Tage erneuert.

---

## ✅ Teil 8: Testen & Verifizieren

### 1. Website aufrufen
```
https://butler.deine-firma.de
```

Du solltest eine Weiterleitung zum Admin-Login sehen (da noch keine Frontend-Views existieren).

### 2. Admin-Panel
```
https://butler.deine-firma.de/admin
```

Logge dich mit deinem Superuser ein.

### 3. SSL überprüfen
- Grünes Schloss-Symbol im Browser
- Zertifikat gültig
- Redirect von HTTP → HTTPS funktioniert

### 4. Logs überprüfen

**Gunicorn Logs:**
```bash
tail -f /home/butler/butler-platform/logs/gunicorn-error.log
```

**Nginx Logs:**
```bash
sudo tail -f /var/log/nginx/butler-platform-error.log
```

**Django Logs:**
```bash
tail -f /home/butler/butler-platform/logs/django.log
```

**Systemd Journal:**
```bash
sudo journalctl -u butler-platform -f
```

---

## 🔄 Teil 9: Updates deployen

### Code-Updates von GitHub

```bash
# Als Butler-User
sudo su - butler
cd /home/butler/butler-platform

# Neuesten Code pullen
git pull origin main

# Virtual Environment aktivieren
source venv/bin/activate

# Dependencies aktualisieren (falls nötig)
pip install -r requirements.txt

# Migrationen ausführen
python manage.py migrate

# Static files sammeln
python manage.py collectstatic --noinput

# Gunicorn neu starten
sudo systemctl restart butler-platform

# Nginx neu laden
sudo systemctl reload nginx
```

### Schnell-Update Skript

Erstelle: `/home/butler/update.sh`
```bash
#!/bin/bash
cd /home/butler/butler-platform
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart butler-platform
echo "✓ Update abgeschlossen!"
```

Ausführen:
```bash
chmod +x /home/butler/update.sh
./update.sh
```

---

## 🛡 Teil 10: Sicherheit

### Firewall (UFW)

```bash
# Status überprüfen
sudo ufw status

# Sollte sein:
# 22/tcp (SSH)
# 80/tcp (HTTP)
# 443/tcp (HTTPS)
```

### Fail2Ban (Schutz vor Brute-Force)

```bash
# Installieren
sudo apt install fail2ban

# Konfiguration für SSH
sudo nano /etc/fail2ban/jail.local
```

Inhalt:
```ini
[sshd]
enabled = true
port = 22
filter = sshd
logpath = /var/log/auth.log
maxretry = 5
bantime = 3600
```

```bash
# Fail2Ban starten
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### Automatische Updates

```bash
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

---

## 📊 Teil 11: Monitoring

### Server-Ressourcen überwachen

```bash
# CPU, RAM, Disk
htop

# Disk-Usage
df -h

# Nginx Status
sudo systemctl status nginx

# Gunicorn Status
sudo systemctl status butler-platform

# PostgreSQL Status
sudo systemctl status postgresql
```

### Backup einrichten

**Datenbank-Backup:**
```bash
# Backup-Skript erstellen
nano /home/butler/backup-db.sh
```

Inhalt:
```bash
#!/bin/bash
BACKUP_DIR="/home/butler/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR
pg_dump -U butler_user butler_platform_prod > $BACKUP_DIR/db_$DATE.sql
# Alte Backups löschen (älter als 30 Tage)
find $BACKUP_DIR -name "db_*.sql" -mtime +30 -delete
```

```bash
# Ausführbar machen
chmod +x /home/butler/backup-db.sh

# Cronjob einrichten (täglich um 3 Uhr)
crontab -e
```

Eintrag:
```
0 3 * * * /home/butler/backup-db.sh
```

---

## ❓ Troubleshooting

### Problem: 502 Bad Gateway

**Lösung:**
```bash
# Überprüfe ob Gunicorn läuft
sudo systemctl status butler-platform

# Neustart
sudo systemctl restart butler-platform

# Logs prüfen
sudo journalctl -u butler-platform -n 50
```

### Problem: Static Files werden nicht geladen

**Lösung:**
```bash
cd /home/butler/butler-platform
source venv/bin/activate
python manage.py collectstatic --noinput
sudo systemctl restart butler-platform
```

### Problem: Datenbank-Verbindung schlägt fehl

**Lösung:**
```bash
# PostgreSQL Status
sudo systemctl status postgresql

# .env Datei überprüfen
cat /home/butler/butler-platform/.env | grep DB_

# Datenbank-Verbindung testen
sudo -u postgres psql -d butler_platform_prod -U butler_user
```

### Problem: Domain nicht erreichbar

**Lösung:**
```bash
# DNS überprüfen
nslookup deine-domain.de

# Nginx Konfiguration testen
sudo nginx -t

# Nginx Logs
sudo tail -f /var/log/nginx/error.log
```

---

## 📞 Support & Hilfe

Bei Problemen:
1. Überprüfe die Logs (siehe oben)
2. GitHub Issues: https://github.com/neubuot/butler-platform/issues
3. Hetzner Support: https://docs.hetzner.com

---

## 🎉 Fertig!

Deine Butler Platform läuft jetzt produktiv auf:
- ✅ **HTTPS** mit Let's Encrypt
- ✅ **PostgreSQL** Datenbank
- ✅ **Gunicorn** Application Server
- ✅ **Nginx** Reverse Proxy
- ✅ **Systemd** Process Management
- ✅ **Firewall** aktiv
- ✅ **Auto-Updates** konfiguriert

**Nächste Schritte:**
1. Frontend-Views entwickeln
2. Test-Daten anlegen
3. Finanzmodul implementieren
4. IoT-Integration vorbereiten

**Viel Erfolg! 🚀**

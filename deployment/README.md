# Deployment Files - Butler Platform

Dieses Verzeichnis enthält alle Dateien und Skripte für das Production-Deployment.

---

## 📁 Dateien-Übersicht

### Haupt-Dateien

**deploy.sh**
- Automatisches Deployment-Skript
- Richtet den kompletten Server ein
- Verwendet: `./deploy.sh` auf dem Production-Server

**generate_secret_key.py**
- Generiert einen sicheren Django SECRET_KEY
- Verwendung: `python3 generate_secret_key.py`

---

### Nginx Konfiguration

**nginx-butler-platform.conf**
- Nginx Virtual Host Konfiguration
- Wird kopiert nach: `/etc/nginx/sites-available/butler-platform`
- **Anpassen**: Ersetze `deine-domain.de` mit deiner echten Domain!

---

### Systemd Services

**butler-platform.service**
- Systemd Service für Gunicorn
- Wird kopiert nach: `/etc/systemd/system/butler-platform.service`
- Startet die Django-Anwendung

**butler-platform.socket**
- Systemd Socket für Gunicorn
- Wird kopiert nach: `/etc/systemd/system/butler-platform.socket`
- Managed die Socket-Kommunikation

---

## 🚀 Schnellstart

### 1. Automatisches Deployment

Auf dem Production-Server (als root):

```bash
# Repository klonen
cd /opt
git clone https://github.com/neubuot/butler-platform.git
cd butler-platform/deployment

# Deployment ausführen
chmod +x deploy.sh
./deploy.sh
```

Das Skript übernimmt alles automatisch!

---

### 2. Manuelle Konfiguration

Falls du einzelne Schritte manuell durchführen möchtest:

#### SECRET_KEY generieren
```bash
python3 generate_secret_key.py
```

#### Nginx konfigurieren
```bash
# Domain anpassen
nano nginx-butler-platform.conf
# Ersetze: deine-domain.de → butler.deine-firma.de

# Kopieren
sudo cp nginx-butler-platform.conf /etc/nginx/sites-available/butler-platform
sudo ln -s /etc/nginx/sites-available/butler-platform /etc/nginx/sites-enabled/

# Testen und neu laden
sudo nginx -t
sudo systemctl reload nginx
```

#### Systemd Services einrichten
```bash
# Services kopieren
sudo cp butler-platform.service /etc/systemd/system/
sudo cp butler-platform.socket /etc/systemd/system/

# Services aktivieren
sudo systemctl daemon-reload
sudo systemctl enable butler-platform.socket
sudo systemctl enable butler-platform.service

# Services starten
sudo systemctl start butler-platform.socket
sudo systemctl start butler-platform.service

# Status überprüfen
sudo systemctl status butler-platform
```

---

## 📋 Wichtige Befehle

### Services verwalten

```bash
# Status überprüfen
sudo systemctl status butler-platform
sudo systemctl status nginx

# Neu starten
sudo systemctl restart butler-platform
sudo systemctl restart nginx

# Logs anzeigen
sudo journalctl -u butler-platform -f
sudo tail -f /var/log/nginx/butler-platform-error.log
```

### Updates deployen

```bash
cd /home/butler/butler-platform
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart butler-platform
```

---

## 🔧 Anpassungen

### Domain ändern

In folgenden Dateien muss die Domain angepasst werden:

1. **nginx-butler-platform.conf**
   ```nginx
   server_name DEINE-DOMAIN.de www.DEINE-DOMAIN.de;
   ```

2. **.env** (auf dem Server)
   ```bash
   ALLOWED_HOSTS=DEINE-DOMAIN.de,www.DEINE-DOMAIN.de
   ```

### Gunicorn Workers anpassen

In **butler-platform.service**:
```ini
# Formel: (2 x CPU-Cores) + 1
# Für CX21 (2 CPUs): --workers 5
ExecStart=... --workers 5 ...
```

### SSL-Pfade

In **nginx-butler-platform.conf** (nach Let's Encrypt):
```nginx
ssl_certificate /etc/letsencrypt/live/DEINE-DOMAIN.de/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/DEINE-DOMAIN.de/privkey.pem;
```

---

## 📚 Weitere Dokumentation

- **../DEPLOYMENT.md** - Vollständige Deployment-Anleitung
- **../DEPLOYMENT_CHECKLIST.md** - Schritt-für-Schritt Checkliste
- **../.env.production.example** - Beispiel Production-Environment

---

## ⚠️ Wichtige Hinweise

### Sicherheit

- **Niemals** .env Dateien ins Git committen!
- **Immer** einen starken SECRET_KEY verwenden
- **Firewall** aktivieren (UFW)
- **Fail2Ban** einrichten
- **SSL-Zertifikat** mit Let's Encrypt

### Backup

Richte regelmäßige Backups ein:
- Datenbank täglich
- Media Files wöchentlich
- Konfigurationsdateien bei Änderungen

---

Bei Fragen: Siehe **../DEPLOYMENT.md** für detaillierte Erklärungen!

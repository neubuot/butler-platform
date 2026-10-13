# 📋 Deployment Checkliste - Butler Platform

Verwende diese Checkliste um sicherzustellen, dass alle Schritte abgeschlossen sind.

---

## Vor dem Deployment

### Lokale Vorbereitung
- [ ] Alle Features getestet
- [ ] Code auf GitHub gepusht
- [ ] `.gitignore` prüfen (keine Secrets im Repo!)
- [ ] `requirements.txt` aktuell

### Server & Domain
- [ ] Hetzner Cloud Server erstellt (CX21 empfohlen)
- [ ] Server-IP-Adresse notiert
- [ ] Domain registriert
- [ ] DNS A-Records erstellt (auf Server-IP zeigend)
- [ ] SSH-Zugriff zum Server funktioniert

---

## Deployment

### Automatisches Setup
- [ ] Auf Server als root eingeloggt
- [ ] Repository geklont: `/opt/butler-platform`
- [ ] Deployment-Skript ausgeführt: `./deployment/deploy.sh`
- [ ] `.env` Datei bearbeitet mit richtigen Werten
- [ ] SECRET_KEY generiert und eingetragen
- [ ] DB_PASSWORD eingetragen
- [ ] ALLOWED_HOSTS korrekt (Domain + IP)
- [ ] Django Superuser erstellt
- [ ] SSL-Zertifikat eingerichtet

### Services
- [ ] Gunicorn läuft: `sudo systemctl status butler-platform`
- [ ] Nginx läuft: `sudo systemctl status nginx`
- [ ] PostgreSQL läuft: `sudo systemctl status postgresql`
- [ ] Keine Fehler in Logs

---

## Testing

### Funktionalität
- [ ] Website erreichbar: `https://deine-domain.de`
- [ ] HTTP → HTTPS Redirect funktioniert
- [ ] SSL-Zertifikat gültig (grünes Schloss)
- [ ] Admin-Panel erreichbar: `https://deine-domain.de/admin`
- [ ] Login mit Superuser funktioniert
- [ ] Static Files laden korrekt (CSS/JS im Admin)

### Logs überprüfen
- [ ] Gunicorn Logs: `/home/butler/butler-platform/logs/gunicorn-error.log`
- [ ] Nginx Logs: `/var/log/nginx/butler-platform-error.log`
- [ ] Django Logs: `/home/butler/butler-platform/logs/django.log`
- [ ] Keine kritischen Fehler

---

## Sicherheit

### Basis-Sicherheit
- [ ] Firewall aktiv: `sudo ufw status`
- [ ] Nur notwendige Ports offen (22, 80, 443)
- [ ] Fail2Ban installiert und konfiguriert
- [ ] SSH-Key-Login (kein Passwort-Login)
- [ ] Root-Login deaktiviert (optional, aber empfohlen)

### Django-Sicherheit
- [ ] `DEBUG=False` in Production
- [ ] `SECRET_KEY` ist einzigartig und sicher
- [ ] `ALLOWED_HOSTS` korrekt konfiguriert
- [ ] SSL-Settings aktiviert (`SECURE_SSL_REDIRECT=True`)
- [ ] CSRF-Protection aktiv
- [ ] Session-Cookies secure

---

## Backup & Monitoring

### Backup
- [ ] Datenbank-Backup-Skript erstellt
- [ ] Cronjob für automatische Backups eingerichtet
- [ ] Backup-Verzeichnis existiert: `/home/butler/backups`
- [ ] Backup getestet (wiederherstellen möglich)

### Monitoring
- [ ] Server-Ressourcen überprüft (`htop`, `df -h`)
- [ ] Disk-Space ausreichend (min. 20% frei)
- [ ] RAM-Usage im grünen Bereich
- [ ] CPU-Load normal

---

## Dokumentation

### Zugangsdaten dokumentiert (SICHER!)
- [ ] Server-IP und Root-Passwort
- [ ] Django Admin-Credentials
- [ ] Datenbank-Credentials
- [ ] SSL-Zertifikat Renewal-E-Mail

### Wichtige Informationen notiert
- [ ] GitHub Repository URL
- [ ] Domain und DNS-Provider
- [ ] Hetzner Cloud Login
- [ ] E-Mail für Benachrichtigungen

---

## Post-Deployment

### Erste Schritte
- [ ] Test-Daten angelegt (IAB-Investoren, Geräte, Mieter)
- [ ] Erste Test-Buchung durchgeführt
- [ ] E-Mail-Benachrichtigungen getestet (falls konfiguriert)

### Optional
- [ ] Automatische Updates konfiguriert
- [ ] Monitoring-Tool installiert (z.B. Uptime Robot)
- [ ] Google Analytics oder Matomo (falls gewünscht)
- [ ] CDN für Static Files (z.B. CloudFlare)

---

## Rollback-Plan (falls Probleme auftreten)

### Schnelles Rollback
```bash
# Zurück zum vorherigen Commit
cd /home/butler/butler-platform
git log --oneline  # Commit-Hash notieren
git checkout <vorheriger-commit-hash>
python manage.py migrate
sudo systemctl restart butler-platform
```

### Datenbank-Restore
```bash
# Backup wiederherstellen
sudo -u postgres psql butler_platform_prod < /home/butler/backups/db_XXXXXX.sql
```

---

## Kontakte für Notfall

- **Hetzner Support**: https://www.hetzner.com/support
- **Let's Encrypt Support**: https://letsencrypt.org/docs/
- **Django Docs**: https://docs.djangoproject.com

---

## Status

**Deployment-Datum**: _________________

**Deployed von**: _________________

**Server-IP**: _________________

**Domain**: _________________

**Status**: ⬜ Geplant | ⬜ In Arbeit | ⬜ Abgeschlossen

---

**Notizen:**

_________________________________________________________________

_________________________________________________________________

_________________________________________________________________

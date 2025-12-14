# Installation & Setup - Butler Platform

Detaillierte Anleitung zur Installation der Butler Asset & Operations Platform.

## Option 1: Lokale Entwicklung (empfohlen für Einsteiger)

### Voraussetzungen
- Python 3.12 oder höher
- Git

### Schritte

1. **Repository klonen**
```bash
git clone https://github.com/DEIN-USERNAME/butler-platform.git
cd butler-platform
```

2. **Virtual Environment erstellen**
```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. **Dependencies installieren**
```bash
pip install -r requirements.txt
```

4. **Umgebungsvariablen einrichten**
```bash
# .env-Datei erstellen
cp .env.example .env

# .env bearbeiten (vorerst können Standardwerte bleiben)
```

5. **Datenbank initialisieren**
```bash
# Migrationen erstellen
python manage.py makemigrations

# Migrationen anwenden
python manage.py migrate

# Superuser erstellen (Admin-Zugang)
python manage.py createsuperuser
```

6. **Entwicklungsserver starten**
```bash
python manage.py runserver
```

Die Anwendung ist nun unter `http://localhost:8000` erreichbar!
- **Admin-Panel**: `http://localhost:8000/admin`

---

## Option 2: Docker (für Production-ähnliche Umgebung)

### Voraussetzungen
- Docker
- Docker Compose

### Schritte

1. **Repository klonen**
```bash
git clone https://github.com/DEIN-USERNAME/butler-platform.git
cd butler-platform
```

2. **Umgebungsvariablen einrichten**
```bash
cp .env.example .env
# Bearbeite .env und passe Datenbank-Credentials an
```

3. **Docker Container starten**
```bash
# Container bauen und starten
docker-compose up -d

# Datenbank migrieren
docker-compose exec web python manage.py migrate

# Superuser erstellen
docker-compose exec web python manage.py createsuperuser
```

Die Anwendung ist nun unter `http://localhost:8000` erreichbar!

### Nützliche Docker-Befehle
```bash
# Logs anzeigen
docker-compose logs -f

# Container stoppen
docker-compose down

# Container neu starten
docker-compose restart

# Shell in Container öffnen
docker-compose exec web bash
```

---

## Erste Schritte nach der Installation

### 1. Admin-Panel erkunden
- Gehe zu `http://localhost:8000/admin`
- Logge dich mit deinem Superuser ein
- Erkunde die Modelle: Benutzer, Butler-Geräte, Buchungen

### 2. Test-Daten anlegen

**IAB-Investor erstellen:**
1. Gehe zu Admin → Benutzer → Hinzufügen
2. Benutzertyp: IAB-Investor
3. Fülle Firmendaten aus
4. Speichern

**Butler-Gerät erstellen:**
1. Gehe zu Admin → Butler-Geräte → Hinzufügen
2. Seriennummer: z.B. "BUT-S50-001"
3. Modell: Butler S (50 kVA / 25 kWh)
4. Eigentümer: Wähle den IAB-Investor
5. Fülle technische Daten aus
6. Speichern

**Gewerblichen Mieter erstellen:**
1. Gehe zu Admin → Benutzer → Hinzufügen
2. Benutzertyp: Gewerblicher Mieter
3. Firmenname eingeben
4. Speichern

**Buchung erstellen:**
1. Gehe zu Admin → Buchungen → Hinzufügen
2. Gerät auswählen
3. Mieter auswählen
4. Zeitraum festlegen
5. Einsatzbereich wählen
6. Preise eingeben
7. Speichern

---

## Problemlösungen

### Problem: Port 8000 bereits belegt
```bash
# Anderen Port verwenden
python manage.py runserver 8001
```

### Problem: Migrations-Fehler
```bash
# Alle Migrationen zurücksetzen (ACHTUNG: Löscht Daten!)
python manage.py migrate accounts zero
python manage.py migrate assets zero
python manage.py migrate bookings zero
rm -rf */migrations/0*.py
python manage.py makemigrations
python manage.py migrate
```

### Problem: PostgreSQL-Verbindung schlägt fehl
- Prüfe ob PostgreSQL läuft
- Prüfe Datenbank-Credentials in .env
- Für lokale Entwicklung: Verwende SQLite (Standard)

---

## Nächste Schritte

Nach erfolgreicher Installation:
1. ✅ Lege Test-Daten an
2. ✅ Erkunde das Admin-Panel
3. ✅ Push das Projekt zu GitHub (siehe GITHUB.md)
4. ⏭ Entwickle die Views und Templates (Phase 2)

---

Bei Problemen: Erstelle ein Issue im GitHub-Repository!

# 🚀 Quickstart - Butler Platform

Die schnellste Art, mit der Butler Platform zu starten!

## ⚡ 5-Minuten-Setup

### Linux / Mac

```bash
# 1. Repository klonen
git clone https://github.com/DEIN-USERNAME/butler-platform.git
cd butler-platform

# 2. Setup-Skript ausführen
./setup.sh

# 3. Server starten
source venv/bin/activate
python manage.py runserver

# 4. Browser öffnen
# http://localhost:8000/admin
```

### Windows

```cmd
REM 1. Repository klonen
git clone https://github.com/DEIN-USERNAME/butler-platform.git
cd butler-platform

REM 2. Setup-Skript ausführen
setup.bat

REM 3. Server starten
venv\Scripts\activate
python manage.py runserver

REM 4. Browser öffnen
REM http://localhost:8000/admin
```

---

## 📋 Was ist passiert?

Das Setup-Skript hat automatisch:
- ✅ Virtual Environment erstellt
- ✅ Alle Python-Pakete installiert
- ✅ Datenbank initialisiert (SQLite)
- ✅ `.env` Konfiguration angelegt
- ✅ (Optional) Admin-User erstellt

---

## 🎯 Erste Schritte

### 1. Admin-Panel öffnen
- URL: `http://localhost:8000/admin`
- Login mit deinem Superuser

### 2. Erste Daten anlegen

**IAB-Investor erstellen:**
```
Admin → Benutzer → Hinzufügen
- Benutzertyp: IAB-Investor
- Username: investor1
- E-Mail: investor@example.com
- Firmenname: Beispiel GmbH
```

**Butler-Gerät anlegen:**
```
Admin → Butler-Geräte → Hinzufügen
- Seriennummer: BUT-S50-001
- Modell: Butler S (50 kVA / 25 kWh)
- Eigentümer: [investor1]
- Nennleistung: 50.0 kVA
- Batteriekapazität: 25.0 kWh
- Kaufdatum: [heute]
- Kaufpreis: 50000.00
```

**Mieter erstellen:**
```
Admin → Benutzer → Hinzufügen
- Benutzertyp: Gewerblicher Mieter
- Username: mieter1
- Firmenname: Bau AG
```

**Buchung erstellen:**
```
Admin → Buchungen → Hinzufügen
- Gerät: BUT-S50-001
- Mieter: mieter1
- Startdatum: [morgen]
- Enddatum: [in 7 Tagen]
- Einsatzbereich: Baustelle/Kranbetrieb
- Tagessatz: 250.00
```

---

## 📚 Weiterführende Dokumentation

- **INSTALLATION.md** - Detaillierte Installation
- **GITHUB.md** - GitHub-Setup
- **README.md** - Projekt-Übersicht

---

## ❓ Häufige Probleme

### Port 8000 belegt?
```bash
python manage.py runserver 8001
```

### Datenbank zurücksetzen?
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Dependencies aktualisieren?
```bash
pip install -r requirements.txt --upgrade
```

---

## 🎨 Projekt-Struktur (Kurzübersicht)

```
butler-platform/
├── accounts/      # User-Management
├── assets/        # Butler-Geräte
├── bookings/      # Buchungen
├── config/        # Django-Settings
├── manage.py      # Django-CLI
└── setup.sh/.bat  # Setup-Skripte
```

---

## 🔄 Nächste Schritte

Nach dem Setup:

1. **Phase 1**: Admin-Interface nutzen ✅ (Du bist hier!)
2. **Phase 2**: Frontend-Views entwickeln 📝
3. **Phase 3**: Finanzmodul implementieren 💰
4. **Phase 4**: IoT-Integration 🌐

---

Viel Erfolg! 🚀

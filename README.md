# Butler Asset & Operations Platform

Eine webbasierte Asset-Management-Plattform für die Verwaltung von Butler-Energiesystemen, die IAB-Investoren, die rhk-mobil GmbH als Betreiber und gewerbliche Mieter miteinander verbindet.

## 🎯 Projekt-Übersicht

Die Butler Asset & Operations Platform ermöglicht:

- **IAB-Investoren**: Verwaltung ihrer Butler-Geräte-Investments und Übersicht über Erträge
- **rhk-mobil GmbH**: Full-Service-Management der Geräteflotte, Vermietung und Wartung
- **Gewerbliche Mieter**: Buchung und Nutzung von Butler-Energiesystemen

## 🚀 MVP Features (Phase 1)

### 1. User Management
- Drei Benutzerrollen: IAB-Investor, rhk-mobil Admin, Mieter
- Authentifizierung und Rechteverwaltung

### 2. Asset-Verwaltung
- Butler-Geräte-Stammdaten (S 50/25, M 150/150)
- Zuordnung Gerät → Eigentümer
- Technische Spezifikationen

### 3. IAB-Eigentümer-Dashboard
- Übersicht eigener Assets
- Ertragsdarstellung
- Gerätestatus

### 4. Buchungsportal
- Kalenderansicht verfügbarer Geräte
- Buchungsanfragen durch Mieter
- Mietkalkulation

## 🛠 Tech Stack

- **Backend**: Django 6.0 (Python)
- **Frontend**: Django Templates (MVP), später optional React
- **Datenbank**: PostgreSQL
- **API**: Django REST Framework
- **Deployment**: Docker

## 📋 Voraussetzungen

- Python 3.12+
- PostgreSQL 14+ (oder SQLite für Entwicklung)
- Git

## 🔧 Installation & Setup

### 1. Repository klonen

```bash
git clone https://github.com/DEIN-USERNAME/butler-platform.git
cd butler-platform
```

### 2. Virtual Environment erstellen

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oder
venv\Scripts\activate  # Windows
```

### 3. Dependencies installieren

```bash
pip install -r requirements.txt
```

### 4. Umgebungsvariablen konfigurieren

```bash
cp .env.example .env
# Bearbeite .env und füge deine Konfiguration hinzu
```

### 5. Datenbank initialisieren

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6. Entwicklungsserver starten

```bash
python manage.py runserver
```

Die Anwendung ist nun unter `http://localhost:8000` erreichbar.

## 📁 Projekt-Struktur

```
butler-platform/
├── accounts/           # User-Management (IAB, rhk-mobil, Mieter)
├── assets/            # Butler-Geräte-Verwaltung
├── bookings/          # Buchungsportal und Vermietung
├── config/            # Django-Hauptkonfiguration
├── static/            # Statische Dateien (CSS, JS, Images)
├── templates/         # HTML-Templates
├── media/             # Hochgeladene Dateien
├── .env.example       # Beispiel-Umgebungsvariablen
├── .gitignore         # Git-Ignore-Datei
├── manage.py          # Django-Management-Script
├── requirements.txt   # Python-Dependencies
└── README.md          # Diese Datei
```

## 🗂 Datenmodelle (MVP)

### accounts.CustomUser
- Benutzertyp (IAB-Investor, rhk-mobil, Mieter)
- Kontaktdaten
- Unternehmensinformationen

### assets.ButlerDevice
- Modell (S 50/25, M 150/150)
- Seriennummer
- Technische Spezifikationen
- Eigentümer (ForeignKey zu User)
- Status (verfügbar, vermietet, Wartung)

### bookings.Booking
- Gerät (ForeignKey zu ButlerDevice)
- Mieter (ForeignKey zu User)
- Zeitraum (Start, Ende)
- Status (Anfrage, Bestätigt, Abgelehnt)
- Einsatzbereich

## 🔐 Sicherheit

- **Keine Secrets im Repository!** Alle sensiblen Daten gehören in `.env`
- `.env` ist in `.gitignore` eingetragen
- Verwende starke SECRET_KEYs in Production
- HTTPS für Production-Deployment

## 📝 Entwicklungs-Roadmap

### ✅ Phase 1 - MVP (aktuell)
- [x] Projekt-Setup
- [ ] User-Management
- [ ] Asset-Verwaltung
- [ ] IAB-Dashboard
- [ ] Buchungsportal

### 🔜 Phase 2 - Erweiterte Features
- [ ] Finanzmodul & Ertragsberechnung
- [ ] Wartungsplanung
- [ ] Logistikmanagement

### 🔮 Phase 3 - IoT-Integration
- [ ] Insights-Platform-Integration
- [ ] Echtzeit-Monitoring
- [ ] Alarm-System

## 🤝 Mitwirken

Dieses ist ein privates Projekt. Kontaktiere den Projektinhaber für Zugriff.

## 📄 Lizenz

Proprietär - Alle Rechte vorbehalten

## 📧 Kontakt

Bei Fragen kontaktiere: [DEINE-EMAIL]

---

**Entwickelt für rhk-mobil GmbH**

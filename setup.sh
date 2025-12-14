#!/bin/bash

# Butler Platform - Setup Script
# Dieses Skript richtet die Entwicklungsumgebung ein

echo "🚀 Butler Platform - Setup wird gestartet..."
echo ""

# Prüfe Python-Version
echo "📍 Prüfe Python-Version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python 3 ist nicht installiert!"
    exit 1
fi

# Virtual Environment erstellen
echo ""
echo "📦 Erstelle Virtual Environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "❌ Fehler beim Erstellen des Virtual Environment!"
    exit 1
fi

# Virtual Environment aktivieren
echo ""
echo "🔧 Aktiviere Virtual Environment..."
source venv/bin/activate

# Dependencies installieren
echo ""
echo "📥 Installiere Python-Packages..."
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Fehler beim Installieren der Dependencies!"
    exit 1
fi

# .env Datei erstellen falls nicht vorhanden
if [ ! -f .env ]; then
    echo ""
    echo "📝 Erstelle .env Datei..."
    cp .env.example .env
    echo "✅ .env Datei erstellt. Bitte bearbeite diese Datei und passe die Einstellungen an."
fi

# Datenbank-Migrationen
echo ""
echo "🗄️  Erstelle Datenbank-Migrationen..."
python manage.py makemigrations
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "❌ Fehler bei den Datenbank-Migrationen!"
    exit 1
fi

# Superuser erstellen
echo ""
echo "👤 Möchtest du einen Admin-User erstellen? (j/n)"
read -r create_superuser
if [ "$create_superuser" = "j" ] || [ "$create_superuser" = "J" ]; then
    python manage.py createsuperuser
fi

echo ""
echo "✅ Setup erfolgreich abgeschlossen!"
echo ""
echo "📚 Nächste Schritte:"
echo "1. Aktiviere das Virtual Environment: source venv/bin/activate"
echo "2. Starte den Server: python manage.py runserver"
echo "3. Öffne http://localhost:8000/admin im Browser"
echo ""
echo "📖 Weitere Informationen findest du in INSTALLATION.md und GITHUB.md"
echo ""

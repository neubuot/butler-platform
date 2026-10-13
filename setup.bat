@echo off
REM Butler Platform - Setup Script für Windows
REM Dieses Skript richtet die Entwicklungsumgebung ein

echo.
echo Butler Platform - Setup wird gestartet...
echo.

REM Prüfe Python-Version
echo Pruefe Python-Version...
python --version
if %errorlevel% neq 0 (
    echo Python ist nicht installiert oder nicht im PATH!
    pause
    exit /b 1
)

REM Virtual Environment erstellen
echo.
echo Erstelle Virtual Environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo Fehler beim Erstellen des Virtual Environment!
    pause
    exit /b 1
)

REM Virtual Environment aktivieren
echo.
echo Aktiviere Virtual Environment...
call venv\Scripts\activate.bat

REM Dependencies installieren
echo.
echo Installiere Python-Packages...
python -m pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Fehler beim Installieren der Dependencies!
    pause
    exit /b 1
)

REM .env Datei erstellen falls nicht vorhanden
if not exist .env (
    echo.
    echo Erstelle .env Datei...
    copy .env.example .env
    echo .env Datei erstellt. Bitte bearbeite diese Datei und passe die Einstellungen an.
)

REM Datenbank-Migrationen
echo.
echo Erstelle Datenbank-Migrationen...
python manage.py makemigrations
python manage.py migrate
if %errorlevel% neq 0 (
    echo Fehler bei den Datenbank-Migrationen!
    pause
    exit /b 1
)

REM Superuser erstellen
echo.
set /p create_superuser="Moechtest du einen Admin-User erstellen? (j/n): "
if /i "%create_superuser%"=="j" (
    python manage.py createsuperuser
)

echo.
echo Setup erfolgreich abgeschlossen!
echo.
echo Naechste Schritte:
echo 1. Aktiviere das Virtual Environment: venv\Scripts\activate
echo 2. Starte den Server: python manage.py runserver
echo 3. Oeffne http://localhost:8000/admin im Browser
echo.
echo Weitere Informationen findest du in INSTALLATION.md und GITHUB.md
echo.
pause

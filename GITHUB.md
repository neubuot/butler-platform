# GitHub Setup - Butler Platform

Schritt-für-Schritt Anleitung um das Butler-Projekt auf GitHub hochzuladen.

## Voraussetzungen

1. **GitHub-Account**: Du hast bereits einen Account
2. **Git installiert**: Prüfen mit `git --version`
3. **SSH-Key eingerichtet** (optional aber empfohlen)

---

## Schritt 1: Neues Repository auf GitHub erstellen

1. Gehe zu https://github.com
2. Klicke auf den **grünen "New"** Button (oben links) oder **"+"** → **"New repository"**
3. Fülle die Felder aus:
   - **Repository name**: `butler-platform`
   - **Description**: "Butler Asset & Operations Platform - Asset-Management für Butler-Energiesysteme"
   - **Visibility**: **Private** ✅ (sehr wichtig!)
   - **NICHT** "Initialize this repository with..." aktivieren (alles leer lassen!)
4. Klicke auf **"Create repository"**

GitHub zeigt dir jetzt Anleitungen. Du brauchst die **HTTPS-URL** oder **SSH-URL**:
- HTTPS: `https://github.com/DEIN-USERNAME/butler-platform.git`
- SSH: `git@github.com:DEIN-USERNAME/butler-platform.git`

---

## Schritt 2: Projekt zu GitHub hochladen

### Im Terminal (im butler-platform Verzeichnis):

```bash
# 1. Navigiere zum Projekt-Verzeichnis
cd /pfad/zu/butler-platform

# 2. Git initialisieren (falls noch nicht geschehen)
git init

# 3. Alle Dateien zum Staging hinzufügen
git add .

# 4. Ersten Commit erstellen
git commit -m "Initial commit: Butler Platform MVP setup"

# 5. Main-Branch umbenennen (GitHub verwendet 'main' statt 'master')
git branch -M main

# 6. GitHub-Repository als Remote hinzufügen
# Ersetze DEIN-USERNAME mit deinem GitHub-Nutzernamen!
git remote add origin https://github.com/DEIN-USERNAME/butler-platform.git

# 7. Code zu GitHub pushen
git push -u origin main
```

**Beim ersten Push wirst du nach deinen GitHub-Zugangsdaten gefragt:**
- Username: Dein GitHub-Username
- Password: **Personal Access Token** (NICHT dein normales Passwort!)

---

## Schritt 3: Personal Access Token erstellen (falls nötig)

Falls du noch keinen Token hast:

1. Gehe zu GitHub → Settings (Profil-Icon oben rechts)
2. Scrolle ganz nach unten → **Developer settings**
3. **Personal access tokens** → **Tokens (classic)**
4. **Generate new token** → **Generate new token (classic)**
5. Einstellungen:
   - **Note**: "Butler Platform Development"
   - **Expiration**: 90 Tage (oder länger)
   - **Scopes**: ✅ `repo` (alle Repo-Berechtigungen)
6. **Generate token** klicken
7. **Token kopieren** (wird nur einmal angezeigt!)
8. Verwende diesen Token als "Password" beim Git-Push

---

## Schritt 4: Verifizierung

Nach erfolgreichem Push:

1. Gehe zu `https://github.com/DEIN-USERNAME/butler-platform`
2. Du solltest alle Dateien sehen
3. README.md wird automatisch angezeigt
4. Prüfe ob das 🔒 **Private** Symbol oben rechts sichtbar ist

---

## Wichtige Git-Befehle für die tägliche Arbeit

### Änderungen hochladen
```bash
# Status prüfen (welche Dateien wurden geändert?)
git status

# Alle Änderungen hinzufügen
git add .

# Commit mit Beschreibung
git commit -m "Beschreibung der Änderungen"

# Zu GitHub pushen
git push
```

### Änderungen herunterladen
```bash
# Neueste Version von GitHub holen
git pull
```

### Branches verwalten
```bash
# Neuen Branch erstellen
git checkout -b feature/neue-funktion

# Zurück zu main wechseln
git checkout main

# Branch pushen
git push -u origin feature/neue-funktion
```

---

## Best Practices

### ✅ DO:
- Regelmäßig committen (nach jeder kleinen Änderung)
- Aussagekräftige Commit-Messages schreiben
- `.env` Datei NIEMALS committen (ist in .gitignore)
- Vor dem Pushen testen ob alles funktioniert

### ❌ DON'T:
- Niemals Passwörter oder API-Keys committen
- Nicht die gesamte venv/ oder node_modules/ hochladen
- Nicht direkt auf main pushen in Produktionsumgebungen

---

## Beispiel-Commit-Messages

**Gut:**
```
✅ "Add ButlerDevice model with technical specifications"
✅ "Fix booking validation for overlapping dates"
✅ "Update README with installation instructions"
```

**Schlecht:**
```
❌ "changes"
❌ "fix"
❌ "asdf"
```

---

## Zusammenarbeit mit anderen Entwicklern

### Andere Personen einladen:
1. Gehe zu deinem Repository auf GitHub
2. **Settings** → **Collaborators**
3. **Add people**
4. E-Mail oder Username eingeben
5. Einladung versenden

---

## Nächste Schritte

Nach erfolgreichem GitHub-Setup:
1. ✅ Repository ist online und sicher
2. ✅ Versionskontrolle ist aktiv
3. ⏭ Weiter mit der Entwicklung
4. ⏭ CI/CD später einrichten (GitHub Actions)

---

## Troubleshooting

### Problem: "Permission denied (publickey)"
→ Du verwendest SSH ohne konfigurierten SSH-Key
→ Lösung: Verwende HTTPS-URL statt SSH

### Problem: "remote: Repository not found"
→ URL ist falsch oder du hast keinen Zugriff
→ Lösung: Prüfe URL und Berechtigungen

### Problem: "Updates were rejected"
→ Jemand anderes hat gepusht
→ Lösung: `git pull` vor dem Push

---

## Hilfreiche Links

- Git Basics: https://git-scm.com/book/de/v2
- GitHub Docs: https://docs.github.com
- Personal Access Tokens: https://github.com/settings/tokens

Bei Fragen: Erstelle ein Issue im Repository!

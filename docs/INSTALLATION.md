# Installation & Setup Guide

Diese Anleitung beschreibt die Installation und Einrichtung des NIS2 ISMS.

## Systemvoraussetzungen

- **Python**: 3.9 oder höher
- **Node.js**: 18 oder höher
- **Git**: Für das Klonen des Repositories
- **Betriebssystem**: Linux, macOS oder Windows

## Installation

### 1. Repository klonen

```bash
git clone <repository-url>
cd ISMS
```

### 2. Backend installieren

```bash
cd backend

# Virtuelle Umgebung erstellen
python -m venv venv

# Aktivieren
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Dependencies installieren
pip install -r requirements.txt

# Umgebungsvariablen konfigurieren
cp .env.example .env
# Bearbeiten Sie .env und ändern Sie mindestens:
# - SECRET_KEY (generieren Sie einen sicheren Schlüssel)
# - ADMIN_PASSWORD (ändern Sie das Standard-Passwort!)
```

### 3. Frontend installieren

```bash
cd ../frontend

# Dependencies installieren
npm install
```

## Konfiguration

### Backend-Konfiguration (.env)

Wichtigste Einstellungen in `backend/.env`:

```env
# Sicherheit - WICHTIG: Ändern Sie diese Werte!
SECRET_KEY=<generieren-Sie-einen-langen-zufälligen-String>
ADMIN_PASSWORD=<sicheres-passwort>

# Datenbank
DATABASE_URL=sqlite:///./nis2_isms.db
# Für PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost/nis2_isms

# CORS (Frontend-URLs)
CORS_ORIGINS=["http://localhost:5173"]
```

### Sicheren SECRET_KEY generieren

Python:
```python
import secrets
print(secrets.token_urlsafe(32))
```

Oder online: https://generate-secret.vercel.app/32

## Erste Schritte

### 1. Backend starten

```bash
cd backend
source venv/bin/activate  # oder venv\Scripts\activate auf Windows

# Development Server
python -m app.main

# Oder mit uvicorn direkt
uvicorn app.main:app --reload
```

Das Backend läuft nun auf: http://localhost:8000

API-Dokumentation: http://localhost:8000/docs

### 2. Frontend starten

```bash
cd frontend

# Development Server
npm run dev
```

Das Frontend läuft nun auf: http://localhost:5173

### 3. Erste Anmeldung

1. Öffnen Sie http://localhost:5173
2. Melden Sie sich mit den Standard-Credentials an:
   - **Benutzername**: admin
   - **Passwort**: admin (oder was Sie in .env konfiguriert haben)

**WICHTIG**: Ändern Sie das Admin-Passwort sofort nach der ersten Anmeldung!

## Datenbank

### SQLite (Standard)

- Die SQLite-Datenbank wird automatisch erstellt bei `backend/nis2_isms.db`
- Keine zusätzliche Konfiguration nötig
- Geeignet für kleine bis mittlere Installationen

### PostgreSQL (Empfohlen für Production)

1. PostgreSQL installieren und Datenbank erstellen:

```bash
sudo -u postgres psql
CREATE DATABASE nis2_isms;
CREATE USER nis2user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE nis2_isms TO nis2user;
\q
```

2. In `backend/.env` konfigurieren:

```env
DATABASE_URL=postgresql://nis2user:secure_password@localhost/nis2_isms
```

3. Backend neu starten - Tabellen werden automatisch erstellt

## Initiale Daten

Beim ersten Start werden automatisch geladen:

- **Admin-Benutzer** (konfiguriert in .env)
- **13 NIS2-Anforderungen** (aus `backend/app/data/nis2_requirements.json`)

## Production Deployment

### Backend (Python/FastAPI)

Empfohlene Setups:

**Option 1: Gunicorn + Nginx**

```bash
# Gunicorn installieren
pip install gunicorn

# Starten
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

**Option 2: Docker**

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend (React)

```bash
cd frontend

# Production Build erstellen
npm run build

# dist/ Ordner mit Nginx oder einem anderen Webserver hosten
```

**Nginx Konfiguration Beispiel:**

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        root /path/to/ISMS/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Sicherheitshinweise

### Vor dem Production-Einsatz

- ✅ Ändern Sie SECRET_KEY
- ✅ Ändern Sie Admin-Passwort
- ✅ Verwenden Sie HTTPS
- ✅ Konfigurieren Sie Firewall
- ✅ Aktivieren Sie nur benötigte CORS-Origins
- ✅ Verwenden Sie PostgreSQL statt SQLite
- ✅ Konfigurieren Sie regelmäßige Backups
- ✅ Aktualisieren Sie Dependencies regelmäßig

## Backup

### SQLite Backup

```bash
# Einfaches Kopieren
cp backend/nis2_isms.db backend/nis2_isms.db.backup

# Oder mit sqlite3
sqlite3 backend/nis2_isms.db ".backup 'backup.db'"
```

### PostgreSQL Backup

```bash
pg_dump nis2_isms > backup.sql

# Restore
psql nis2_isms < backup.sql
```

## Updates

```bash
# Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt --upgrade

# Frontend
cd frontend
npm update

# Datenbank-Migration (falls nötig)
# Bei Schema-Änderungen kann Alembic verwendet werden
```

## Troubleshooting

### Backend startet nicht

- Überprüfen Sie, ob Port 8000 frei ist: `lsof -i :8000`
- Prüfen Sie die .env Datei auf Syntaxfehler
- Schauen Sie in die Logs

### Frontend kann nicht mit Backend kommunizieren

- Überprüfen Sie CORS_ORIGINS in backend/.env
- Stellen Sie sicher, dass Backend läuft (http://localhost:8000)
- Prüfen Sie Browser-Konsole auf Fehler

### Datenbank-Fehler

- Prüfen Sie DATABASE_URL Syntax
- Bei SQLite: Schreibrechte im backend/ Ordner prüfen
- Bei PostgreSQL: Verbindung und Credentials prüfen

## Support

Bei Problemen:
1. Prüfen Sie die Logs (Backend: Terminal-Output)
2. Schauen Sie in die API-Dokumentation (http://localhost:8000/docs)
3. Erstellen Sie ein Issue im Repository

## Weiterführende Dokumentation

- [Microsoft Entra Setup](ENTRA_SETUP.md)
- [Administrator Handbuch](ADMIN_GUIDE.md)
- [Benutzerhandbuch](USER_GUIDE.md)

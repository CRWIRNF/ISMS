# Docker Deployment Guide

Diese Anleitung beschreibt, wie Sie das NIS2 ISMS mit Docker und Portainer betreiben.

## 📋 Übersicht

Das System besteht aus folgenden Docker-Containern:

1. **Backend** - FastAPI (Python)
2. **Frontend** - React/Nginx
3. **PostgreSQL** - Datenbank (Production) oder SQLite im Backend-Container

## 🚀 Deployment-Optionen

### Option 1: Docker Compose (Lokal/Entwicklung)

Einfachstes Setup mit SQLite-Datenbank:

```bash
# .env Datei erstellen
cp .env.docker .env
# Bearbeiten Sie .env und ändern Sie SECRET_KEY und ADMIN_PASSWORD!

# Container starten
docker-compose up -d

# Logs anzeigen
docker-compose logs -f

# Container stoppen
docker-compose down
```

Zugriff: **http://localhost**

### Option 2: Docker Compose Production (mit PostgreSQL)

Produktions-Setup mit PostgreSQL:

```bash
# .env Datei erstellen
cp .env.docker .env
# Bearbeiten Sie .env und setzen Sie:
# - SECRET_KEY (sicher generieren!)
# - ADMIN_PASSWORD
# - POSTGRES_PASSWORD

# Container starten
docker-compose -f docker-compose.prod.yml up -d

# Logs anzeigen
docker-compose -f docker-compose.prod.yml logs -f
```

### Option 3: Portainer Stack (Empfohlen für Production)

## 🐳 Portainer Deployment

### Voraussetzungen

- Portainer CE/EE installiert und laufend
- Docker Environment in Portainer konfiguriert
- Zugriff auf Git-Repository oder Image Registry

### Schritt 1: Images bauen

**Option A: Lokales Bauen und Push zu Registry**

```bash
# Backend Image bauen
cd backend
docker build -t your-registry.com/nis2-isms-backend:latest .
docker push your-registry.com/nis2-isms-backend:latest

# Frontend Image bauen
cd ../frontend
docker build -t your-registry.com/nis2-isms-frontend:latest .
docker push your-registry.com/nis2-isms-frontend:latest
```

**Option B: Portainer baut direkt aus Git**

In `portainer-stack.yml` ist bereits konfiguriert:
```yaml
build:
  context: https://github.com/your-repo/ISMS.git#main:backend
```

### Schritt 2: Stack in Portainer erstellen

1. **Portainer öffnen** und zu Ihrem Environment navigieren
2. **Stacks** > **Add stack** klicken
3. **Name** eingeben: `nis2-isms`
4. **Build method** wählen:

#### Methode A: Git Repository

- **Repository URL**: `https://github.com/your-repo/ISMS`
- **Repository reference**: `refs/heads/main`
- **Compose path**: `portainer-stack.yml`

#### Methode B: Web editor

- Kopieren Sie den Inhalt von `portainer-stack.yml`
- Passen Sie Image-Namen an, falls nötig

5. **Environment variables** hinzufügen:

```
SECRET_KEY=<generieren Sie einen sicheren Schlüssel>
ADMIN_PASSWORD=<sicheres Passwort>
POSTGRES_PASSWORD=<sicheres Passwort>
```

6. **Deploy the stack** klicken

### Schritt 3: Verifizierung

Nach dem Deployment:

1. **Container-Status prüfen** - alle Container sollten "running" sein
2. **Logs überprüfen**:
   - Backend: Sollte "Application startup complete" zeigen
   - PostgreSQL: Sollte "database system is ready" zeigen
3. **Health Checks prüfen** - alle sollten "healthy" sein

### Schritt 4: Zugriff

- **Frontend**: http://your-server-ip
- **API Docs**: http://your-server-ip:8000/docs (falls Port 8000 exposed ist)
- **Login**: admin / <IHR-ADMIN-PASSWORD>

## 🔐 Sicherer SECRET_KEY generieren

**Methode 1: Python**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Methode 2: OpenSSL**
```bash
openssl rand -base64 32
```

**Methode 3: Online**
https://generate-secret.vercel.app/32

## 📊 Portainer Environment Variables

Setzen Sie diese Variablen in Portainer unter Stack > Environment variables:

### Pflichtfelder (unbedingt ändern!)

| Variable | Beschreibung | Beispiel |
|----------|--------------|----------|
| `SECRET_KEY` | JWT-Secret (min. 32 Zeichen) | `abc123...` |
| `ADMIN_PASSWORD` | Admin-Passwort | `SecurePass123!` |
| `POSTGRES_PASSWORD` | Datenbank-Passwort | `DBPass123!` |

### Optional

| Variable | Beschreibung | Default |
|----------|--------------|---------|
| `ADMIN_USERNAME` | Admin-Benutzername | `admin` |
| `ADMIN_EMAIL` | Admin-E-Mail | `admin@example.com` |
| `POSTGRES_USER` | DB-Benutzer | `nis2user` |
| `POSTGRES_DB` | DB-Name | `nis2_isms` |

### Microsoft Entra (Optional)

| Variable | Beschreibung |
|----------|--------------|
| `ENTRA_ENABLED` | `True` oder `False` |
| `ENTRA_TENANT_ID` | Azure AD Tenant ID |
| `ENTRA_CLIENT_ID` | Application (client) ID |
| `ENTRA_CLIENT_SECRET` | Client Secret |

## 🔄 Updates durchführen

### Über Portainer

1. Neue Images bauen und pushen (oder Git-Repo aktualisieren)
2. In Portainer: **Stacks** > **nis2-isms**
3. **Update the stack** > **Pull and redeploy**

### Via CLI

```bash
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d
```

## 💾 Backup & Restore

### PostgreSQL Backup

**Über Portainer:**

1. **Containers** > **nis2-isms-postgres** > **Console**
2. Führen Sie aus:
```bash
pg_dump -U nis2user nis2_isms > /tmp/backup.sql
```
3. Kopieren Sie die Datei aus dem Container:
```bash
docker cp nis2-isms-postgres:/tmp/backup.sql ./backup.sql
```

**Via CLI:**
```bash
# Backup erstellen
docker exec nis2-isms-postgres pg_dump -U nis2user nis2_isms > backup.sql

# Restore
docker exec -i nis2-isms-postgres psql -U nis2user nis2_isms < backup.sql
```

### Volume Backup

```bash
# PostgreSQL Volume sichern
docker run --rm \
  -v nis2-isms_postgres-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/postgres-backup.tar.gz -C /data .

# Restore
docker run --rm \
  -v nis2-isms_postgres-data:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/postgres-backup.tar.gz -C /data
```

## 🌐 HTTPS/SSL mit Reverse Proxy

### Option 1: Traefik (empfohlen mit Portainer)

In Portainer können Sie einen Traefik-Proxy davor setzen:

```yaml
labels:
  - "traefik.enable=true"
  - "traefik.http.routers.nis2-isms.rule=Host(`nis2.your-domain.com`)"
  - "traefik.http.routers.nis2-isms.entrypoints=websecure"
  - "traefik.http.routers.nis2-isms.tls.certresolver=letsencrypt"
```

### Option 2: Nginx Proxy Manager

1. Erstellen Sie einen Proxy Host in NPM
2. **Domain**: nis2.your-domain.com
3. **Forward Hostname/IP**: nis2-isms-frontend
4. **Forward Port**: 80
5. SSL-Zertifikat anfordern (Let's Encrypt)

### Option 3: Eigenes SSL-Zertifikat

Mounten Sie Zertifikate in den Frontend-Container:

```yaml
frontend:
  volumes:
    - ./certs/cert.pem:/etc/nginx/certs/cert.pem:ro
    - ./certs/key.pem:/etc/nginx/certs/key.pem:ro
```

## 📈 Monitoring in Portainer

Portainer zeigt automatisch:

- **Container-Status** und Health Checks
- **Ressourcen-Nutzung** (CPU, RAM, Netzwerk)
- **Logs** in Echtzeit
- **Console-Zugriff** für Debugging

### Health Check Status

Alle Container haben Health Checks:

- **Backend**: Prüft `/api/health` Endpoint
- **Frontend**: Prüft HTTP-Verfügbarkeit
- **PostgreSQL**: Prüft `pg_isready`

## 🐛 Troubleshooting

### Backend startet nicht

**Logs prüfen:**
```bash
docker logs nis2-isms-backend
```

**Häufige Probleme:**
- Datenbank nicht erreichbar → Prüfen Sie PostgreSQL-Container
- Ungültiger SECRET_KEY → Setzen Sie neue Environment Variable
- Port bereits belegt → Ändern Sie Port-Mapping

### Frontend kann Backend nicht erreichen

**Nginx-Konfiguration prüfen:**
```bash
docker exec nis2-isms-frontend cat /etc/nginx/conf.d/default.conf
```

**Prüfen Sie:**
- Backend-Container läuft: `docker ps | grep backend`
- Netzwerk-Verbindung: `docker exec nis2-isms-frontend ping backend`
- Browser-Konsole auf CORS-Fehler prüfen

### PostgreSQL Connection Error

**Prüfen Sie:**
```bash
# PostgreSQL läuft?
docker ps | grep postgres

# Verbindung testen
docker exec nis2-isms-backend python -c "
from sqlalchemy import create_engine
import os
engine = create_engine(os.getenv('DATABASE_URL'))
with engine.connect() as conn:
    print('Connection successful!')
"
```

### Container restart-Loop

**Health Check Logs:**
```bash
docker inspect nis2-isms-backend --format='{{json .State.Health}}' | python -m json.tool
```

## 🔒 Sicherheits-Checkliste

Vor Production-Einsatz:

- [ ] SECRET_KEY geändert (min. 32 Zeichen)
- [ ] ADMIN_PASSWORD geändert (stark!)
- [ ] POSTGRES_PASSWORD geändert
- [ ] CORS_ORIGINS auf echte Domain gesetzt
- [ ] HTTPS aktiviert (Reverse Proxy oder SSL-Zertifikate)
- [ ] Firewall konfiguriert (nur Port 80/443 öffentlich)
- [ ] Regelmäßige Backups eingerichtet
- [ ] Container-Updates geplant
- [ ] Logs-Rotation konfiguriert

## 📚 Weiterführende Dokumentation

- [Portainer Documentation](https://docs.portainer.io/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [PostgreSQL Docker](https://hub.docker.com/_/postgres)

## 🆘 Support

Bei Problemen:

1. Prüfen Sie Container-Logs in Portainer
2. Prüfen Sie Health Checks
3. Konsultieren Sie [INSTALLATION.md](INSTALLATION.md)
4. Erstellen Sie ein Issue im Repository

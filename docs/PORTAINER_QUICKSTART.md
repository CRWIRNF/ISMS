# Portainer Stack Deployment - Schnellanleitung

## 🎯 Einfachste Methode: Lokaler Build

Da das Repository auf einem nicht-standard Branch liegt, ist die einfachste Methode:

### Schritt 1: Repository auf Ihren Server klonen

```bash
# Auf Ihrem Server (wo Portainer läuft)
cd /opt  # oder ein anderes Verzeichnis Ihrer Wahl
git clone <REPOSITORY_URL> ISMS
cd ISMS
git checkout claude/nis2-compliance-requirements-011CUoKupKkui9x28zeqpAS2
```

### Schritt 2: Stack in Portainer erstellen

1. Öffnen Sie Portainer
2. Gehen Sie zu **Stacks** → **Add stack**
3. **Name**: `nis2-isms`
4. **Build method**: Wählen Sie **"Upload"**
5. **Upload**: Wählen Sie `docker-compose.prod.yml` aus dem Repository

### Schritt 3: Environment Variables setzen

Fügen Sie diese hinzu (Button "Add an environment variable"):

```
SECRET_KEY=<generieren Sie einen mit: python3 -c "import secrets; print(secrets.token_urlsafe(32))">
ADMIN_PASSWORD=SecurePassword123!
POSTGRES_PASSWORD=DBPassword456!
```

### Schritt 4: Deploy

Klicken Sie auf **"Deploy the stack"**

---

## 🔧 Alternative: Manuell mit Docker Compose

Falls Portainer Probleme macht, können Sie auch direkt mit Docker Compose arbeiten:

```bash
# Auf dem Server
cd /opt/ISMS
git checkout claude/nis2-compliance-requirements-011CUoKupKkui9x28zeqpAS2

# .env erstellen
cp .env.docker .env
nano .env
# Setzen Sie: SECRET_KEY, ADMIN_PASSWORD, POSTGRES_PASSWORD

# Starten
docker-compose -f docker-compose.prod.yml up -d

# Status prüfen
docker-compose -f docker-compose.prod.yml ps

# Logs ansehen
docker-compose -f docker-compose.prod.yml logs -f
```

Dann können Sie den Stack in Portainer importieren:
1. **Stacks** → **Add stack**
2. **Name**: `nis2-isms`
3. **Build method**: Wählen Sie "From existing stack"
4. Wählen Sie den laufenden Stack aus

---

## 📋 Alternative: Images vorab bauen

Wenn Sie die Images vorab bauen und in eine Registry pushen möchten:

```bash
# Backend Image bauen
cd backend
docker build -t localhost:5000/nis2-isms-backend:latest .

# Frontend Image bauen
cd ../frontend
docker build -t localhost:5000/nis2-isms-frontend:latest .

# Optional: In lokale Registry pushen
docker push localhost:5000/nis2-isms-backend:latest
docker push localhost:5000/nis2-isms-frontend:latest
```

Dann in `portainer-stack.yml` die `build:` Zeilen ersetzen durch:
```yaml
backend:
  image: localhost:5000/nis2-isms-backend:latest
  # Entfernen Sie die build: Sektion

frontend:
  image: localhost:5000/nis2-isms-frontend:latest
  # Entfernen Sie die build: Sektion
```

---

## ✅ Empfohlener Workflow für Sie

Da Sie Portainer verwenden, empfehle ich:

**Option A (Einfachst):**
```bash
# Auf dem Server
cd /opt
git clone <IHRE_REPO_URL> ISMS
cd ISMS
git checkout claude/nis2-compliance-requirements-011CUoKupKkui9x28zeqpAS2
cp .env.docker .env
nano .env  # SECRET_KEY, ADMIN_PASSWORD, POSTGRES_PASSWORD setzen
docker-compose -f docker-compose.prod.yml up -d
```

Dann in Portainer: **Stacks** → **Add stack** → **"From existing stack"**

**Option B (Portainer Web Editor):**
1. **Stacks** → **Add stack**
2. **Build method**: "Web editor"
3. Kopieren Sie den Inhalt von `docker-compose.prod.yml`
4. Ersetzen Sie alle `${VARIABLE}` mit echten Werten
5. **Deploy**

---

## 🐛 Warum der Git-Import nicht funktioniert

Der Fehler "reference not found" tritt auf weil:
- Der Branch heißt `claude/nis2-compliance-requirements-011CUoKupKkui9x28zeqpAS2`
- Nicht der Standard-Branch `main` oder `master`
- Portainer kann lange Branch-Namen manchmal nicht richtig verarbeiten

**Lösung**: Verwenden Sie Upload oder Web Editor statt Git-Integration.

---

## 📞 Schnellhilfe

Falls es immer noch nicht klappt, können Sie auch:

1. **Minimaler Test**: Nur PostgreSQL starten
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: test123
    ports:
      - "5432:5432"
```

2. **Images einzeln bauen**:
```bash
cd backend && docker build -t nis2-backend .
cd ../frontend && docker build -t nis2-frontend .
```

3. **In Portainer nur Images verwenden** (ohne build)

Welche Methode möchten Sie ausprobieren?

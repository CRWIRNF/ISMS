# NIS2 ISMS - Portainer Deployment Guide

## Schnellstart für Portainer Stack Editor

### Methode 1: Git Repository (Empfohlen)

1. **Öffnen Sie Portainer Web UI**
   - Navigieren Sie zu: `Stacks` > `+ Add stack`

2. **Stack-Konfiguration**
   - **Name:** `nis2-isms`
   - **Build method:** `Repository`
   - **Repository URL:** Ihre Git-Repository-URL
   - **Repository reference:** `claude/nis2-compliance-requirements-011CUoKupKkui9x28zeqpAS2`
   - **Compose path:** `portainer-stack.yml`

3. **Umgebungsvariablen konfigurieren**
   Klicken Sie auf `+ Add an environment variable` und fügen Sie hinzu:

   **Erforderlich:**
   ```
   SECRET_KEY=IhrSicheresGeheimnis-MindestensXYZ
   ADMIN_PASSWORD=IhrAdminPasswort123!
   ```

   **Optional:**
   ```
   BACKEND_PORT=8000
   FRONTEND_PORT=80
   CORS_ORIGINS=["http://ihre-domain.de","https://ihre-domain.de"]
   ```

4. **Stack deployen**
   - Klicken Sie auf `Deploy the stack`
   - Warten Sie, bis der Build abgeschlossen ist (kann 2-5 Minuten dauern)

5. **Zugriff auf die Anwendung**
   - Frontend: `http://ihr-server:80`
   - Backend API: `http://ihr-server:8000/docs`
   - Login: `admin` / (das von Ihnen gesetzte ADMIN_PASSWORD)

---

### Methode 2: Web Editor (Copy & Paste)

1. **Öffnen Sie Portainer Web UI**
   - Navigieren Sie zu: `Stacks` > `+ Add stack`

2. **Stack-Konfiguration**
   - **Name:** `nis2-isms`
   - **Build method:** `Web editor`

3. **Stack-Datei kopieren**
   - Kopieren Sie den kompletten Inhalt von `portainer-stack.yml`
   - Fügen Sie ihn in den Web Editor ein

4. **Umgebungsvariablen** (siehe Methode 1, Schritt 3)

5. **Stack deployen** (siehe Methode 1, Schritte 4-5)

---

## Umgebungsvariablen - Komplette Liste

### Erforderliche Variablen

| Variable | Beschreibung | Beispiel |
|----------|--------------|----------|
| `SECRET_KEY` | Geheimer Schlüssel für JWT-Tokens (min. 32 Zeichen) | `IhrSicheresGeheimnis123XYZ` |
| `ADMIN_PASSWORD` | Passwort für den Admin-User | `SecurePassword123!` |

### Optionale Variablen

| Variable | Standard | Beschreibung |
|----------|----------|--------------|
| `BACKEND_PORT` | `8000` | Port für Backend API |
| `FRONTEND_PORT` | `80` | Port für Frontend |
| `ADMIN_USERNAME` | `admin` | Admin-Benutzername |
| `ADMIN_EMAIL` | `admin@example.com` | Admin-E-Mail |
| `CORS_ORIGINS` | `["http://localhost:80"]` | Erlaubte Origins für CORS |

### Microsoft Entra ID / Azure AD (SSO)

| Variable | Beschreibung |
|----------|--------------|
| `ENTRA_ENABLED` | `True` aktiviert SSO |
| `ENTRA_TENANT_ID` | Azure AD Tenant ID |
| `ENTRA_CLIENT_ID` | Azure AD Client ID |
| `ENTRA_CLIENT_SECRET` | Azure AD Client Secret |
| `ENTRA_REDIRECT_URI` | Redirect URI (z.B. `https://ihre-domain.de/api/auth/entra/callback`) |

---

## Troubleshooting

### Backend startet nicht (ModuleNotFoundError)
**Problem:** Backend zeigt `ModuleNotFoundError: No module named 'app'`

**Lösung:**
1. Gehen Sie zu: `Stacks` > `nis2-isms` > `Editor`
2. Klicken Sie auf `Update the stack`
3. Aktivieren Sie: `Re-pull image and redeploy`
4. Klicken Sie auf `Update`

### Frontend kann Backend nicht erreichen (502 Bad Gateway)
**Problem:** Nginx zeigt `connect() failed (113: Host is unreachable)`

**Lösung:**
1. Überprüfen Sie Backend-Logs: `Containers` > `nis2-isms-backend` > `Logs`
2. Stellen Sie sicher, dass Backend läuft und gesund ist
3. Prüfen Sie Netzwerk-Konfiguration

### Datenbank wird nicht initialisiert
**Problem:** Keine Admin-User nach Start

**Lösung:**
1. Überprüfen Sie Volume: `Volumes` > `nis2-isms_backend-data`
2. Löschen Sie das Volume und deployen Sie neu (ACHTUNG: Datenverlust!)
3. Überprüfen Sie ADMIN_* Umgebungsvariablen

### Container werden nicht gebaut
**Problem:** Portainer zeigt Build-Fehler

**Lösung:**
1. Stellen Sie sicher, dass Git-Repository öffentlich zugänglich ist
2. Prüfen Sie Branch-Name: `claude/nis2-compliance-requirements-011CUoKupKkui9x28zeqpAS2`
3. Verwenden Sie Web Editor Methode als Alternative

---

## Stack verwalten

### Logs anzeigen
```
Stacks > nis2-isms > Container > [Service] > Logs
```

### Stack neu starten
```
Stacks > nis2-isms > Stop
Stacks > nis2-isms > Start
```

### Stack aktualisieren (nach Code-Änderungen)
```
Stacks > nis2-isms > Editor > Update the stack
☑ Re-pull image and redeploy
☑ Prune services
```

### Stack komplett neu bauen
```
Stacks > nis2-isms > Delete stack
Dann neu deployen (siehe oben)
```

---

## Sicherheitshinweise

⚠️ **WICHTIG für Produktionsumgebungen:**

1. **Ändern Sie unbedingt:**
   - `SECRET_KEY` (generieren Sie einen zufälligen String mit min. 32 Zeichen)
   - `ADMIN_PASSWORD` (verwenden Sie ein starkes Passwort)

2. **CORS korrekt konfigurieren:**
   ```
   CORS_ORIGINS=["https://ihre-domain.de"]
   ```

3. **HTTPS verwenden:**
   - Verwenden Sie einen Reverse Proxy (nginx, Traefik, Caddy)
   - Oder konfigurieren Sie SSL-Zertifikate

4. **Backups:**
   - Sichern Sie regelmäßig das `backend-data` Volume
   - Command: `docker run --rm -v nis2-isms_backend-data:/data -v $(pwd):/backup alpine tar czf /backup/backup.tar.gz /data`

---

## Standard-Zugangsdaten

**Nach erstem Deployment:**
- **Benutzername:** `admin`
- **Passwort:** Wert von `ADMIN_PASSWORD` (Standard: `admin`)

⚠️ **Ändern Sie das Passwort sofort nach dem ersten Login!**

---

## Support

Bei Problemen:
1. Überprüfen Sie die Container-Logs in Portainer
2. Prüfen Sie die Umgebungsvariablen
3. Stellen Sie sicher, dass alle Ports verfügbar sind (80, 8000)
4. Konsultieren Sie die Haupt-Dokumentation im Repository

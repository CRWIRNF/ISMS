# NIS2 Compliance Management System (ISMS)

Ein kostenloses, selbst-gehostetes Information Security Management System (ISMS) für die Erfüllung der NIS2-Richtlinien-Anforderungen.

## 🎯 Funktionen

- ✅ **Vollständiger NIS2-Anforderungskatalog** basierend auf Artikel 21
- 📊 **Umsetzungs-Tracking** für alle Maßnahmen
- 👥 **Benutzerverwaltung** mit Rollen und Berechtigungen
- 🔐 **Lokale Authentifizierung** (JWT-basiert)
- 🌐 **Microsoft Entra Integration** (vorbereitet für Enterprise SSO)
- 📝 **Dokumentationsvorlagen** für Richtlinien und Prozesse
- 🎯 **Risikomanagement** und Incident-Tracking
- 📈 **Reporting und Compliance-Dashboards**
- 🔄 **Audit-Trail** für alle Änderungen
- 🏢 **ISO 27001 Mapping** integriert

## 🚀 Quick Start

### 🐳 Docker/Portainer (Empfohlen)

**Einfachster Weg mit Docker Compose:**

```bash
# .env Datei erstellen
cp .env.docker .env
# WICHTIG: Bearbeiten Sie .env und ändern Sie SECRET_KEY und ADMIN_PASSWORD!

# Container starten
docker-compose up -d

# Zugriff auf die Anwendung
# Frontend: http://localhost
# API Docs: http://localhost:8000/docs
```

**Mit Portainer:**

1. Stack erstellen mit `portainer-stack.yml`
2. Environment Variables setzen (SECRET_KEY, ADMIN_PASSWORD, POSTGRES_PASSWORD)
3. Stack deployen

👉 **Siehe [Docker Deployment Guide](docs/DOCKER_DEPLOYMENT.md) für Details**

### 💻 Manuelle Installation

<details>
<summary>Klicken für manuelle Installation ohne Docker</summary>

#### Voraussetzungen

- Python 3.9+
- Node.js 18+
- Git

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Bearbeiten Sie .env mit Ihren Einstellungen
python -m app.main
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

Die Anwendung ist nun verfügbar unter:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Dokumentation: http://localhost:8000/docs

</details>

### 🔑 Standard-Benutzer

Nach der ersten Installation wird ein Admin-Benutzer erstellt:
- **Benutzername**: admin
- **Passwort**: admin (bitte sofort ändern!)

## 📋 NIS2-Anforderungen

Das System deckt alle 10 Hauptanforderungen nach Artikel 21 ab:

1. **Risikoanalyse und Sicherheitskonzepte**
2. **Bewältigung von Sicherheitsvorfällen**
3. **Aufrechterhaltung des Betriebs** (Backup, DR, Krisenmanagement)
4. **Lieferkettensicherheit**
5. **Sicherheit bei Erwerb, Entwicklung und Wartung**
6. **Prüfung und Bewertung der Wirksamkeit**
7. **Cyberhygiene und Schulungen**
8. **Verschlüsselung und Kryptografie**
9. **Personalsicherheit** (Zugangskontrollen)
10. **Multi-Faktor-Authentifizierung**

## 🔐 Microsoft Entra Integration

Die Microsoft Entra (Azure AD) Integration ist vorbereitet:

1. Erstellen Sie eine Enterprise App in Ihrem Azure AD
2. Konfigurieren Sie die OAuth2/OIDC-Parameter in der `.env`
3. Aktivieren Sie die Entra-Authentifizierung in den Einstellungen

Siehe [docs/ENTRA_SETUP.md](docs/ENTRA_SETUP.md) für Details.

## 📁 Projektstruktur

```
ISMS/
├── backend/          # FastAPI Backend
│   ├── app/
│   │   ├── api/      # API Endpoints
│   │   ├── models/   # Datenbankmodelle
│   │   ├── schemas/  # Pydantic Schemas
│   │   └── core/     # Auth & Security
├── frontend/         # React Frontend
│   └── src/
│       ├── components/
│       ├── pages/
│       └── services/
└── docs/             # Dokumentation
```

## 🛠️ Technologie-Stack

**Backend:**
- FastAPI (Python Web Framework)
- SQLAlchemy (ORM)
- SQLite (Datenbank, erweiterbar auf PostgreSQL)
- JWT (Authentifizierung)
- Pydantic (Validierung)

**Frontend:**
- React 18
- TypeScript
- Vite (Build Tool)
- TailwindCSS (Styling)
- React Router (Navigation)
- Axios (HTTP Client)

## 📖 Dokumentation

- 🐳 [**Docker/Portainer Deployment**](docs/DOCKER_DEPLOYMENT.md) - Empfohlen für Production
- 💻 [Manuelle Installation](docs/INSTALLATION.md)
- 🔐 [Microsoft Entra Setup](docs/ENTRA_SETUP.md)
- 📚 [API Dokumentation](http://localhost:8000/docs) (nach Start verfügbar)

## 🤝 Beitragen

Dieses Projekt wurde erstellt, um eine kostenlose Alternative zu teuren NIS2-Compliance-Tools zu bieten.

## 📄 Lizenz

MIT License - Siehe [LICENSE](LICENSE) für Details.

## ⚠️ Disclaimer

Dieses Tool unterstützt Sie bei der Umsetzung der NIS2-Anforderungen. Es ersetzt jedoch keine professionelle rechtliche oder sicherheitstechnische Beratung. Die Verantwortung für die Compliance liegt beim Nutzer.

## 🆘 Support

Bei Fragen oder Problemen erstellen Sie bitte ein Issue im GitHub Repository.

---

**Version**: 1.0.0
**Status**: In Entwicklung
**Letzte Aktualisierung**: November 2025

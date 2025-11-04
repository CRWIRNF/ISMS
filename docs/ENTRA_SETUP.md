# Microsoft Entra (Azure AD) Integration Setup

Dieses Dokument beschreibt, wie Sie die Microsoft Entra (ehemals Azure AD) Integration für Single Sign-On (SSO) konfigurieren.

## Voraussetzungen

- Microsoft Azure Subscription
- Admin-Zugriff auf Azure Active Directory
- NIS2 ISMS Backend läuft auf einer öffentlich erreichbaren URL

## Schritt 1: Enterprise App in Azure erstellen

1. Melden Sie sich im [Azure Portal](https://portal.azure.com) an
2. Navigieren Sie zu **Azure Active Directory** > **Enterprise Applications**
3. Klicken Sie auf **New application** > **Create your own application**
4. Geben Sie einen Namen ein (z.B. "NIS2 ISMS") und wählen Sie "Integrate any other application you don't find in the gallery"
5. Klicken Sie auf **Create**

## Schritt 2: App Registration konfigurieren

1. Navigieren Sie zu **Azure Active Directory** > **App registrations**
2. Finden Sie Ihre erstellte App oder klicken Sie auf **New registration**
3. Konfigurieren Sie:
   - **Name**: NIS2 ISMS
   - **Supported account types**: Accounts in this organizational directory only
   - **Redirect URI**:
     - Type: Web
     - URI: `http://localhost:8000/api/auth/entra/callback` (für Development)
     - URI: `https://your-domain.com/api/auth/entra/callback` (für Production)

## Schritt 3: Client Secret erstellen

1. In der App Registration, gehen Sie zu **Certificates & secrets**
2. Klicken Sie auf **New client secret**
3. Geben Sie eine Beschreibung ein und wählen Sie eine Ablaufzeit
4. **Wichtig**: Kopieren Sie den Secret-Wert sofort - er wird nur einmal angezeigt!

## Schritt 4: API Permissions konfigurieren

1. Gehen Sie zu **API permissions**
2. Klicken Sie auf **Add a permission** > **Microsoft Graph**
3. Wählen Sie **Delegated permissions**
4. Fügen Sie folgende Permissions hinzu:
   - `User.Read` (Standard)
   - `email`
   - `profile`
   - `openid`
5. Klicken Sie auf **Grant admin consent**

## Schritt 5: Backend-Konfiguration

Tragen Sie die Werte in Ihre `.env` Datei ein:

```env
# Microsoft Entra (Azure AD) Integration
ENTRA_ENABLED=True
ENTRA_TENANT_ID=your-tenant-id-here
ENTRA_CLIENT_ID=your-client-id-here
ENTRA_CLIENT_SECRET=your-client-secret-here
ENTRA_REDIRECT_URI=http://localhost:8000/api/auth/entra/callback
ENTRA_AUTHORITY=https://login.microsoftonline.com/
```

### Werte finden:

- **ENTRA_TENANT_ID**: Azure AD > Overview > Directory (tenant) ID
- **ENTRA_CLIENT_ID**: App Registration > Overview > Application (client) ID
- **ENTRA_CLIENT_SECRET**: Der Wert, den Sie in Schritt 3 kopiert haben

## Schritt 6: Benutzer-Mapping

Wenn ein Benutzer sich zum ersten Mal mit Entra anmeldet, wird automatisch ein Benutzerkonto erstellt:

- **Username**: Wird aus der E-Mail-Adresse generiert
- **Email**: Vom Entra-Profil
- **Full Name**: Vom Entra-Profil
- **Auth Provider**: Wird auf "entra" gesetzt
- **Role**: Standard ist "user" (kann manuell vom Admin geändert werden)

## Schritt 7: Testen

1. Starten Sie das Backend neu
2. Navigieren Sie zu `/api/auth/entra/login`
3. Sie sollten zur Microsoft-Login-Seite weitergeleitet werden
4. Nach erfolgreicher Anmeldung werden Sie zurück zur Anwendung geleitet

## Sicherheitshinweise

- **Production**: Verwenden Sie HTTPS für alle Redirect URIs
- **Client Secret**: Speichern Sie den Secret sicher und rotieren Sie ihn regelmäßig
- **Permissions**: Gewähren Sie nur die minimal notwendigen Berechtigungen
- **Conditional Access**: Erwägen Sie die Konfiguration von Conditional Access Policies in Azure AD

## Troubleshooting

### "AADSTS50011: The reply URL specified does not match"

- Überprüfen Sie, dass die Redirect URI in Azure exakt mit der in `.env` übereinstimmt
- Stellen Sie sicher, dass Sie die URI als "Web" Platform konfiguriert haben

### "AADSTS700016: Application not found in the directory"

- Überprüfen Sie die ENTRA_CLIENT_ID
- Stellen Sie sicher, dass Sie im richtigen Azure AD Tenant sind

### Benutzer kann sich nicht anmelden

- Überprüfen Sie, dass der Benutzer im Azure AD existiert
- Prüfen Sie die API Permissions und Admin Consent
- Schauen Sie in die Backend-Logs für detaillierte Fehlermeldungen

## Erweiterte Konfiguration

### Multi-Tenant Support

Ändern Sie in der App Registration:
- **Supported account types**: Accounts in any organizational directory

### Custom Claims

Sie können zusätzliche Claims in den Token konfigurieren:
1. App Registration > Token configuration
2. Add optional claim
3. Wählen Sie die gewünschten Claims

### Group-based Roles

Um Benutzerrollen basierend auf Azure AD Gruppen zu vergeben:
1. Konfigurieren Sie Group Claims in der App Registration
2. Erweitern Sie den Backend-Code zur Auswertung der Group Claims
3. Mappen Sie Azure AD Gruppen auf ISMS-Rollen

## Support

Bei Fragen zur Microsoft Entra Integration:
- [Microsoft Identity Platform Documentation](https://docs.microsoft.com/en-us/azure/active-directory/develop/)
- [MSAL Python Library](https://github.com/AzureAD/microsoft-authentication-library-for-python)

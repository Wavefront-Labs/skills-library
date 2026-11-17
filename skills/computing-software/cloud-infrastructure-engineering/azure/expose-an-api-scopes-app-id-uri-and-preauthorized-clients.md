---
id: computing-software.cloud-infrastructure-engineering.azure.expose-an-api-scopes-app-id-uri-and-preauthorized-clients
name: expose-an-api-scopes-app-id-uri-and-preauthorized-clients
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, app-registrations, expose-api, oauth2-scopes, app-id-uri, preauthorized-applications, token-validation]
level: practitioner
status: docs-checked
description: "Protect your own API with Entra ID: Application ID URI, delegated scopes, app roles for daemons, pre-authorised clients, and what the API must validate."
sources: ["https://learn.microsoft.com/entra/identity-platform/quickstart-configure-app-expose-web-apis", "https://learn.microsoft.com/entra/identity-platform/scopes-oidc", "https://learn.microsoft.com/entra/identity-platform/access-tokens"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Expose an API: scopes, App ID URI, pre-authorised clients

**Goal:** a web API registration that clients can request tokens for, with least-privilege permissions.

## 1. Application ID URI
Default `api://<appId>` (the App ID URI is the prefix of the scopes your API code references and must be globally unique).
```bash
az ad app update --id <apiAppId> --identifier-uris "api://<apiAppId>"
```

## 2. Delegated scopes (user present)
Expose an API > Add a scope: value `Orders.Read`, who can consent Admins/Admins and users, display strings.
Graph/manifest shape:
```json
"api": { "requestedAccessTokenVersion": 2,
  "oauth2PermissionScopes": [ { "id": "<new-guid>", "value": "Orders.Read", "type": "User", "isEnabled": true,
    "adminConsentDisplayName": "Read orders", "adminConsentDescription": "Read orders on behalf of the user",
    "userConsentDisplayName": "Read your orders", "userConsentDescription": "Read your orders" } ] }
```
Clients request `api://<apiAppId>/Orders.Read`.

## 3. App roles (daemon / app-only)
Define app roles with `allowedMemberTypes: ["Application"]` (e.g. `Orders.ReadWrite.All`), grant them to the client
app (API permissions > Application permissions > admin consent). Daemon requests `api://<apiAppId>/.default`;
the token has `roles`, not `scp`.

## 4. Pre-authorised clients
Expose an API > Authorized client applications: add your SPA/mobile client ID for specific scopes - users are not
prompted to consent for your first-party front end.

## 5. API-side validation
- Signature via OIDC metadata keys; `iss` = `https://login.microsoftonline.com/<tid>/v2.0` (v2) for allowed tenants.
- `aud` = API client ID (v2) or App ID URI (v1).
- Delegated: required scope in `scp`; app-only: required role in `roles`; delegated tokens carry `scp`, app-only tokens carry `roles`.
- Use Microsoft.Identity.Web / MSAL-compatible middleware rather than hand-rolled validation.

## Gotchas
- Disable a scope (`isEnabled: false`) and save before deleting it.
- Set `requestedAccessTokenVersion: 2` and validate issuer and audience for the matching token version.

## Verify
- [ ] Token from the client shows correct `aud`, `scp`/`roles`; API returns 403 for a token missing the scope.

## Checked
2026-10-28. Confirmed on the Learn expose-a-web-api quickstart: Application ID URI defaults to api://<client-id>, must be globally unique, Authorized client applications. check_commands confirmed `az ad app update --id --identifier-uris`. Removed: verified-domain example, `idtyp`, the /.default mixing rule and the 401 ranking claim (not on fetched pages).
Method: documentation only; no commands were run.

---
id: computing-software.ai-ml-engineering.open-webui.enable-scim-provisioning
name: enable-scim-provisioning
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [ldap-scim, scim, provisioning, okta, externalid, open-webui]
level: advanced
status: docs-checked
description: "Enable SCIM 2.0 user and group provisioning in Open WebUI with SCIM_ENABLED, SCIM_TOKEN and SCIM_AUTH_PROVIDER, and test the endpoints with curl."
sources:
  - https://docs.openwebui.com/features/authentication-access/auth/scim
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: let Okta, Azure AD or Google Workspace create, update and deactivate users and groups automatically.

## Configure (env vars only, no UI)
```bash
export SCIM_ENABLED=true
export SCIM_TOKEN="$(openssl rand -base64 32)"
export SCIM_AUTH_PROVIDER="microsoft"   # or oidc; required for externalId
```
Without `SCIM_AUTH_PROVIDER`, any create/lookup/update needing `externalId` returns 500 and startup logs a warning.

## IdP settings
Base URL `https://your-domain.com/api/v1/scim/v2/`, Bearer token auth (`Authorization: Bearer <SCIM_TOKEN>`). In Okta: SCIM connector base URL, authentication "HTTP Header".

## Behaviour
- Endpoints: Users and Groups with POST, GET, PUT, PATCH, DELETE and list. Filters `eq ne co sw ew pr gt ge lt le`, e.g. `Users?filter=userName eq "user@example.com"`, `filter=externalId eq "abc-123"`.
- PATCH ops add/replace/remove; actionable paths: `userName`, `displayName`, `name.formatted`, `emails[primary eq true].value`, `active`, `externalId`. Others return `invalidPath`; remove on anything but `externalId` returns `mutability`; all operations are validated before anything is written.
- `userName` must be the email. externalId is stored per provider in the user's `scim` JSON field and falls back to matching OAuth `sub` for linking.
- `active:false` sets role `pending` (live WebSocket connections end), `true` sets `user`. Admins keep their role.
- Only externally provisioned accounts (via SCIM or OAuth/OIDC) are visible; locally created ones (first admin) answer 404. DELETE on a visible admin returns 403.
- Group members must be existing users, else the whole request fails with 400 `invalidValue`. SCIM groups start top level; admin-set parents persist.
- SCIM users get a random unknown password; they sign in through SSO.

## Test
```bash
curl -H "Authorization: Bearer $SCIM_TOKEN" https://your-domain.com/api/v1/scim/v2/Users
curl -X POST -H "Authorization: Bearer $SCIM_TOKEN" -H "Content-Type: application/scim+json" \
 -d '{"schemas":["urn:ietf:params:scim:schemas:core:2.0:User"],"userName":"test@example.com","externalId":"idp-user-id-123","emails":[{"value":"test@example.com","primary":true}],"active":true}' \
 https://your-domain.com/api/v1/scim/v2/Users
```

## Troubleshooting and limits
401: `SCIM_ENABLED` unset or token mismatch. 404: missing `/api/v1` prefix. Creation failure: bad email or duplicate email/externalId. Not supported: custom schema extensions, bulk operations, ETags. Use HTTPS, rotate the token, consider IP allowlisting; pair with OIDC for login.

## Checked
2026-11-04. Confirmed against the Open WebUI docs page features/authentication-access/auth/scim (read in full): env-only configuration and the three variables, openssl token generation, the 500 error and startup warning without SCIM_AUTH_PROVIDER, base URL and bearer auth, the Okta steps, user and group operations, filter examples and operators, PATCH paths and the error codes, userName as email, per-provider externalId storage and OAuth sub fallback, active mapping to pending/user with live WebSocket end, visibility of externally provisioned accounts only, admin DELETE 403, group member 400 invalidValue, top-level groups, random SSO passwords, the troubleshooting list, security notes and limitations. Corrected: Entra was not named on the page (it says Azure AD) and okta was not a documented SCIM_AUTH_PROVIDER value.
Method: documentation only; no commands were run.

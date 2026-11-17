---
id: computing-software.ai-ml-engineering.open-webui.issue-and-restrict-api-keys
name: issue-and-restrict-api-keys
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [api-keys-mfa, api-keys, service-accounts, bearer-token, endpoint-restrictions, open-webui]
level: practitioner
status: docs-checked
description: "Enable API keys in Open WebUI, grant the permission, create or rotate keys, restrict routes and handle gateways that consume the Authorization header."
sources:
  - https://docs.openwebui.com/features/authentication-access/api-keys
  - https://docs.openwebui.com/features/authentication-access/mfa
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: give scripts and integrations a revocable credential.

## Enable
1. Admin: Settings > Admin > Authentication > toggle **API Keys** > Save (env `ENABLE_API_KEYS`). Off means nobody (admins included) can create or use keys and existing keys stop working.
2. Non-admins need Features permission **API Keys** (`USER_PERMISSIONS_FEATURES_API_KEYS`), via Default Permissions or better a dedicated "API Users" group. Admins need only the global toggle.
3. Optional **API Key Endpoint Restrictions**: comma-separated allowlist, e.g. `/api/v1/models,/api/v1/chat/completions`. A path matches exactly or as a segment prefix. It applies instance-wide to all keys.

## Create
Profile > Settings > Account > API keys > **Show** next to Secrets > **Create new secret key**. Keys look like `sk-` plus 32 hex chars. Each account has exactly ONE key; creating a new one replaces the old immediately. The section is collapsed by default, so an apparently empty section just needs Show.

## Use
```bash
curl -H "Authorization: Bearer sk-..." http://localhost:8080/api/models
```
Behind a gateway that consumes `Authorization`, send the key in the custom header instead (default `x-api-key`, rename with `CUSTOM_API_KEY_HEADER`, e.g. `X-OpenWebUI-Key`). Lookup order: Bearer header, `token` cookie, custom header.

## Admin rotation
Admin Panel > Users > user edit dialog: **Rotate** (shows the new key once; needs the global toggle on) or **Delete** (works even with keys disabled). Scripted with an admin key: `POST /api/v1/users/{user_id}/api_key/rotate`, `DELETE /api/v1/users/{user_id}/api_key`. Only the primary admin changes the primary admin's key.

## Practices
One non-admin service account per integration (`monitoring-bot`, `ci-pipeline`) so you can revoke one without breaking others. Keys act as the owner with the owner's role and groups, re-checked on every request. Audit log records requests under the key owner.

## Troubleshooting
- 401: wrong format (`Bearer sk-...`), key replaced, or account pending/missing.
- 403: global toggle off, owner lost the permission, or route not in the allowlist.
- No API keys section: global toggle or permission missing.

## Limits
No per-key scopes, no expiry, no multiple keys per account. MFA does not block keys.

## Checked
2026-11-04. Confirmed against the Open WebUI docs page features/authentication-access/api-keys (read in full): the global toggle and its effect, the non-admin permission and Default Permissions versus group routes, endpoint restrictions and prefix matching, the create steps and collapsed section, one key per account, key format, Bearer use, the custom header with its default and lookup order, admin Rotate and Delete with both endpoints and the primary admin rule, service account practice, the 401 and 403 lists and the limits. The MFA does not block keys line is on features/authentication-access/mfa (read in full earlier, API keys are unaffected), which is now listed in sources.
Method: documentation only; no commands were run.

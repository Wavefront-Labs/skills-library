---
id: computing-software.cloud-infrastructure-engineering.datadog.api-app-keys-rbac
name: api-app-keys-rbac
category: computing-software
field: cloud-infrastructure-engineering
product: datadog
tags: [datadog, api-keys, application-keys, rbac, roles]
level: practitioner
status: docs-checked
description: "Manage Datadog API keys, application keys, scopes and roles, and rotate credentials safely."
sources: ["https://docs.datadoghq.com/account_management/api-app-keys/", "https://docs.datadoghq.com/account_management/rbac/", "https://docs.datadoghq.com/account_management/rbac/permissions/", "https://docs.datadoghq.com/account_management/rbac/granular_access/", "https://docs.datadoghq.com/account_management/scim/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API keys, application keys and RBAC
Goal: least-privilege access to Datadog.

```
# API key: identifies the org for submitting data (Agent, DogStatsD, API submit)
# Application key: used with an API key to read or change data through the API

curl -s -H "DD-API-KEY: <DD_API_KEY>" "https://api.datadoghq.com/api/v1/validate"
```

- Check an API key with `/api/v1/validate` and an application key with `/api/v2/validate_keys` (key pair).
- Application keys can be scoped to minimal privileges. Without scopes a key has all the permissions of its creator, so scope keys.
- Application keys are not transferred between users; share via a service account instead. Disabling a user revokes their application keys but not the API keys they created.
- Managed roles: Datadog Admin, Datadog Standard and Datadog Read Only. Clone one to make a custom role; only users with User Access Manage can create or edit roles. When you give a user a custom role, remove their managed role to enforce it.
- Restrict individual resources by role, Team or user with granular access control.
- SCIM provisioning is documented for Entra ID and Okta (plan-limited).
- Rotate with several API keys: create the new key, deploy it, then revoke the old one. A revoked API key can be restored for 7 days; a revoked application key cannot.
- By default an org can hold up to 50 API keys.
- Store keys in a secrets manager, not in source or env files.

Gotcha: API keys cannot send data from browser or mobile apps because they would be exposed client-side; use client tokens (Organization Settings > Client Tokens). If a key leaks, revoke it and review the docs' compromised-key steps.

## Verify
- The validate endpoints report the key as valid, and the key list shows a Last used timestamp.

## Checked
2026-11-09. Confirmed against the API and application keys page (validate endpoints, scopes, 7-day API key restore, 50-key default, client tokens, secrets manager advice, service accounts, disabled-user behaviour, Last used), RBAC and permissions pages (three managed roles, custom roles, User Access Manage, clone, remove managed role), granular access page (restrict by role, Team, user) and the SCIM page (Entra ID, Okta). Removed: SAML/SSO and MFA-at-IdP claims, "Datadog's key audit", the example `{"valid": true}` response, and the per-user last-used refresh claim beyond the documented Last used timestamp.
Method: documentation only; no commands were run.

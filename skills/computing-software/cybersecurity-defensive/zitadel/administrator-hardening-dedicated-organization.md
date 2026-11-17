---
id: computing-software.cybersecurity-defensive.zitadel.administrator-hardening-dedicated-organization
name: administrator-hardening-dedicated-organization
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, hardening, administrators, break-glass, login-client, security]
level: advanced
status: docs-checked
description: "Isolate instance administrators, the login client and break-glass access in a dedicated organization so organization admins cannot reach them."
sources:
  - https://zitadel.com/docs/guides/manage/console/administrator-hardening
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Instance administrators (`IAM_*` roles) manage every organization. Organization administrators (`ORG_*` roles) manage one. When both kinds share an organization, their scopes overlap and organization administrators can influence how instance administrators log in, which can lead to unexpected account takeover.

Create a dedicated organization reserved for instance administrators and automation. The documented layout:

```text
Instance
  Dedicated organization (instance administrators only)
    Break-glass IAM_OWNER service account (PAT, offline storage)
    Login client service account (IAM_LOGIN_CLIENT only)
    Other instance automation service accounts
  Customer or application organizations
    End users and ORG_* administrators only
```

Why it matters:

- Login behavior and security, password complexity, expiry and lockout can be overridden per organization. Organization admins of the shared organization could weaken MFA, passkeys or external IdPs for instance administrators.
- Auditing who is an administrator stays clean, because customers and platform staff are not mixed in one user list.

The organization created at setup may serve as the dedicated one only if it hosts no customer users and no organization administrators manage it on behalf of customers. Otherwise create a separate one.

Keep the break-glass personal access token in offline storage.

## Checked
2026-11-08. Confirmed against the ZITADEL guide Hardening instance administrators: IAM_ and ORG_ scopes, dedicated organization layout, per-organization login settings overriding, default organization caveat, break-glass PAT stored offline.
Method: documentation only; no commands were run.

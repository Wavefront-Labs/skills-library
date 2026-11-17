---
id: computing-software.web-development.strapi.sso-settings
name: sso-settings
category: computing-software
field: web-development
product: strapi
tags: [strapi, sso, single-sign-on, auto-registration, default-role, lockout]
level: practitioner
status: docs-checked
description: "Strapi admin SSO settings: auto-registration, default role, local authentication lock-out, and the Super Admin lockout trap."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/features/sso.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Single Sign-On (admin panel)

General settings are in the admin panel (Global settings > Single Sign-On); additional SSO providers are configured in code.

| Setting | Effect |
|---|---|
| Auto-registration | True: an SSO login that matches no administrator creates a new one. False: admins must be created manually beforehand |
| Default role | role given to auto-registered administrators |
| Local authentication lock-out | roles whose local login is disabled; they must use SSO and cannot change or reset a password |

Click **Save**. Changes are recorded in Audit Logs.

## Trap
Don't select Super Admin in the lock-out list. If selected, you can accidentally lock yourself out of the admin panel entirely, and if the Super Admin cannot log in, the only way back is to temporarily disable the SSO feature entirely, log in with username and password, remove Super Admin from the lock-out list, then re-enable SSO.

SSO is an Enterprise feature (CMS Enterprise plan, or the SSO add-on with the CMS Growth plan) and is disabled by default. Provider setup lives in code in the `/config/admin` file.

## Checked

2026-11-04: checked against the Strapi docs page Single Sign-On (features/sso). Confirmed: path, the three settings and their effects, Save, Audit Logs, the Super Admin lock-out warning and recovery steps, plan and default activation, provider configuration in `/config/admin`. Removed: the unsupported claim that admin accounts can still be created from the CLI. Replaced: the vague 'page continues' note with the recovery procedure from the page.

Method: documentation only; no commands were run.

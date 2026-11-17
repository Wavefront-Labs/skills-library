---
id: computing-software.web-development.strapi.admin-tokens
name: admin-tokens
category: computing-software
field: web-development
product: strapi
tags: [strapi, admin-token, automation, admin-api, permissions, ci]
level: advanced
status: docs-checked
description: "Strapi admin tokens for programmatic Admin API access: scoped to the owner's permissions, ownership rules, one-time key display."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/features/admin-tokens.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Admin tokens

Authenticate automated clients (MCP agents, CI/CD, scripts) against the Admin API. Separate from API tokens; each is rejected on the other's routes. Path: Settings > Administration Panel > Admin Tokens.

Activated by default for Super Admin; each lower role needs an explicit permission grant. Creating one needs permission to access the Admin tokens page and to generate tokens.

Form: name, optional description, duration (7 days, 30 days, 90 days, Unlimited), then tabs of permission checkboxes. Permissions the creator does not hold are disabled; role conditions are shown read-only and apply automatically.

## Rules
- The plaintext key is shown once, after creation or regeneration. `admin.secrets.encryptionKey` (which makes Content API token keys viewable) does not apply to admin tokens.
- Stored in the same table as API tokens (a `kind` field differentiates) but managed on independent pages.
- Anyone with page access can view tokens; only the owner or a super-admin can edit or delete.
- Removing a permission from a role deletes it from admin tokens owned by that role's users.
- If the owner's account is deleted, all their admin tokens are deleted with no recovery.
- A shared salt and encryption key apply to all token kinds; the salt is set via `apiToken.salt` (see `computing-software.web-development.strapi.api-tokens`).

## Checked

2026-11-04: checked against the Strapi docs page Admin tokens (features/admin-tokens). Confirmed: purpose, separation from API tokens, default activation for Super Admin, creation prerequisites, duration options, disabled permissions and read-only role conditions, one-time key display, shared table with a `kind` field, view/edit/delete rules, permission removal and owner deletion behaviour, shared `apiToken.salt`. Removed: nothing.

Method: documentation only; no commands were run.

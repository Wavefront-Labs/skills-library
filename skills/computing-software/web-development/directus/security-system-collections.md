---
id: computing-software.web-development.directus.security-system-collections
name: security-system-collections
category: computing-software
field: web-development
product: directus
tags: [security-system-collections, privilege-escalation, flows-hardening, sensitive-read-access]
level: advanced
status: docs-checked
description: "Harden a Directus project by restricting non-admin access to system collections such as flows, settings, users, permissions, sessions and shares."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/14.security/1.best-practices.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Grant create, update and delete to administrators only on:
- `directus_flows`, `directus_operations` (flows can run scripts and mutate any data)
- `directus_settings` (theming CSS injection, email links, auth policy; read also exposes AI provider API keys, so scope read fields)
- `directus_users`, `directus_roles`, `directus_policies`, `directus_permissions` (privilege escalation)
- `directus_extensions` (update), and `directus_fields`, `directus_collections`, `directus_relations`

Safer patterns:
- Profile editing: scope update with `id = $CURRENT_USER` and remove `role` and `policies` from field permissions.
- If a role may create users, set a field preset locking `role` to a non-admin value.
- Treat Webhook flow URLs as public endpoints: require a token or shared secret and validate the payload. Audit any Run Script operation.
- Keep `MARKETPLACE_TRUST` at the default `sandbox`; ship extensions through deployment, not the Studio.

Read access to restrict: `directus_activity` (IPs, behaviour; or rule `user = $CURRENT_USER`), `directus_revisions` and `directus_versions` (snapshots bypass source permissions), `directus_sessions` and `directus_shares` (tokens; admins only).

Gotcha: editors using content versioning need create, update and delete on `directus_versions`; avoid item rules on its update permission.

## Checked

2026-11-04: each system collection restriction, the profile-editing and role-preset patterns, webhook and Run Script cautions, MARKETPLACE_TRUST default sandbox, read-access audit list and the content versioning gotcha confirmed against the Directus Security Best Practices page. Removed a Verify line the page does not state.

Method: documentation only; no commands were run.

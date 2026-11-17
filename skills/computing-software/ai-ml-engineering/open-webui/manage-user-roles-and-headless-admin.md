---
id: computing-software.ai-ml-engineering.open-webui.manage-user-roles-and-headless-admin
name: manage-user-roles-and-headless-admin
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [rbac, roles, admin, headless-admin, default-user-role, sign-out-all-devices, open-webui]
level: practitioner
status: docs-checked
description: "Set default roles, bootstrap the admin account from env vars, change roles and sign a user out of every device in Open WebUI."
sources:
  - https://docs.openwebui.com/features/authentication-access/rbac/roles
  - https://docs.openwebui.com/features/authentication-access/rbac/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: control who is admin, what new sign-ups become, and how to cut a user off.

## Roles
- `admin`: superuser, bypasses most permission checks (effectively `check_permission() == True`).
- `user`: subject to RBAC permissions; nothing is implicit.
- `pending`: zero access until an admin promotes them. Pending accounts are refused on every API request and the WebSocket handshake.

## Default role for new sign-ups
```bash
DEFAULT_USER_ROLE=pending   # pending | user | admin
```
Use `pending` on public/shared instances. The very first account on a fresh install is always `admin` (the "primary administrator" = the earliest-created account; the UI and backend refuse to delete it, but this is a safeguard, not a security boundary).

## Headless admin (CI/CD, Kubernetes)
Set `WEBUI_ADMIN_EMAIL`, `WEBUI_ADMIN_PASSWORD` and optionally `WEBUI_ADMIN_NAME` (defaults to "Admin"). On startup, if the user table is empty, the admin is created with a hashed password and `ENABLE_SIGNUP=False` is applied automatically. If any user already exists, the variables are ignored; restarts never modify the account.
```yaml
environment:
  - WEBUI_ADMIN_EMAIL=admin@example.com
  - WEBUI_ADMIN_PASSWORD=${ADMIN_PASSWORD}   # inject from a secret, never hardcode
  - WEBUI_ADMIN_NAME=System Administrator
```
Re-enable sign-up later in Settings > Admin > General if needed.

## Change a role
Admin Panel > Users. A role change (UI, SCIM sync, OAuth role management, trusted role header) closes that user's live WebSocket connections so they reconnect under the new role; REST calls read the account from the database each request. It does NOT revoke the token, so a demoted user stays signed in (except `pending`, which is locked out).

## Sign out all devices
Open the user in Admin Panel > Users, click **Sign out all devices** at the bottom of the edit dialog, confirm. Works without Redis (stored in the database). Setting a new password in that dialog also signs them out everywhere. Scripted: `POST /api/v1/users/{user_id}/sessions/revoke` with an admin API key; logged as event `auth.sessions_revoked`.

## Gotchas
- API keys remain active after sign-out; delete or rotate the key separately.
- Only the primary administrator can sign themselves out this way.
- `ENABLE_ADMIN_CHAT_ACCESS=False` only hides chats in the UI. With `BYPASS_ADMIN_ACCESS_CONTROL` disabled, admins are checked against access grants like everyone else; private workspace items then show only to owner and grantees. Admin-configured connections with no grants stay admin-only.
- Recommended: put admins in a Group too so future permission changes can be granted to them.

## Checked
2026-11-04. Confirmed against the Open WebUI docs page features/authentication-access/rbac/roles (read in full): the three roles and the admin check_permission note, DEFAULT_USER_ROLE options and the pending recommendation, the first-account admin rule and the primary administrator safeguard, headless admin variables and behaviour (empty user table only, hashing, ENABLE_SIGNUP disabled, ignored afterwards), the role change routes closing WebSocket connections without revoking the token, pending lockout, Sign out all devices behaviour with the database store, API keys staying active, the primary admin rule, the session revoke endpoint and the auth.sessions_revoked event, and the admin limitations. Trimmed the phrase either way, which the page ties to BYPASS_ADMIN_ACCESS_CONTROL being disabled.
Method: documentation only; no commands were run.

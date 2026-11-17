---
id: computing-software.web-development.ghost.ghost-admin-api-authentication-methods
name: ghost-admin-api-authentication-methods
category: computing-software
field: web-development
product: ghost
tags: [ghost, admin-api, authentication, integration-token, staff-token, session]
level: advanced
status: docs-checked
description: "Choose among Ghost Admin API authentication methods: integration token, staff access token and user session, with permission differences."
sources:
  - https://github.com/TryGhost/docs/blob/main/admin-api.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: pick the right Admin API credential.

Three methods exist:
1. Integration token authentication: for integrations that handle common workflows such as publishing content or sharing it elsewhere. You authenticate as the integration, which has its own API keys and webhooks and a fixed set of permissions (for example `GET /users/`, `POST /posts/`). The key is secret, so use it only server side.
2. Staff access token authentication: a token from a user's settings page. You act as that user with their role-based permissions, without sharing a password. It is used the same way as an integration token.
3. User authentication: email and password swapped via the session API for a cookie-based session. Intended for full clients where different users log in; it must support second factor codes and is safe in the browser if passwords are entered securely.

Permissions: Owner or Admin roles reach the full endpoint set. Staff tokens cannot transfer ownership or delete all content. Many endpoints can be found by watching requests Ghost Admin makes, but only the documented ones are considered stable.

The JavaScript Admin client supports integration and staff-token authentication.

Verify: a GET to a documented endpoint such as `GET /admin/posts/` with your credential succeeds.

## Checked

2026-11-04. Confirmed: the three authentication methods, who each is for, the fixed integration permissions, the Owner/Admin note and the two staff-token exceptions (Admin API overview page). Removed: the "missing permission returns 403" outcome, which no page states.

Method: documentation only; no commands were run.

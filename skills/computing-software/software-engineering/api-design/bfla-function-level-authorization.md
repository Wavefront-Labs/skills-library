---
id: computing-software.software-engineering.api-design.bfla-function-level-authorization
name: bfla-function-level-authorization
category: computing-software
field: software-engineering
product: api-design
tags: [api-design, bfla, function-level-authorization, owasp-api-top-10, rbac, api-security, admin-endpoints]
level: practitioner
status: docs-checked
description: "Stop broken function level authorization (OWASP API5:2023): deny by default, gate admin and mutating operations by role, and test low-privilege access."
sources: ["https://owasp.org/API-Security/editions/2023/en/0xa5-broken-function-level-authorization/", "https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Broken function level authorization (BFLA)

Where BOLA is "wrong object", BFLA (OWASP API5:2023) is "wrong operation": a regular user calls an admin-only or state-changing endpoint, often by switching the HTTP method (GET allowed, DELETE not checked) or by guessing a URL such as `/api/v1/users/export_all`.

## Controls
1. Use one consistent, easy-to-analyse authorization module invoked from all business functions (OWASP notes this is often an external component). It denies all access by default and requires explicit grants to specific roles for every function.
2. Make administrative controllers inherit from an administrative base controller that checks the user's group or role; administrative functions inside a regular controller need the same group/role check.
3. Declare the requirement beside the route so it is reviewable, for example in OpenAPI (the scheme name `oauth2` must be defined under `components.securitySchemes`):
```yaml
paths:
  /users/{id}:
    delete:
      security: [{ oauth2: ["users:delete"] }]
```
4. Do not assume an endpoint is regular or admin-only from its URL path: admin endpoints often sit under the same paths as regular ones (for example `/api/users`), not only under `/api/admins`.
5. Treat methods separately; test every method on every path, since changing GET to DELETE is a standard probe.
6. Review endpoints against the application's business logic and its group hierarchy (sub-users, users with more than one role make checks easy to get wrong).

## Gotchas
- OWASP scenario #1: `GET /api/invites/{id}` was allowed, but `POST /api/invites/new` (admin only) had no check, letting an attacker issue an invite with the admin role.
- Role checks added to the "main" controller but not to export, bulk or older-version routes.
- Scopes that are too coarse (`write`) make function-level separation impossible; see the oauth2-scopes skill.

Verify: with a low-privilege token, iterate every operation in the OpenAPI file (all methods) and assert 403/404 for each operation not granted to that role; fail CI when a route lacks a `security` requirement.

## Checked
2026-11-08. Read in full: OWASP API Security Top 10 2023 page API5 (vulnerability questions, both scenarios, prevention list). The Authorization Cheat Sheet was not used for any claim kept here. Removed unsupported items: keeping admin APIs on a separate host or gateway route, `X-HTTP-Method-Override` testing, and the unsigned-client-header gotcha. The OpenAPI snippet was not validated against the spec.
Method: documentation only; no commands were run.

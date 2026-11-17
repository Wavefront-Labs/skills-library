---
id: computing-software.cloud-infrastructure-engineering.zot.authentication-priority-order
name: authentication-priority-order
category: computing-software
field: cloud-infrastructure-engineering
product: zot
tags: [zot, auth-priority, authorization-header, session-auth, anonymous-access, request-flow]
level: advanced
status: docs-checked
description: "The order in which Zot evaluates authentication methods per request, from basic auth through session and mTLS to anonymous, and what fails early."
sources:
  - https://raw.githubusercontent.com/project-zot/project-zot.github.io/main/docs/articles/authn-authz.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Zot evaluates request authentication in this order:

1. Basic auth, if an `Authorization` header is present and basic auth is enabled.
2. The request fails if an `Authorization` header is present but basic auth is disabled.
3. Session auth for the web UI.
4. mTLS, if enabled and client certificates are present.
5. Allowed, if no authentication is configured at all.
6. Allowed for anonymous access or management endpoints.

Related facts:
- With OIDC bearer alongside `cert` or `awsSecretsManager`, Zot tries OIDC first, then traditional bearer.
- With htpasswd and LDAP both configured, htpasswd is checked first.
- If authentication is not configured, anyone can use the API.
- `failDelay` adds a wait before reporting denied authentication.
- Authorization then runs per repository, user and action; unauthenticated requests to admin routes get `401`, non-matching identities `403`.

Use this to debug why a request is treated as anonymous or rejected: check whether a stray `Authorization` header is present while basic auth is off.

## Checked

2026-11-04. Read against the zot authn-authz article (combining mTLS, failDelay, admin-only routes sections); every remaining claim found there. Removed: nothing.

Method: documentation only; no commands were run.

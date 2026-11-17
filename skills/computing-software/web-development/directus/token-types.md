---
id: computing-software.web-development.directus.token-types
name: token-types
category: computing-software
field: web-development
product: directus
tags: [token-types, static-token, session-token, external-jwt]
level: practitioner
status: docs-checked
description: "Choose between Directus standard, session, static and external JWT access tokens, how each is stored, and how to send them on requests."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/03.auth/1.tokens-cookies.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Tokens are scoped to a user and carry that user's permissions.

- **Standard**: returned on login with an expiry and a longer-lived refresh token. Store it, check expiry before each use, refresh when needed. Logging out invalidates the refresh token.
- **Session**: access and refresh combined in one token, stored as a cookie, refreshable only before it expires. Log in with `mode: session` and the browser gets an `httpOnly` `directus_session_token` cookie that JavaScript cannot read.
- **Static**: one non-expiring token per user, generated on the user page. It is stored in plain text in `directus_users`. The Studio warns that after you save and leave the page the token cannot be viewed again, so copy it first.
- **External**: configure Directus to validate JWTs from your own auth system, useful for machine-to-machine access.

Sending a token:
- `Authorization: Bearer <token>` header (preferred)
- session cookie, automatic for the same domain
- `?access_token=<token>` query parameter; it can leak into logs, so avoid it if possible

## Checked

2026-11-04: the four token types, JSON and cookie storage, httpOnly directus_session_token cookie, static token storage in plain text in directus_users, and the three ways to send a token with the query parameter caution confirmed against the Directus Access Tokens page. Removed a Verify line the page does not state.

Method: documentation only; no commands were run.

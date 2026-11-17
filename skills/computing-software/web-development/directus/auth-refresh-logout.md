---
id: computing-software.web-development.directus.auth-refresh-logout
name: auth-refresh-logout
category: computing-software
field: web-development
product: directus
tags: [token-refresh, auth-logout, session-cookie-login, auth-otp]
level: practitioner
status: docs-checked
description: "Log in with JSON or session mode, refresh tokens via /auth/refresh, log out via /auth/logout, and pass an otp when two-factor auth is on."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/03.auth/4.email-login.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Login: `POST /auth/login` with `email` and `password`. If the user has 2FA, add `otp`. Add `"mode": "session"` to receive a session cookie; then the token is not in the JSON response.

Refresh: `POST /auth/refresh` with `{ "refresh_token": "..." }`. For cookie modes you do not send the refresh token but must set `mode` (`session` or `cookie`); the refresh token otherwise comes in JSON or an `httpOnly` cookie.

Logout: `POST /auth/logout` with `{ "refresh_token": "..." }` invalidates it and destroys the session. For a cookie, send `{ "mode": "session" }` to delete it immediately.

SDK:

```js
const client = createDirectus(url).with(authentication()).with(rest());
await client.logout();
await client.request(refresh({ mode: 'json', refresh_token }));
```

GraphQL equivalents: `auth_refresh(refresh_token:)`, `auth_logout(refresh_token:)` or `auth_logout(mode: "session")`.

Gotcha: users must exist first (Studio, invite or Users API).

## Checked

2026-11-04: login with otp and mode session, refresh in JSON and cookie modes, logout with refresh_token or mode session, the SDK and GraphQL calls, and the requirement that the user must already exist confirmed against the Directus Email Login page. Removed a Verify line the page does not state.

Method: documentation only; no commands were run.

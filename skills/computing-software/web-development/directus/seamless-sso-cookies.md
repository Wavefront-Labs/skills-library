---
id: computing-software.web-development.directus.seamless-sso-cookies
name: seamless-sso-cookies
category: computing-software
field: web-development
product: directus
tags: [seamless-sso, session-cookie-domain, redirect-allow-list, cross-domain-cookie]
level: advanced
status: docs-checked
description: "Implement Directus seamless SSO with session mode cross-domain cookies, a provider login link with redirect, a refresh call, and the redirect allow list."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/03.auth/7.sso/2.seamless.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: log users in via an external provider without them seeing the Directus login page.

Env (replace the provider name and domain):

```sh
AUTH_<PROVIDER>_MODE="session"
SESSION_COOKIE_DOMAIN="directus.myserver.com"
SESSION_COOKIE_SECURE="true"
SESSION_COOKIE_SAME_SITE="None"
```

Login link on the client:

```html
<a href="https://directus.myserver.com/auth/login/google?redirect=https://client.myserver.com/login">Login</a>
```

On the client's redirect page call refresh with credentials:

```js
await fetch("https://directus.myserver.com/auth/refresh", {
  method: "POST", credentials: "include",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ mode: "session" }),
});
```

SDK: `authentication("session", { credentials: "include" })` then `client.refresh()`.

Gotchas:
- Add the client origin to `AUTH_<PROVIDER>_REDIRECT_ALLOW_LIST`.
- Local testing only: `SESSION_COOKIE_SECURE="false"`, `SESSION_COOKIE_SAME_SITE="lax"`, no cookie domain. Never in production (CSRF exposure).

## Checked

2026-11-04: session-mode variables, login link format, refresh call with credentials include, SDK usage, redirect allow list variable and local-testing settings confirmed against the Directus Seamless SSO page.

Method: documentation only; no commands were run.

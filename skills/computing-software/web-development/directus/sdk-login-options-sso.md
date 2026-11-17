---
id: computing-software.web-development.directus.sdk-login-options-sso
name: sdk-login-options-sso
category: computing-software
field: web-development
product: directus
tags: [sdk-login-options, sdk-ldap-login, sdk-sso-login, sdk-auth-mode]
level: advanced
status: docs-checked
description: "Use Directus SDK login options (otp, mode, provider) for LDAP and 2FA, and complete redirect-based SSO by calling refresh after the provider returns."
sources:
  - https://raw.githubusercontent.com/directus/docs/main/content/guides/04.connect/6.sdk.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `authentication()` composable manages token storage and refreshes automatically; the current token lives inside the client.

```js
await directus.login({ email, password }, { otp, mode, provider });
```

- `otp`: one-time password when 2FA is enabled.
- `mode`: how the refresh token is returned: `json`, `cookie` or `session`; defaults to `cookie`.
- `provider`: non-redirect providers. LDAP uses `identifier` (usually a username) not `email`:

```js
await client.login({ identifier: 'username', password: '...' }, { provider: 'ldap' });
```

**Redirect SSO** (Google, GitHub, Okta, etc.) cannot use `.login()`:
1. Link the user to `https://directus.example.com/auth/login/<provider>?redirect=https://your-app.com/callback`, with `<provider>` from `AUTH_PROVIDERS`.
2. The user authenticates; Directus redirects back.
3. On the callback page call `client.refresh()`.

Use session mode with credentials:

```js
const client = createDirectus(url)
  .with(authentication('session', { credentials: 'include' }))
  .with(rest({ credentials: 'include' }));
await client.refresh();
```

Gotcha: the redirect URL must be in `AUTH_<PROVIDER>_REDIRECT_ALLOW_LIST` or it is blocked.

## Checked

2026-11-04: authentication composable behaviour, login options otp, mode (default cookie) and provider, LDAP identifier login, the four-step redirect SSO flow, session mode with credentials include and the allow list warning confirmed against the Directus SDK page.

Method: documentation only; no commands were run.

---
id: computing-software.web-development.payload-cms.auth-refresh-tokens
name: auth-refresh-tokens
category: computing-software
field: web-development
product: payload-cms
tags: [refresh-tokens, refreshtokens, autorefresh, long-lived-session]
level: advanced
status: docs-checked
description: "Keep mobile apps and CLIs logged in with auth.refreshTokens, and keep Admin Panel users logged in with admin.autoRefresh."
sources:
  - https://payloadcms.com/docs/authentication/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Refresh tokens

Goal: keep clients authenticated past token expiry.

Admin Panel: set `autoRefresh: true` in the `admin` config so users stay logged in indefinitely while the browser is open on the dashboard; the token is refreshed before it expires.

Apps that are not always running (mobile apps, CLIs) cannot refresh in time. Enable refresh tokens on the auth collection:

```ts
auth: {
  refreshTokens: {
    expiration: 60 * 60 * 24 * 7, // seconds; optional, default 30 days
  },
}
```

Set `refreshTokens: true` for the defaults. Login then also returns a `refreshToken`. Exchange it at the refresh-token endpoint:

```ts
const res = await fetch('http://localhost:3000/api/users/refresh-token', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ refreshToken }),
})
const { refreshedToken, refreshToken: nextRefreshToken } = await res.json()
```

Store the new `refreshToken` for next time; the old one is replaced. `expiration` is how long the session lasts without a refresh, which is how long its refresh token can be used.

Each refresh token is one-time use: after an exchange the old token stays valid only for a 30 second grace window. Refresh tokens need `useSessions` (the default), and logging out ends them.

## Checked

2026-11-04. Read authentication/overview (refresh tokens) and authentication/operations (refresh) in the payloadcms/payload docs. Confirmed: refreshTokens option, 30 day default expiration, refreshToken in login and refresh responses, refreshedToken. Added: one-time use, grace window, session requirement.
Method: documentation only; no commands were run.

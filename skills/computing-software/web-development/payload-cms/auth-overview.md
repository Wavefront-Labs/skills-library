---
id: computing-software.web-development.payload-cms.auth-overview
name: auth-overview
category: computing-software
field: web-development
product: payload-cms
tags: [authentication, auth-collection, token-expiration, lockout]
level: practitioner
status: docs-checked
description: "Enable authentication on a collection with the auth option and configure tokenExpiration, verify, maxLoginAttempts, lockTime and useSessions."
sources:
  - https://payloadcms.com/docs/authentication/overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Authentication overview

Goal: turn a Collection into a user collection.

```ts
export const Admins: CollectionConfig = {
  slug: 'admins',
  auth: {
    tokenExpiration: 7200,   // seconds
    verify: true,            // require email verification
    maxLoginAttempts: 5,     // 0 disables lockout
    lockTime: 600 * 1000,    // milliseconds
  },
  fields: [],
}
```

`auth: true` gives default behaviour. Payload injects `email`, `hash` and `salt` fields; the hash is a PBKDF2-SHA256 derived key (600,000 iterations by default) that you should not derive yourself.

Other auth options: `cookies` (`secure`, `sameSite`, `domain`), `depth` (default `0`, how deep the user is populated into `req.user`), `disableLocalStrategy`, `forgotPassword`, `loginWithUsername`, `refreshTokens`, `removeTokenFromResponses`, `strategies`, `useAPIKey`, `useSessions`, `verify`.

- `useSessions` defaults to `true`; set `false` for stateless JWTs, which cannot be revoked until `tokenExpiration`.
- `admin.user` in the root config names the collection allowed into the Admin Panel.
- `admin.autoRefresh: true` refreshes tokens while a user stays on the dashboard.

Login (`POST /api/<slug>/login`) returns a user, token and exp.

## Checked

2026-11-04. Read authentication/overview and authentication/operations in the payloadcms/payload docs. Confirmed: option list, PBKDF2-SHA256 with 600,000 iterations, depth default 0, useSessions default true, maxLoginAttempts 0 disables lockout, lockTime in ms, tokenExpiration in seconds, autoRefresh. Nothing removed.
Method: documentation only; no commands were run.

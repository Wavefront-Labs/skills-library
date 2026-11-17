---
id: computing-software.web-development.strapi.users-permissions-jwt
name: users-permissions-jwt
category: computing-software
field: web-development
product: strapi
tags: [strapi, users-permissions, jwt, jwtmanagement, refresh, legacy-support]
level: advanced
status: docs-checked
description: "Users and Permissions JWT modes in config/plugins: legacy-support long-lived JWTs versus refresh session tokens."
sources:
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/features/users-permissions.md
  - https://raw.githubusercontent.com/strapi/documentation/main/docusaurus/docs/cms/cli.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Users & Permissions JWT modes

Set `jwtManagement` in `users-permissions.config` of `/config/plugins`:

| Mode | Behavior |
|---|---|
| `legacy-support` (default) | long-lived JWTs, traditional config |
| `refresh` | session management with short-lived access tokens and refresh tokens |

```js
module.exports = ({ env }) => ({
  'users-permissions': {
    config: {
      jwtManagement: 'legacy-support',
      jwt: {
        expiresIn: '30d', // Traditional JWT expiry
      },
    },
  },
});
```

- `jwtSecret` is typically set from the `JWT_SECRET` environment variable.
- `jwt.expiresIn` (legacy mode only) is seconds or a time-span string like `"45m"`, `"10h"`, `"7d"`. A numeric value is seconds; a string without units is milliseconds ("120" equals "120ms").
- JWT expiry beyond 30 days is not recommended.

Projects scaffolded by `create-strapi-app` ship with `jwtManagement: 'refresh'` and `sessions.httpOnly: true`, and a random `JWT_SECRET` in `.env`.

In refresh mode (`jwtManagement: 'refresh'`) the config uses a `sessions` object (Content API sessions only; the admin panel has its own `auth.sessions` options):

| Key | Default |
|---|---|
| `sessions.accessTokenLifespan` | `600` seconds (10 minutes) |
| `sessions.maxRefreshTokenLifespan` | `2592000` seconds (30 days) |
| `sessions.idleRefreshTokenLifespan` | `1209600` seconds (14 days) |
| `sessions.httpOnly` | `false`, but `true` in projects created with `create-strapi-app` |
| `sessions.cookie.name` | `'strapi_up_refresh'` |
| `sessions.cookie.secure` | `true` in production, `false` otherwise |

With `sessions.httpOnly: true` the refresh token is sent as an HTTP-only cookie instead of in the response body. A client can request the cookie for a single request with the header `x-strapi-refresh-cookie: httpOnly`, even when `sessions.httpOnly` is `false`.

## Checked

Checked 2026-11-04 against the Strapi Users & Permissions page (JWT management modes, notes, sessions table) and the CLI page (security defaults for new projects: `jwtManagement: 'refresh'`, `sessions.httpOnly: true`, random `JWT_SECRET` in `.env`). Nothing removed.

Method: documentation only; no commands were run.

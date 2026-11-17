---
id: computing-software.web-development.payload-cms.auth-operations
name: auth-operations
category: computing-software
field: web-development
product: payload-cms
tags: [auth-operations, login, me, refresh-token, forgot-password]
level: practitioner
status: docs-checked
description: "Call the auth operations (access, me, login, logout, refresh-token, verify, forgot-password, reset-password, unlock) over REST, GraphQL or the Local API."
sources:
  - https://payloadcms.com/docs/authentication/operations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Auth operations

Goal: use the endpoints that auth-enabled collections expose.

REST routes (replace `{user-collection}` with the slug): `POST /api/{user-collection}/login`, `POST .../logout`, `POST .../unlock`, `POST .../refresh-token`, `POST .../verify/{token}`, `GET .../me`, `POST .../forgot-password`, `POST .../reset-password`. `GET /api/access` returns what the current user may do.

Login:

```ts
const res = await fetch('http://localhost:3000/api/users/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email: 'dev@payloadcms.com', password: '...' }),
})
const { user, token, exp } = await res.json()
```

`me` returns `{ user, token, exp }` for a logged-in user or a null user otherwise. Refresh returns `refreshedToken` (and the next `refreshToken` when refresh tokens are enabled). Logout accepts `?allSessions=true` to end every session for the user.

The `access` response contains `canAccessAdmin` plus per-collection `create/read/update/delete` permissions and nested field permissions. Document-level access is available at `/api/{collection}/access/{id}` and `/api/{global}/access`.

GraphQL operations are named per collection label. The operations page shows `login[collection-singular-label]`, `me[...]`, `refreshToken[...]`, `verifyEmail[...]`, `forgotPassword[...]`, `resetPassword[...]`, `unlock[...]` and `logoutUser(allSessions: false)`. The GraphQL overview page instead lists `verifyPublicUser` and `logoutPublicUser` for a collection labelled PublicUser. The two pages disagree on the verify and logout names, so confirm them in the GraphQL playground Schema.

## Checked

2026-11-04. Read authentication/operations and graphql/overview in the payloadcms/payload docs. Confirmed: routes, login/me response shape, access response, refresh and logout parameters. Fixed: verify is POST, not GET. Flagged: the two pages name the GraphQL verify and logout operations differently. Removed: the unconfirmed verify step.
Method: documentation only; no commands were run.

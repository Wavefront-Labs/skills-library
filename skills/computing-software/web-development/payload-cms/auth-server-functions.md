---
id: computing-software.web-development.payload-cms.auth-server-functions
name: auth-server-functions
category: computing-software
field: web-development
product: payload-cms
tags: [server-functions, auth-server-function, login-action, nextjs-auth]
level: advanced
status: docs-checked
description: "Use Payload login, logout and refresh server functions from @payloadcms/next/auth (or the TanStack Start equivalents) to manage auth cookies."
sources:
  - https://payloadcms.com/docs/authentication/server-functions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Auth server functions

Goal: log users in and out from React Server Functions.

Payload provides `login`, `logout` and `refresh` server functions that manage the authentication cookie for you. Each needs your Payload config, so they must run on the server. Suggested wrapper signatures: `loginAction({ email, password })`, `logoutAction()`, `refreshAction()`.

Next.js - import from `@payloadcms/next/auth` in a `'use server'` file:

```ts
'use server'
import { login, logout, refresh } from '@payloadcms/next/auth'
import config from '@payload-config'

export function loginAction({ email, password }: { email: string; password: string }) {
  return login({ collection: 'users', config, email, password })
}
export function logoutAction() {
  return logout({ config })
}
export function refreshAction() {
  return refresh({ config })
}
```

TanStack Start - import the same helpers from `@payloadcms/tanstack-start/server` inside each `createServerFn` handler (dynamic `import()` of the helper and `@payload-config`).

To read the current user in any server code use `payload.auth({ headers })`, which returns `{ user }`.

All three functions reject on failure, so wrap calls in try/catch.

## Checked

2026-11-04. Read authentication/server-functions in the payloadcms/payload docs. Confirmed: login, logout and refresh from @payloadcms/next/auth, TanStack Start equivalents, payload.auth. Removed: the cookie verify step (not stated). Added: rejection behaviour.
Method: documentation only; no commands were run.

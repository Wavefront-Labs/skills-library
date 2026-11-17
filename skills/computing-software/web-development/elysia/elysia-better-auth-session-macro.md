---
id: computing-software.web-development.elysia.elysia-better-auth-session-macro
name: elysia-better-auth-session-macro
category: computing-software
field: web-development
product: elysia
tags: [integrations-better-auth, better-auth, macro, session, authentication]
level: advanced
status: docs-checked
description: "Protect Elysia routes with Better Auth by writing a macro whose resolve loads the session and user and returns 401 when absent."
sources:
  - https://elysiajs.com/integrations/better-auth.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: give routes typed `user` and `session` values and block unauthenticated requests with one option.

Wrap the mount and a macro in a named plugin instance:

```ts
import { Elysia } from 'elysia'
import { auth } from './auth'

const betterAuth = new Elysia({ name: 'better-auth' })
    .mount(auth.handler)
    .macro({
        auth: {
            async resolve({ status, request: { headers } }) {
                const session = await auth.api.getSession({ headers })
                if (!session) return status(401)
                return { user: session.user, session: session.session }
            }
        }
    })

const app = new Elysia()
    .use(betterAuth)
    .get('/user', ({ user }) => user, { auth: true })
    .listen(3000)
```

How it works:
- `auth.api.getSession({ headers })` reads the session from the incoming request headers.
- Returning `status(401)` from `resolve` stops the request before the handler.
- Returning `{ user, session }` adds those to the context of every route that sets `auth: true`.
- The instance is created as `new Elysia({ name: 'better-auth' })` in the docs example.

Gotchas:
- The `user`/`session` context only exists on routes that opt in with `auth: true`.
- Mounting and the macro are in the same plugin so that importing `betterAuth` brings both; remember CORS ordering (see the mount skill).

## Checked

Checked 2026-11-07 against the Elysia documentation source (integrations/better-auth.html); each claim, option name and default was compared with the page text. Removed the invented Verify step and an unfinished gotcha about an unread page.

Method: documentation only; no commands were run.

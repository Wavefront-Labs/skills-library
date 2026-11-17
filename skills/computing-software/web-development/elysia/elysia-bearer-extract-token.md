---
id: computing-software.web-development.elysia.elysia-bearer-extract-token
name: elysia-bearer-extract-token
category: computing-software
field: web-development
product: elysia
tags: [bearer, authentication, rfc6750, plugin]
level: intro
status: docs-checked
description: "Read the Bearer token from the Authorization header in Elysia with @elysia/bearer and reject requests that carry none."
sources:
  - https://elysiajs.com/plugins/bearer.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: expose the RFC 6750 Bearer token on the handler context so routes can check it.

1. Install: `bun add @elysia/bearer`
2. Register the plugin and read `bearer` from the context:

```typescript
import { Elysia } from 'elysia'
import { bearer } from '@elysia/bearer'

const app = new Elysia()
    .use(bearer())
    .get('/sign', ({ bearer }) => bearer, {
        beforeHandle({ bearer, set, status }) {
            if (!bearer) {
                set.headers['WWW-Authenticate'] =
                    `Bearer realm='sign', error="invalid_request"`
                return status(400, 'Unauthorized')
            }
        }
    })
    .listen(3000)
```

3. Put the missing-token check in `beforeHandle` so the handler never runs without a token. Set the `WWW-Authenticate` response header as shown, with the realm and `error="invalid_request"`, when you reject.

Gotchas:
- The plugin only retrieves the token. The docs state it does NOT handle authentication validation; the decision is left to you, for example inside `beforeHandle`.
- The example returns `status(400, 'Unauthorized')`, i.e. status 400 with an "Unauthorized" message.

## Checked

Checked 2026-11-07 against the Elysia documentation source (plugins/bearer.html); each claim, option name and default was compared with the page text. Removed advice to verify with @elysia/jwt, the invented Verify step and the 401 advice.

Method: documentation only; no commands were run.

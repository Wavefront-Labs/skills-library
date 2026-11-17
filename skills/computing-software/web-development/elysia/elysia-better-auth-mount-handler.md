---
id: computing-software.web-development.elysia.elysia-better-auth-mount-handler
name: elysia-better-auth-mount-handler
category: computing-software
field: web-development
product: elysia
tags: [integrations-better-auth, better-auth, authentication, mount, openapi]
level: practitioner
status: docs-checked
description: "Mount a Better Auth instance on an Elysia app, choose its path prefix and basePath, and wire CORS and OpenAPI docs around it."
sources:
  - https://elysiajs.com/integrations/better-auth.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: serve Better Auth endpoints from Elysia.

1. Create the instance (basic setup from the docs):

```ts
// auth.ts
import { betterAuth } from 'better-auth'
import { Pool } from 'pg'
export const auth = betterAuth({ database: new Pool() })
```

2. Mount its handler with Elysia's `mount`:

```ts
new Elysia().mount(auth.handler).listen(3000)
```

Better Auth is then reachable at `http://localhost:3000/api/auth`.

3. Prefix it. Recommended: `.mount('/auth', auth.handler)` gives `/auth/api/auth`. To avoid the redundant URL set `basePath` in the Better Auth config (`betterAuth({ basePath: '/api' })`), giving `/auth/api`. You cannot set `basePath` to empty or `/`.

4. CORS for a separate frontend, registered before the mount:

```ts
new Elysia()
    .use(cors({ origin: 'http://localhost:3001',
        methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
        credentials: true, allowedHeaders: ['Content-Type', 'Authorization'] }))
    .mount(auth.handler)
```

5. Put Better Auth routes in your OpenAPI page: add `plugins: [openAPI()]` (from `better-auth/plugins`) to the instance, then build `OpenAPI.getPaths(prefix = '/auth/api')` and `OpenAPI.components` from `auth.api.generateOpenAPISchema()` (cache the schema promise, prefix every path and tag operations `'Better Auth'`), and pass them: `openapi({ documentation: { components: await OpenAPI.components, paths: await OpenAPI.getPaths() } })`.

Gotchas:
- Without the `openAPI()` plugin, `auth.api.generateOpenAPISchema` does not exist and TypeScript reports `Property 'generateOpenAPISchema' does not exist`.
- Keep the prefix passed to `getPaths` in sync with your mount path plus `basePath`.
- Read the Better Auth installation guide first; the page assumes it.

## Checked

Checked 2026-11-07 against the Elysia documentation source (integrations/better-auth.html); each claim, option name and default was compared with the page text. Removed the invented Verify step.

Method: documentation only; no commands were run.

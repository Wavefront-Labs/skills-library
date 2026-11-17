---
id: computing-software.web-development.elysia.elysia-nextjs-route-handler-eden
name: elysia-nextjs-route-handler-eden
category: computing-software
field: web-development
product: elysia
tags: [integrations-frameworks, nextjs, eden, route-handler]
level: practitioner
status: docs-checked
description: "Run Elysia inside a Next.js App Router catch-all route, set the prefix, and call it with Eden Treaty directly on the server or over HTTP on the client."
sources:
  - https://elysiajs.com/integrations/nextjs.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: host the Elysia API in the same Next.js repo.

1. Create `app/api/[[...slugs]]/route.ts`, define the server, and export `app.fetch` under each HTTP method name you want:

```typescript
import { Elysia, t } from 'elysia'

const app = new Elysia({ prefix: '/api' })
    .get('/', 'Hello Nextjs')
    .post('/', ({ body }) => body, { body: t.Object({ name: t.String() }) })

export const GET = app.fetch
export const POST = app.fetch
```

2. Prefix rule: the Elysia `prefix` must match where the route file sits. A server at `app/user/[[...slugs]]/route.ts` needs `prefix: '/user'`.

3. pnpm users: pnpm does not auto-install peer dependencies, so run `pnpm add @sinclair/typebox openapi-types`.

4. Eden with an isomorphic client. Export the instance (`export const app = new Elysia({ prefix: '/api' })...`) and build the client:

```typescript
// lib/eden.ts
import { treaty } from '@elysia/eden'
import type { app } from '../app/api/[[...slugs]]/route'

export const api =
  typeof process !== 'undefined'
    ? treaty(app).api                       // server: direct call, no network
    : treaty<typeof app>('localhost:3000').api   // client: HTTP
```

`.api` enters the `/api` prefix. Use `await api.get()` in server and client components. React Query works by calling the client inside `queryFn`.

Gotchas:
- Test `typeof process`, NOT `typeof window`: `window` is undefined at build time and causes a hydration error.
- Export handlers named after each HTTP method you need (the example exports GET and POST).
- The docs' Eden sample uses `treaty.schema(...)` for the body (without importing `treaty` in that file), and the React Query example is a TanStack Router snippet; step 1 uses `t.Object` instead.

## Checked

Checked 2026-11-07 against the Elysia documentation source (integrations/nextjs.html); each claim, option name and default was compared with the page text. Removed the invented Verify step and speculation about the sample origins.

Method: documentation only; no commands were run.

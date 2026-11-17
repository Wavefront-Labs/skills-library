---
id: computing-software.web-development.elysia.elysia-tanstack-start-server-route
name: elysia-tanstack-start-server-route
category: computing-software
field: web-development
product: elysia
tags: [integrations-frameworks, tanstack-start, eden, ssr]
level: practitioner
status: docs-checked
description: "Mount Elysia in a TanStack Start server route under /api and call it with Eden Treaty from loaders and React Query using createIsomorphicFn."
sources:
  - https://elysiajs.com/integrations/tanstack-start.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: serve Elysia from `src/routes/api.$.ts` in TanStack Start with end-to-end types.

1. Create `src/routes/api.$.ts`:

```typescript
import { Elysia } from 'elysia'
import { createFileRoute } from '@tanstack/react-router'
import { createIsomorphicFn } from '@tanstack/react-start'
import { treaty } from '@elysia/eden'

const app = new Elysia({ prefix: '/api' }).get('/', 'Hello Elysia!')

const handle = ({ request }: { request: Request }) => app.fetch(request)

export const Route = createFileRoute('/api/$')({
    server: { handlers: { GET: handle, POST: handle } }
})

export const getTreaty = createIsomorphicFn()
    .server(() => treaty(app).api)
    .client(() => treaty<typeof app>('localhost:3000').api)
```

Elysia now answers on `/api`. Add more keys to `server.handlers` for other HTTP methods.

2. `createIsomorphicFn` yields two Eden Treaty instances: on the server Elysia is called directly without HTTP overhead; on the client it is called over HTTP.

3. Loader data:

```tsx
export const Route = createFileRoute('/a')({
    component: App,
    loader: () => getTreaty().get().then((res) => res.data)
})
function App() { const data = Route.useLoaderData(); return data }
```

During SSR the loader executes on the server with no HTTP hop; on client-side navigation the loader runs in the browser and makes an HTTP request.

4. React Query: `useQuery({ queryKey: ['get'], queryFn: () => getTreaty().get() })` and read `response?.data`; caching, pagination and infinite queries work as usual.

5. pnpm: `pnpm add @sinclair/typebox openapi-types`.

Gotchas:
- The example pairs Elysia `prefix: '/api'` with the route path `/api/$`.
- The client branch in the docs example uses a hard-coded `localhost:3000`.

## Checked

Checked 2026-11-07 against the Elysia documentation source (integrations/tanstack-start.html); each claim, option name and default was compared with the page text. Removed the invented Verify step and the unsupported deployment advice.

Method: documentation only; no commands were run.

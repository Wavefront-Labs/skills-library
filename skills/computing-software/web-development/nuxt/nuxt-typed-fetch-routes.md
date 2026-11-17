---
id: computing-software.web-development.nuxt.nuxt-typed-fetch-routes
name: nuxt-typed-fetch-routes
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, typescript, fetch, server-routes, standard-schema]
level: advanced
status: docs-checked
description: "How $fetch and useFetch are typed from server handlers, validated handlers, baseURL resolution, strictRouteTypes and ServerRoutes augmentation."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/1.getting-started/10.data-fetching.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`$fetch` and `useFetch` infer response types from the handlers in `server/`. The HTTP method picks the handler: `/api/todos` with POST is typed by `server/api/todos.post.ts`, not the GET file.

Validated handlers type their input via any Standard Schema library:

```ts
import { z } from 'zod'
export default defineValidatedHandler({
  validate: { body: z.object({ title: z.string() }) },
  handler: () => ({ id: '1' }),
})
```

Then `$fetch('/api/todos', { method: 'POST', body: { title: 42 } })` is a type error and a missing body is an error.

Untypable requests resolve to `unknown`: a path built at runtime, an absolute URL, a `Request` object. Provide the type yourself: `$fetch<{ id: string }>(`/api/${resource}`)`. Unrecognised paths are `unknown` by default because middleware, `routeRules` proxies or catch-alls may answer; enable `experimental.strictRouteTypes` to make them errors.

`baseURL` is part of the resolved route: `$fetch('/todos', { baseURL: '/api' })` resolves `/api/todos`, also for `$fetch.create({ baseURL })` and `createUseFetch`. Passing a path that already contains the base (`/api/todos` with base `/api`) is an error. Runtime or external-origin bases stay `unknown`.

Declare routes Nuxt cannot discover (registered at runtime by a Nitro plugin, or an external API) by augmenting `ServerRoutes` in a `.d.ts` under `shared/`:

```ts
import type { Endpoint } from 'nuxt/app'
declare module '@nuxt/schema' {
  interface ServerRoutes {
    '/api/hello': { [Endpoint]: { GET: { response: { message: string } } } }
  }
}
```

The docs note this resolves at the call site but does not appear in editor completions. Modules registering handlers should use `addServerHandler`.

Verify: hover a `$fetch` result in the editor to see the inferred type.

## Checked

2026-11-08. Read the Typing section of the Nuxt data-fetching doc (from the handler-typing paragraph through createUseFetch; the rest of that long page was not read for this skill). Confirmed method-specific handler typing, Standard Schema validated handlers, unknown for runtime paths, absolute URLs and Request objects, strictRouteTypes, baseURL resolution, the ServerRoutes augmentation, the completions caveat, and addServerHandler. Nothing removed.

Method: documentation only; no commands were run.

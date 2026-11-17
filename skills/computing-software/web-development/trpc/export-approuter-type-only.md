---
id: computing-software.web-development.trpc.export-approuter-type-only
name: export-approuter-type-only
category: computing-software
field: web-development
product: trpc
tags: [trpc, approuter, type-only-import, typescript]
level: intro
status: docs-checked
description: "Define a router with router() and export only typeof appRouter so the client imports a type and no server code ends up in the bundle."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/routers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A router is created by passing an object of procedures to `router()`. Each key becomes an API endpoint, and your adapter must be given the `appRouter` instance for the endpoints to be reachable.

```ts
import { publicProcedure, router } from './trpc';

const appRouter = router({
  greeting: publicProcedure.query(() => 'hello tRPC v11!'),
});

// Export only the type of a router!
// This prevents us from importing server code on the client.
export type AppRouter = typeof appRouter;
```

On the client, use `import type { AppRouter } from '.../server'` and never import the `appRouter` value. A type-only import is always erased, so your server code can't end up in the client bundle. The client passes `AppRouter` as the generic, as in `createTRPCClient<AppRouter>()`.

Naming restriction: procedures cannot be named `then`, `call` or `apply`. `router()` throws if you use these names.

## Checked

2026-11-04: read in full against the tRPC docs repo (trpc/trpc, docs repo www/v11/docs/): server/routers.md (Defining a router). Every parameter name, default, error string and code sample left in this skill appears on those pages. Removed: the invented Verify step, the 'database drivers, secrets' example and the thenable rationale for reserved names.

Method: documentation only; no commands were run.

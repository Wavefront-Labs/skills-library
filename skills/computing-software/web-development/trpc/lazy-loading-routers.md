---
id: computing-software.web-development.trpc.lazy-loading-routers
name: lazy-loading-routers
category: computing-software
field: web-development
product: trpc
tags: [trpc, lazy, dynamic-import, cold-start, router]
level: advanced
status: docs-checked
description: "Use lazy() from @trpc/server to load sub-routers on demand and cut serverless cold starts, with short-hand and named-export forms."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/merging-routers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `lazy` function dynamically loads routers, which can reduce cold starts of your application. A lazily loaded router is used exactly like a normal one.

```ts
import { lazy } from '@trpc/server';
import { router } from '../trpc';

export const appRouter = router({
  // Option 1: short-hand when the module has exactly 1 router exported
  greeting: lazy(() => import('./greeting.js')),
  // Option 2: if exporting more than 1 router
  user: lazy(() => import('./user.js').then((m) => m.userRouter)),
});
export type AppRouter = typeof appRouter;
```

Each lazy module exports its router built from the shared `t` (`router`, `publicProcedure` imported from the trpc setup file), for instance `export const greetingRouter = router({ hello: publicProcedure.query(() => 'world') })`.

Option 1 is the short-hand for a module that exports exactly one router; use Option 2 (select the named export) when it exports more than one.

## Checked

2026-11-04: read in full against the tRPC docs repo (trpc/trpc, docs repo www/v11/docs/): server/merging-routers.md (Dynamically load routers). Every parameter name, default, error string and code sample left in this skill appears on those pages. Removed: the invented Verify step, the 'use it when serverless/edge' advice and the 'types are unaffected' claim.

Method: documentation only; no commands were run.

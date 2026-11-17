---
id: computing-software.web-development.trpc.server-side-calls-createcaller
name: server-side-calls-createcaller
category: computing-software
field: web-development
product: trpc
tags: [trpc, createcallerfactory, createcaller, server-side-call, testing]
level: practitioner
status: docs-checked
description: "Call procedures in-process with t.createCallerFactory, passing a context object or function; the caller skips your adapter createContext."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/server-side-calls.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Call your procedures directly from the same server they are hosted in with `createCallerFactory`; the page says this is useful for server-side calls and for integration testing.

```ts
const { createCallerFactory, router } = t;
const appRouter = router({ post: router({ add: ..., list: ... }) });

// 1. create a caller-function for your router
const createCaller = createCallerFactory(appRouter);
// 2. create a caller using your Context
const caller = createCaller({ foo: 'bar' });
// 3. call procedures like functions
const addedPost = await caller.post.add({ title: 'How to make server-side call in tRPC' });
const postList = await caller.post.list();
```

The caller does not run your adapter's `createContext`, so pass everything procedures and middlewares expect; an inner context works well because it needs no request. You can also pass a function returning the context (or a promise of it). The caller calls it for every procedure call, so cache it (for example with React's `cache()`) if expensive.

`router.createCaller(ctx)` is also documented. Middlewares run before procedures, so a protected route called with `createCaller({})` fails with the middleware's error, while a context with `user` succeeds.

Do not use `createCaller` to call one procedure from another: that re-creates context, re-runs middleware and re-validates input. Extract shared logic into a plain function (for example `getCustomerId(userId, prisma)`) and call it from both procedures.

## Checked

2026-11-07. Read in full from a clone of github.com/trpc/trpc (main, commit fe64009), www/v11/docs/server/server-side-calls.md (read in full): intro and info note on not calling a caller from another procedure, the basic example, the context function paragraph, the integration-test snippet, `router.createCaller()` and the middleware example.

Removed or corrected: "server components, scripts" as use cases and the word "older" for router.createCaller (neither is on the page), and the invented Verify step naming Vitest.

Method: documentation only; no commands were run.

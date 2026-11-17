---
id: computing-software.web-development.trpc.middleware-logging-timing
name: middleware-logging-timing
category: computing-software
field: web-development
product: trpc
tags: [trpc, middleware, logging, timing, opts-next]
level: practitioner
status: docs-checked
description: "Log duration of every query by wrapping opts.next() in a middleware and inspecting result.ok, with path and type from the middleware options."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/middlewares.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A middleware can measure and log procedures. The docs example:

```ts
export const loggedProcedure = publicProcedure.use(async (opts) => {
  const start = Date.now();

  const result = await opts.next();

  const durationMs = Date.now() - start;
  const meta = { path: opts.path, type: opts.type, durationMs };

  result.ok
    ? console.log('OK request timing:', meta)
    : console.error('Non-OK request timing', meta);

  return result;
});

export const appRouter = router({
  foo: loggedProcedure.query(() => 'bar'),
  abc: loggedProcedure.query(() => 'def'),
});
```

Points to remember:

- `opts.path` is the procedure path and `opts.type` is `query`, `mutation` or `subscription`.
- `opts.next()` does not throw when the downstream procedure fails; it resolves to a result with `ok: false` and the error, so branch on `result.ok`.
- You must `return result` so the response reaches the client.

## Checked

2026-11-07. Read in full from a clone of github.com/trpc/trpc (main, commit fe64009), www/v11/docs/server/middlewares.md (read in full, including the trpclogger include block): the Logging snippet, the list of middleware parameters, and the Common mistakes note that `opts.next()` does not throw but resolves with `ok: false`.

Removed or corrected: the invented example path `user.list`, the unsourced advice to build logging into the base procedure, the adapter onError aside, and the invented Verify step.

Method: documentation only; no commands were run.

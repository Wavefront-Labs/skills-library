---
id: computing-software.web-development.trpc.middleware-order-and-raw-input
name: middleware-order-and-raw-input
category: computing-software
field: web-development
product: trpc
tags: [trpc, middleware, getrawinput, input, order]
level: advanced
status: docs-checked
description: "Middlewares run in chain order and .input() parses at its position; before it opts.input is undefined and getRawInput() returns the unvalidated value."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/middlewares.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Middlewares run in the order they are chained, and the parser given to `.input()` runs at its position in that chain. A middleware chained before `.input()` receives `opts.input` as `undefined`. If it needs the data it can read the unvalidated input with `await opts.getRawInput()`.

```ts
const auditedProcedure = publicProcedure.use(async (opts) => {
  const rawInput = await opts.getRawInput();
  console.log(`${opts.type} ${opts.path}`, rawInput);
  return opts.next();
});

auditedProcedure
  .input(z.object({ id: z.string() }))
  .use((opts) => {
    // after `.input()`, `opts.input` is parsed and typed
    console.log(opts.input.id);
    return opts.next();
  })
  .query((opts) => opts.input.id);
```

Besides `ctx`, `input`, `getRawInput` and `next`, a middleware receives the procedure `path`, `type` (`query`, `mutation` or `subscription`), `meta`, and the request's `signal`.

## Checked

2026-11-07. Read in full from a clone of github.com/trpc/trpc (main, commit fe64009), www/v11/docs/server/middlewares.md (read in full), section "Middleware order and input": order of chained middlewares, `opts.input` undefined before `.input()`, `getRawInput()`, and the list of parameters a middleware receives.

Removed or corrected: the unsourced design rule about ordering authentication and authorization, the AbortSignal gloss, and the invented Verify step.

Method: documentation only; no commands were run.

---
id: computing-software.web-development.trpc.middleware-pipe-extension
name: middleware-pipe-extension
category: computing-software
field: web-development
product: trpc
tags: [trpc, middleware, unstable-pipe, context, overlap]
level: advanced
status: docs-checked
description: "Extend a middleware with unstable_pipe() to build chained context types, and know why the ctx overlap rule makes piping order matter."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/middlewares.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`unstable_pipe()` extends one middleware with another in a typesafe way. The `unstable_` prefix marks a newer API; the docs say you are safe to use it.

```ts
const fooMiddleware = t.middleware((opts) => {
  return opts.next({ ctx: { foo: 'foo' as const } });
});

const barMiddleware = fooMiddleware.unstable_pipe((opts) => {
  const { ctx } = opts; // ctx.foo is available here
  return opts.next({ ctx: { bar: 'bar' as const } });
});

const barProcedure = publicProcedure.use(barMiddleware);
barProcedure.query((opts) => opts.ctx.bar);
```

The procedure receives the new context value. Order matters and the contexts must overlap. In the docs' forbidden example, `fooMiddleware` replaces `ctx.a` (originally an object) with a string, while `barMiddleware` still expects the root context where `ctx.a` is an object. So `fooMiddleware.unstable_pipe(barMiddleware)` is a type error, whereas `barMiddleware.unstable_pipe(fooMiddleware)` works.

In the docs snippet the invalid pipe is annotated as TypeScript error 2345.

## Checked

2026-11-07. Read in full from a clone of github.com/trpc/trpc (main, commit fe64009), www/v11/docs/server/middlewares.md (read in full), section "Extending middlewares": the `unstable_` info note, the fooMiddleware/barMiddleware snippet, the overlap explanation and the forbidden example.

Removed or corrected: the unsourced rule of thumb and the advice to prefer additive context; the Verify step was turned into the page-backed note about error 2345.

Method: documentation only; no commands were run.

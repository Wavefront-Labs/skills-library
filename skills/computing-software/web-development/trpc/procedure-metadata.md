---
id: computing-software.web-development.trpc.procedure-metadata
name: procedure-metadata
category: computing-software
field: web-development
product: trpc
tags: [trpc, meta, metadata, defaultmeta, middleware]
level: practitioner
status: docs-checked
description: "Attach typed meta to procedures with initTRPC.meta<Meta>() and read it in middleware; defaults and chained meta are shallow merged."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/metadata.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Procedure metadata adds an optional, procedure-specific `meta` property available to all middleware.

```ts
interface Meta {
  authRequired: boolean;
}
export const t = initTRPC.context<Context>().meta<Meta>().create();

export const authedProcedure = t.procedure.use(async (opts) => {
  const { meta, next, ctx } = opts;
  // only check authorization if enabled
  if (meta?.authRequired && !ctx.user) {
    throw new TRPCError({ code: 'UNAUTHORIZED' });
  }
  return next();
});

export const appRouter = t.router({
  hello: authedProcedure.meta({ authRequired: false }).query(() => ({ greeting: 'hello world' })),
  protectedHello: authedProcedure.meta({ authRequired: true }).query(() => ({ greeting: 'hello-world' })),
});
```

Defaults and chaining: pass `defaultMeta` to `create()`, for example `{ authRequired: false }`. If you chain `.meta()` on a base procedure the values are shallow merged: a base with `{ authRequired: true, role: 'user' }` followed by `.meta({ role: 'admin' })` yields `{ authRequired: true, role: 'admin' }`.

The `meta` property is available in all middleware function parameters. The docs also point to `trpc-openapi` which uses metadata to expose REST-compatible endpoints.

## Checked

2026-11-07. Read in full from a clone of github.com/trpc/trpc (main, commit fe64009), www/v11/docs/server/metadata.md (read in full): intro, `meta<Meta>()` setup, the authRequired example, `defaultMeta` and the shallow merge example, and the trpc-openapi tip.

Removed or corrected: the invented Verify step and an unsourced typing claim (reworded to the page sentence).

Method: documentation only; no commands were run.

---
id: computing-software.web-development.trpc.context-extension
name: context-extension
category: computing-software
field: web-development
product: trpc
tags: [trpc, middleware, context-extension, ctx, type-narrowing]
level: practitioner
status: docs-checked
description: "Use opts.next({ ctx }) to add or override context keys in a typesafe way; the new ctx is merged and flows to later middlewares and the resolver."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/middlewares.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Context extension lets a middleware add or override keys on the procedure context, in a typesafe way. The `ctx` you pass to `opts.next()` is merged into the existing context, so you only pass the keys you add or change.

```ts
const protectedProcedure = publicProcedure.use(async function isAuthed(opts) {
  const { ctx } = opts;
  // `ctx.user` is nullable
  if (!ctx.user) {
    throw new TRPCError({ code: 'UNAUTHORIZED' });
  }
  return opts.next({
    ctx: {
      // user value is known to be non-null now
      user: ctx.user,
    },
  });
});

protectedProcedure.query((opts) => {
  return opts.ctx.user; // typed as non-null
});
```

The changes are visible to all chained consumers, such as later middlewares and procedures.

Pitfall from the docs: when middlewares are combined with `.unstable_pipe()`, the context must overlap. A middleware that overrides a key with a different type (an object `ctx.a` replaced by a string) cannot be piped into a middleware that still expects the original type, while piping in the other order works.

## Checked

2026-11-04: read in full against the tRPC docs repo (trpc/trpc, docs repo www/v11/docs/): server/middlewares.md (Context Extension, Extending middlewares). Every parameter name, default, error string and code sample left in this skill appears on those pages. Removed: the invented Verify step, the unsupported use-case list and the claim that overrides also break .concat().

Method: documentation only; no commands were run.

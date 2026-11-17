---
id: computing-software.web-development.trpc.middleware-authorization
name: middleware-authorization
category: computing-software
field: web-development
product: trpc
tags: [trpc, middleware, authorization, trpcerror, adminprocedure]
level: practitioner
status: docs-checked
description: "Write an admin-only middleware with procedure.use() that throws a TRPCError and passes a narrowed ctx to opts.next()."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/middlewares.md
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/authorization.md
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/error-handling.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Add middleware to a procedure with `procedure.use()`. A middleware wraps the procedure call and must call `opts.next()` and return its result.

```ts
export const adminProcedure = publicProcedure.use(async (opts) => {
  const { ctx } = opts;
  if (!ctx.user?.isAdmin) {
    throw new TRPCError({ code: 'UNAUTHORIZED' });
  }
  return opts.next({
    ctx: { user: ctx.user },
  });
});

const adminRouter = router({
  secretPlace: adminProcedure.query(() => 'a key'),
});

export const appRouter = router({
  foo: publicProcedure.query(() => 'bar'),
  admin: adminRouter,
});
```

Every call to an `adminProcedure` verifies the user is an admin before the resolver runs. Passing `ctx: { user: ctx.user }` to `next` narrows the type: downstream code sees `user` as defined.

The thrown `TRPCError` is mapped to an HTTP status by its code (`UNAUTHORIZED` is 401, `FORBIDDEN` is 403 in the error-handling page's code table). The middlewares page uses `UNAUTHORIZED` for the failed admin check, while the authorization page advises `UNAUTHORIZED` (401) when the caller is not signed in and `FORBIDDEN` (403) when they are signed in but not allowed to do this, and shows an `adminProcedure` built on a protected procedure that throws `FORBIDDEN` on a role mismatch.

## Checked

2026-11-07. Read in full from a clone of github.com/trpc/trpc (main, commit fe64009), www/v11/docs/server/middlewares.md (read in full, including the admin include block), www/v11/docs/server/authorization.md and www/v11/docs/server/error-handling.md (both read in full): the adminProcedure snippet, router snippet, narrowing via opts.next ctx, the UNAUTHORIZED vs FORBIDDEN guidance and the error code table with HTTP codes.

Removed or corrected: the unsourced "many teams" claim and the pointer to the procedures docs (the UNAUTHORIZED vs FORBIDDEN guidance is on the authorization page, now cited); the invented Verify step. Added authorization.md and error-handling.md as sources.

Method: documentation only; no commands were run.

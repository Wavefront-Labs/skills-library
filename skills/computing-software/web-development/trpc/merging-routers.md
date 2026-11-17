---
id: computing-software.web-development.trpc.merging-routers
name: merging-routers
category: computing-software
field: web-development
product: trpc
tags: [trpc, merging-routers, mergerouters, router, organization]
level: practitioner
status: docs-checked
description: "Split an API across files and combine with namespaced child routers or flat t.mergeRouters; mergeRouters throws on duplicate paths or mixed instances."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/merging-routers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Writing the whole API in one file gets unwieldy. Two ways to combine routers:

Child routers (namespaced):

```ts
const appRouter = router({
  user: userRouter,
  post: postRouter,
});
export type AppRouter = typeof appRouter;
```

Client calls are `user.list`, `post.create`.

Flat namespace with `t.mergeRouters`:

```ts
const appRouter = mergeRouters(userRouter, postRouter);
```

In the flat form give procedures unique names (`userList`, `postCreate`), because `mergeRouters` throws if two routers define the same procedure path. It also throws when the routers come from separate tRPC instances that each set a transformer or error formatter, so merge routers built from the same `t` (see `computing-software.web-development.trpc.initialize-trpc-once`).

Export `mergeRouters` alongside `router` and `publicProcedure` from your trpc setup file (`export const mergeRouters = t.mergeRouters`).

Use `t.mergeRouters` only if you prefer all procedures flat in one namespace; the page shows child routers first.

## Checked

2026-11-07. Read in full from a clone of github.com/trpc/trpc (main, commit fe64009), www/v11/docs/server/merging-routers.md (read in full, including the trpcbase include block): child routers snippet, `t.mergeRouters` snippet, the throw on duplicate paths and on separate instances that each set a transformer or error formatter, and `export const mergeRouters = t.mergeRouters`.

Removed or corrected: the unsourced guidance on when to prefer child routers or feature plugins, and the invented Verify step. The page also covers lazy loading, which this skill does not claim.

Method: documentation only; no commands were run.

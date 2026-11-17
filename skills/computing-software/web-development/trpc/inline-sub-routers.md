---
id: computing-software.web-development.trpc.inline-sub-routers
name: inline-sub-routers
category: computing-software
field: web-development
product: trpc
tags: [trpc, nested-router, sub-router, router, namespacing]
level: practitioner
status: docs-checked
description: "Group procedures into nested namespaces with router() or a plain object literal; both forms are equivalent and give dotted client paths."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/routers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Nested routers give your API namespaces such as `user.list` and `post.create`. In v11 you can nest in two equivalent ways: by calling `router()` for the sub-router, or by using an inline plain object.

```ts
const appRouter = router({
  // Using the router() method
  nested1: router({
    proc: publicProcedure.query(() => '...'),
  }),
  // Using an inline sub-router
  nested2: {
    proc: publicProcedure.query(() => '...'),
  },
});
```

The docs state that `nested1` and `nested2` are equal. For combining independently defined routers see `computing-software.web-development.trpc.merging-routers` for the merge helpers.

## Checked

2026-11-04: read in full against the tRPC docs repo (trpc/trpc, docs repo www/v11/docs/): server/routers.md (Defining an inline sub-router), server/merging-routers.md. Every parameter name, default, error string and code sample left in this skill appears on those pages. Removed: the invented Verify step, the client call syntax, the 'avoids an extra import' advice and the claim that reserved names apply at every level.

Method: documentation only; no commands were run.

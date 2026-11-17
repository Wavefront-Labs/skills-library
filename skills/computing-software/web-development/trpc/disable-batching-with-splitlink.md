---
id: computing-software.web-development.trpc.disable-batching-with-splitlink
name: disable-batching-with-splitlink
category: computing-software
field: web-development
product: trpc
tags: [trpc, splitlink, batching, httplink, context]
level: practitioner
status: docs-checked
description: "Turn batching off globally on the server or per request with a splitLink on op.context.skipBatch that swaps httpBatchLink for httpLink."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/client/links/splitLink.md
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/client/links/httpBatchLink.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
To skip batching only for selected calls, branch on a context flag.

```ts
const client = createTRPCClient<AppRouter>({
  links: [
    splitLink({
      condition(op) { return Boolean(op.context.skipBatch); },
      true: httpLink({ url }),
      false: httpBatchLink({ url }),
    }),
  ],
});

const post = await client.posts.query(undefined, { context: { skipBatch: true } });
```

In React Query: `trpc.posts.useQuery(undefined, { trpc: { context: { skipBatch: true } } })`.

`splitLink` takes `condition(op) => boolean` plus `true` and `false`. Both branches are required and each may be a single link or an array. Splitting creates a brand-new chain per branch, so each branch must contain a terminating link (at the end of an array).

Turning batching off for everything:

1. Server: `createHTTPServer({ router: appRouter, allowBatching: false })` (or the same option on the Next.js handler).
2. Client: replace `httpBatchLink` with `httpLink`. In Next.js, swap the link in the client passed to the provider.

## Checked

2026-11-04: read in full against the tRPC docs repo (trpc/trpc, docs repo www/v11/docs/): client/links/splitLink.md, client/links/httpBatchLink.md (Disabling request batching). Every parameter name, default, error string and code sample left in this skill appears on those pages. Removed: the invented Verify step and the unsupported 'requests will fail if only the server disables batching' sentence.

Method: documentation only; no commands were run.

---
id: computing-software.web-development.trpc.http-batch-link-usage
name: http-batch-link-usage
category: computing-software
field: web-development
product: trpc
tags: [trpc, httpbatchlink, batching, client, promise-all]
level: practitioner
status: docs-checked
description: "Set up httpBatchLink so calls made in one tick become a single request, and know the shared HTTP link options like fetch, headers, methodOverride, pathSeparator."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/client/links/httpBatchLink.md
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/client/links/httpLink.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`httpBatchLink` is a terminating link that merges individual operations into one HTTP request. A batch can mix procedures; queries and mutations are batched separately.

```ts
const client = createTRPCClient<AppRouter>({
  links: [httpBatchLink({ url: 'http://localhost:3000' /*, transformer */ })],
});
const somePosts = await Promise.all([
  trpc.post.byId.query(1),
  trpc.post.byId.query(2),
  trpc.post.byId.query(3),
]);
```

Calls in the same event loop tick are batched, so `Promise.all` is common but not required. The code above makes one HTTP request and the server runs `createContext` once. Each procedure still runs its own resolver, so database round trips depend on your data layer: Prisma batches `findUnique()` calls from the same tick, and a DataLoader does the same for other queries.

Options shared with `httpLink` (`HTTPLinkOptions`):
- `url`: string or URL.
- `fetch`: ponyfill for fetch.
- `transformer`: must match the server.
- `headers`: object or callback. `httpLink` calls it with `{ op }`; batch links call it once per batch with `{ opList }`.
- `methodOverride: 'POST'`: send everything as POST; the server must allow it with `allowMethodOverride`.
- `pathSeparator`: `'.' | '_' | '~' | '-'`, default `'.'`; must match the server's setting.

Batch-only options: `maxURLLength` and `maxItems` (both default `Infinity`).

`httpLink` takes the same shape but sends one request per call and supports both GET and POST.

## Checked

2026-11-04: read in full against the tRPC docs repo (trpc/trpc, docs repo www/v11/docs/): client/links/httpBatchLink.md, client/links/httpLink.md. Every parameter name, default, error string and code sample left in this skill appears on those pages. Removed: the invented Verify step.

Method: documentation only; no commands were run.

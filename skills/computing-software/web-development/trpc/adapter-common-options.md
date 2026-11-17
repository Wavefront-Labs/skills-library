---
id: computing-software.web-development.trpc.adapter-common-options
name: adapter-common-options
category: computing-software
field: web-development
product: trpc
tags: [trpc, adapter, maxbatchsize, maxbodysize, allowbatching]
level: practitioner
status: docs-checked
description: "Options every HTTP adapter accepts (router, createContext, onError, responseMeta, allowBatching, maxBatchSize, allowMethodOverride) plus Node-only maxBodySize."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/adapters.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Every HTTP adapter takes these options next to its own (like `endpoint` for Fetch or `basePath` for Standalone):

- `router` (required) your app router.
- `createContext` creates the context for each request; it receives the adapter's own objects (for example `req` and `res`) plus `info`.
- `onError` is called with `{ error, type, path, input, ctx, req }` for every error.
- `responseMeta` returns `{ status, headers }` for the response, for example for caching.
- `allowBatching` set `false` to reject batch requests (default `true`).
- `maxBatchSize` rejects batch requests with more calls than this with `400 Bad Request`; set `maxItems` on your batch link to the same or lower value.
- `allowMethodOverride` accepts queries sent as POST, for clients that set `methodOverride: 'POST'` on their link (default `false`).

The Node.js adapters (Standalone, Express, Next.js) also accept `maxBodySize` and a connect-style `middleware(req, res, next)` that runs before tRPC (for example `cors()`).

```ts
createHTTPServer({
  router: appRouter,
  createContext: () => ({}),
  onError({ error, path }) { console.error(`tRPC error on '${path}':`, error); },
  maxBatchSize: 10,
  maxBodySize: 1024 * 1024, // 1 MiB
}).listen(3000);
```

## Checked

2026-11-04: read in full against the tRPC docs repo (trpc/trpc, docs repo www/v11/docs/): server/adapters.md (Common options, Request body size). Every parameter name, default, error string and code sample left in this skill appears on those pages. Removed: the invented Verify step.

Method: documentation only; no commands were run.

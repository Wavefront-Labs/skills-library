---
id: computing-software.web-development.trpc.batch-limits-url-length-and-size
name: batch-limits-url-length-and-size
category: computing-software
field: web-development
product: trpc
tags: [trpc, httpbatchlink, maxurllength, maxbatchsize, maxitems]
level: advanced
status: docs-checked
description: "Stop 413/414/404 errors from long batch URLs with maxURLLength, and align client maxItems with the server maxBatchSize to avoid 400 rejections."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/client/links/httpBatchLink.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Large batches can build very long URLs and fail with `413 Payload Too Large`, `414 URI Too Long` or `404 Not Found`. Two controls exist.

Client URL length:

```ts
httpBatchLink({
  url: 'http://localhost:3000',
  maxURLLength: 2083, // split the batch into several requests beyond this
  // methodOverride: 'POST', // alternative: send everything as POST
})
```

`methodOverride: 'POST'` also needs `allowMethodOverride: true` on the server adapter.

Batch size, in two halves:

1. Server: set `maxBatchSize` on any adapter. Requests with more operations are rejected with `400 Bad Request`.

```ts
createHTTPServer({ router: appRouter, maxBatchSize: 10 });
// Next.js: createNextApiHandler({ router: appRouter, maxBatchSize: 10 })
```

2. Client: set `maxItems` on the batch link to the same or a lower value so oversized batches are split automatically into several HTTP requests.

```ts
httpBatchLink({ url: 'http://localhost:3000', maxItems: 10 })
```

Both `maxURLLength` and `maxItems` default to `Infinity`, so nothing is limited until you set it. If the server sets `maxBatchSize` and the client does not set `maxItems`, large Promise.all bursts get rejected.

## Checked

2026-11-04: read in full against the tRPC docs repo (trpc/trpc, docs repo www/v11/docs/): client/links/httpBatchLink.md (options, Setting a maximum URL length, Limiting batch size), client/links.md (Common mistakes). Every parameter name, default, error string and code sample left in this skill appears on those pages. Removed: the invented Verify step.

Method: documentation only; no commands were run.

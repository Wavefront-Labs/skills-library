---
id: computing-software.web-development.trpc.request-body-size-limit
name: request-body-size-limit
category: computing-software
field: web-development
product: trpc
tags: [trpc, maxbodysize, security, payload-too-large, node]
level: advanced
status: docs-checked
description: "Set maxBodySize on Node adapters so one large request cannot exhaust memory; 413 PAYLOAD_TOO_LARGE, recommended 1 MiB, and when parsers take over."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/adapters.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Node.js adapters read the request body into memory, and `maxBodySize` is unset by default, so they accept bodies of any size. On an internet-facing server set `maxBodySize` so a single large request cannot exhaust the process memory. A body over the limit is rejected with `413 PAYLOAD_TOO_LARGE` as soon as it passes the limit, before it is parsed.

Recommended values from the docs: `1024 * 1024` (1 MiB) for typical JSON inputs. If you accept files or other large inputs, set it a little above the largest you expect and keep it under about `10 * 1024 * 1024` (10 MiB).

```ts
createHTTPServer({
  router: appRouter,
  maxBodySize: 1024 * 1024, // 1 MiB
}).listen(3000);
```

Caveat: `maxBodySize` only applies to bodies tRPC reads itself. If a body parser such as `express.json()` or the Next.js API routes body parser has already set `req.body`, limit the size in that parser instead. A limit in your reverse proxy (for example nginx `client_max_body_size`) adds another layer.

Pair with `maxBatchSize` to bound how many procedure calls one request can trigger.

## Checked

2026-11-07. Read in full from a clone of github.com/trpc/trpc (main, commit fe64009), www/v11/docs/server/adapters.md (read in full): the Node.js adapter options list, the "Request body size" section (no default limit, 413 PAYLOAD_TOO_LARGE before parsing, 1 MiB and about 10 MiB guidance, body-parser and reverse proxy caveat) and the maxBatchSize row of the common options table. Every claim matched the page text.

Removed or corrected: the invented Verify step (curl against a limit); no other claim needed changing.

Method: documentation only; no commands were run.

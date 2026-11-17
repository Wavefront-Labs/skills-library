---
id: computing-software.web-development.trpc.standalone-adapter-server
name: standalone-adapter-server
category: computing-software
field: web-development
product: trpc
tags: [trpc, standalone-adapter, createhttpserver, node, basepath]
level: intro
status: docs-checked
description: "Serve a router with createHTTPServer or createHTTPHandler, add a basePath, and run on HTTP/2 with createHTTP2Handler."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/adapters/standalone.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Standalone adapter wraps Node's `http.Server` and is the simplest way to get a project running.

```ts
import { createHTTPServer } from '@trpc/server/adapters/standalone';

createHTTPServer({
  router: appRouter,
  createContext() { return {}; },
  // basePath: '/trpc/', // optional, defaults to '/'
}).listen(2022);
```

`createHTTPServer` returns a standard `http.Server`, so all its APIs are available. When you need your own server logic, use `createHTTPHandler` and call `handler(req, res)` yourself:

```ts
const handler = createHTTPHandler({ router: appRouter, basePath: '/trpc/' });
createServer((req, res) => {
  if (req.url?.startsWith('/trpc/')) return handler(req, res);
  res.statusCode = 404;
  res.end('Not Found');
}).listen(3001);
```

`basePath` slices the prefix from the start of the request path. For HTTP/2 use `createHTTP2Handler` with `http2.createSecureServer({ key, cert }, (req, res) => handler(req, res))`; its context options type is `CreateHTTP2ContextOptions` with `req`, `res` and `info`.

Accepted options include everything in the common-options list plus `middleware`, `maxBodySize` and `basePath`.

## Checked

2026-11-07. Read in full from a clone of github.com/trpc/trpc (main, commit fe64009), www/v11/docs/server/adapters/standalone.md (read in full) and www/v11/docs/server/adapters.md (read in full, for the common options list): createHTTPServer snippet, basePath default, createHTTPHandler custom server, HTTP/2 handler with CreateHTTP2ContextOptions (req, res, info) and the options sentence. Every claim matched the page text.

Removed or corrected: the invented Verify step (curl against /getUser); no other claim needed changing.

Method: documentation only; no commands were run.

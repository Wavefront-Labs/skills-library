---
id: computing-software.web-development.trpc.standalone-cors-and-options
name: standalone-cors-and-options
category: computing-software
field: web-development
product: trpc
tags: [trpc, cors, options, standalone-adapter, middleware]
level: practitioner
status: docs-checked
description: "Handle browser CORS and OPTIONS preflight on the standalone adapter with the cors package passed as middleware, and when to switch to Express."
sources:
  - https://github.com/trpc/trpc/blob/main/www/v11/docs/server/adapters/standalone.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By default the standalone server does not answer HTTP OPTIONS requests or set CORS headers. A browser calling it from another origin sends a preflight OPTIONS request that gets no CORS headers, so the browser blocks the call. This is the single common mistake listed for the adapter.

Install `cors` (and its types) and pass it as `middleware`:

```ts
import cors from 'cors';

createHTTPServer({
  middleware: cors(),
  router: appRouter,
  createContext() { return {}; },
}).listen(3333);
```

`cors()` with no options throws open CORS to any request, which the docs call useful for development; configure it more strictly in production. The page's common-mistakes note says to pass `middleware: cors()` with the origins you allow.

The `middleware` option accepts any connect-style function so it is usable for more than CORS, but it is an escape hatch that does not compose multiple middlewares. For that: use the Express adapter, compose with `connect`, or extend `createHTTPHandler` in your own HTTP server.

## Checked

2026-11-07. Read in full from a clone of github.com/trpc/trpc (main, commit fe64009), www/v11/docs/server/adapters/standalone.md (read in full): "Handling CORS & OPTIONS", the middleware escape-hatch paragraph with its three alternatives, and "Common mistakes".

Removed or corrected: the `credentials` advice (not on the page) and the invented Verify step.

Method: documentation only; no commands were run.

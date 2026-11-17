---
id: computing-software.software-engineering.deno.http-server-serve-basics
name: http-server-serve-basics
category: computing-software
field: software-engineering
product: deno
tags: [http-server, deno-serve, request, response, urlpattern, static-files, streaming]
level: intro
status: docs-checked
description: "Write a Deno.serve HTTP server: handler, port, reading the request, JSON and streamed responses, URLPattern routing, serveDir and graceful shutdown."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/fundamentals/http_server.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
Deno.serve({ port: 4242, hostname: "0.0.0.0" }, (req) => {
  const url = new URL(req.url);
  return new Response(JSON.stringify({ path: url.pathname }), {
    status: 404,
    headers: { "content-type": "application/json; charset=utf-8" },
  });
});
```

Run with `deno run --allow-net server.ts`. Default port 8000; the handler may be async. Reading `req.text()`, `req.json()` etc. can fail if the client hangs up mid-body, so handle that.

Streaming bodies must define `cancel()` (called when the client disconnects) or messages queue until memory runs out.

Routing with `URLPattern`:

```ts
const userPattern = new URLPattern({ pathname: "/users/:id" });
Deno.serve((req) => {
  const match = userPattern.exec(req.url);
  if (match) return new Response(`User ${match.pathname.groups.id}`);
  return new Response("Not found", { status: 404 });
});
```

Static files (`deno run -N -R server.ts`): 

```ts
import { serveDir } from "jsr:@std/http/file-server";
Deno.serve((req) => serveDir(req, { fsRoot: "./public" }));
```

Graceful shutdown: `Deno.serve` returns an `HttpServer`; `shutdown()` stops new connections and lets in-flight requests finish.

```ts
const server = Deno.serve((_req) => new Response("Hello"));
Deno.addSignalListener("SIGINT", async () => { await server.shutdown(); });
```

You can also pass an `AbortSignal` via the `signal` option to tie the server's lifetime to other logic.

## Checked

2026-11-04: confirmed against the Deno docs Writing an HTTP Server page: Deno.serve handler and options, default port 8000, request body failure caution, 404 JSON response, stream cancel note, URLPattern routing, serveDir and permission flags, shutdown() and signal option.

Method: documentation only; no commands were run.

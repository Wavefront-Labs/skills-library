---
id: computing-software.software-engineering.d.d-vibed-http-server-and-router
name: d-vibed-http-server-and-router
category: computing-software
field: software-engineering
product: d
tags: [d-vibed-http-server-and-router, ecosystem-vibed, vibe-d, vibed, listenhttp, urlrouter, httpserversettings, fibers, event-loop, runapplication, rest, d]
level: practitioner
status: draft
description: "Start an HTTP server with listenHTTP and HTTPServerSettings, route with URLRouter, read request params and JSON, send responses, and understand fibers and the event loop."
sources:
  - https://dlang.org/spec/spec.html
  - https://dlang.org/phobos/index.html
  - https://dub.pm/
  - https://ddili.org/ders/d.en/index.html
  - https://dlang.org/articles.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# vibe.d basics: listenHTTP, URLRouter, request/response and async I/O

Goal: write a small HTTP service.

```d
import vibe.vibe;
void main() {
    auto router = new URLRouter;
    router.get("/hello/:name", (HTTPServerRequest req, HTTPServerResponse res) {
        res.writeBody("Hello, " ~ req.params["name"]);
    });
    router.post("/echo", (req, res) { res.writeJsonBody(req.json); });
    auto s = new HTTPServerSettings; s.port = 8080; s.bindAddresses = ["::1", "127.0.0.1"];
    listenHTTP(s, router);
    runApplication();
}
```
- dub: `dependency "vibe-d" version="~>0.10"`; `dub init myapp -t vibe.d` scaffolds it.
- Request: `req.query`, `req.params` (route), `req.form`, `req.json`, `req.headers`, `req.cookies`, `req.method`; response: `res.statusCode = 404`, `res.headers["X"]`, `res.writeJsonBody`, `res.redirect`, `res.render!("page.dt", var)` (Diet templates), static files `serveStaticFiles("public/")`.
- Concurrency model: each connection runs in a fiber on an event loop (libevent/libasync/vibe-core); blocking calls (`Thread.sleep`, blocking C libs) stall that thread's loop: use `vibe.core.core.sleep`, `runWorkerTask`, or `runTask`.
- Multi-core: `settings.options |= HTTPServerOption.reusePort` and `runWorkerTaskDist`, or `HTTPServerOption.distribute`.
- Client: `requestHTTP(url, (scope req) {...}, (scope res) {...})`; `vibe.http.client`.
- Config: `@path`/REST interface generator with `registerRestInterface(router, new Impl)`.

Gotchas:
- Handlers share thread-local state per worker thread; protect shared data with `shared`/locks.
- A fiber that `throw`s inside a handler results in 500; configure `errorPageHandler`.

Verify: `curl localhost:8080/hello/world`.

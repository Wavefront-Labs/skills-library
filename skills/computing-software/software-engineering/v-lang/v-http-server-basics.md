---
id: computing-software.software-engineering.v-lang.v-http-server-basics
name: v-http-server-basics
category: computing-software
field: software-engineering
product: v-lang
tags: [v-http-server-basics, net-http, http server, net.http.server, handler, routing, serve, listen_and_serve, request response, v-lang]
level: practitioner
status: draft
description: "Serve requests using http.Server and a Handler, route by path and method, parse queries and write responses."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Minimal HTTP server with net.http

Goal: stand up a small server without a framework.

```v
import net.http
struct App {}
fn (mut a App) handle(req http.Request) http.Response {
    return match req.url {
        '/' { http.new_response(status: .ok, body: 'hello') }
        else { http.new_response(status: .not_found, body: 'nope') }
    }
}
fn main() {
    mut s := http.Server{ addr: ':8080', handler: App{} }
    s.listen_and_serve()
}
```
- Interface is `http.Handler` with `handle(Request) Response`; confirm signature for your version.
- Parse query: `urllib.parse(req.url)!.query()`; method via `req.method`.
- For routing, templates and middleware use `veb` instead (see web skills).

Gotchas:
- Handler runs per request in parallel; guard shared state.
- Bind `127.0.0.1:port` for local-only services.

Verify: `curl localhost:8080/` returns hello.

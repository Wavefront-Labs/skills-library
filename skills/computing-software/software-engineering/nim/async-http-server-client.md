---
id: computing-software.software-engineering.nim.async-http-server-client
name: async-http-server-client
category: computing-software
field: software-engineering
product: nim
tags: [async-http-server-client, async-programming, asynchttpserver, asynchttpclient, http-server, request, respond, async-networking, nim]
level: practitioner
status: docs-checked
description: "Serve requests with asynchttpserver and call APIs with AsyncHttpClient, handling headers and bodies."
sources:
  - https://nim-lang.org/docs/asynchttpserver.html
  - https://nim-lang.org/docs/httpclient.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Async HTTP server and client

Goal: write a small async HTTP service.

```nim
import std/[asynchttpserver, asyncdispatch]
proc cb(req: Request) {.async, gcsafe.} =
  await req.respond(Http200, "hello", newHttpHeaders([("Content-Type","text/plain")]))
let server = newAsyncHttpServer()
waitFor server.serve(Port(8080), cb)
```
- `req.url.path`, `req.reqMethod`, `req.headers`, `req.body` describe the request.
- Client: `let c = newAsyncHttpClient(); let r = await c.get(url); echo await r.body; c.close()`.
- HTTPS needs `-d:ssl` and OpenSSL available.

Gotchas:
- The callback is `proc (req: Request) {.async, gcsafe.}`; `serve` takes the port and that callback.
- Close clients with `close()` when done.

Verify: `curl localhost:8080` returns hello.

## Checked

2026-11-03. Confirmed against the asynchttpserver and httpclient pages: newAsyncHttpServer, serve(port, callback), Request url/reqMethod/headers/body, respond, newHttpHeaders, newAsyncHttpClient, `-d:ssl` and OpenSSL for HTTPS. Removed: the Jester/Prologue/Mummy recommendation (maintenance not verified) and the respond-exactly-once claim.

Method: documentation only; no commands were run.

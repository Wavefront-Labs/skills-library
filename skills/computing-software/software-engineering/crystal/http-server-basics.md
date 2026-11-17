---
id: computing-software.software-engineering.crystal.http-server-basics
name: http-server-basics
category: computing-software
field: software-engineering
product: crystal
tags: [http-server-basics, http-server-client, http-server, http-handler, request, response, listen, bind-tcp, handler-chain, log-handler, error-handler, static-file-handler, crystal]
level: practitioner
status: docs-checked
description: "Create an HTTP::Server with a block or handler chain, read request path, headers and body, and write responses."
sources:
  - https://crystal-lang.org/api/latest/HTTP/Server.html
  - https://crystal-lang.org/api/latest/HTTP/Server/Response.html
  - https://crystal-lang.org/api/latest/HTTP/Request.html
  - https://crystal-lang.org/api/latest/HTTP/Handler.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HTTP::Server and handlers

Goal: serve HTTP from stdlib.

```crystal
require "http/server"
server = HTTP::Server.new([HTTP::ErrorHandler.new, HTTP::LogHandler.new]) do |ctx|
  ctx.response.content_type = "text/plain"
  ctx.response.print "hi #{ctx.request.path}"
end
server.bind_tcp "0.0.0.0", 8080
server.listen
```
- `ctx.request` has `method`, `path`, `query_params`, `headers`, `body` (`IO | Nil`) and `cookies`; `ctx.response` has `status_code=`, `headers`, `content_type=`, `cookies`, `respond_with_status(status, message = nil)` and `redirect(location, status = :found)`. The response is a write-only IO, so `print`, `puts` and `write` send the body; once output has been written, changing status and headers has no effect.
- Custom handler: `require "http/server/handler"`, `include HTTP::Handler`, implement `call(context)` and call `call_next(context)` to continue the chain.
- Built-in handlers that include `HTTP::Handler`: `CompressHandler`, `ErrorHandler`, `LogHandler`, `StaticFileHandler`, `WebSocketHandler`. The docs describe `ErrorHandler` as returning a 500 for exceptions raised by later handlers.
- `HTTP::Server.new` takes a block, a handler, an array of handlers, or an array plus a final block.
- Each connection is processed concurrently in its own fiber and can serve several request-response cycles with keep-alive. `server.close` gracefully terminates the server: it stops accepting new connections and does not wait for requests in progress; `listen` blocks until the server is closed.

Gotchas:
- Connection reuse requires the handler chain to consume the whole request body; otherwise the connection is closed.
- `bind_tcp(port)` binds 127.0.0.1; pass a host such as `"0.0.0.0"` to listen on all interfaces. `reuse_port: true` sets `SO_REUSEPORT` so several processes can bind the same port.
- TLS: `server.bind_tls host, port, context` with an `OpenSSL::SSL::Context::Server` that has `certificate_chain=` and `private_key=` set.
- `server.max_headers_size` and `max_request_line_size` can be changed; a request whose headers exceed the limit gets status 432.

Verify: `curl localhost:8080/x` prints `hi /x`.

## Checked

Checked 2026-11-08 against the API pages for HTTP::Server, HTTP::Server::Response, HTTP::Request and HTTP::Handler (Crystal 1.22.2 docs). Removed: the claim that the body must be read before responding for large uploads (the page says the body must be consumed for connection reuse) and the `HTTP::Server::Context` TLS mention.

Method: docs-only read of cited pages, 2026-11-08

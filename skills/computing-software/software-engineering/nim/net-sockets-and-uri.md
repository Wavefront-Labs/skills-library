---
id: computing-software.software-engineering.nim.net-sockets-and-uri
name: net-sockets-and-uri
category: computing-software
field: software-engineering
product: nim
tags: [net-sockets-and-uri, stdlib-net-httpclient, net, socket, tcp, uri, parseuri, encodeurl, newsocket, listen, accept, nim]
level: practitioner
status: docs-checked
description: "Use TCP sockets from std/net, parse and build URLs with std/uri, and encode query strings."
sources:
  - https://nim-lang.org/docs/net.html
  - https://nim-lang.org/docs/uri.html
  - https://nim-lang.org/docs/lib.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# net sockets and std/uri parsing

Goal: low-level networking and URL handling.

- TCP client: `let s = newSocket(); s.connect("host", Port(80)); s.send("..."); let line = s.recvLine(); s.close()`.
- Server: `s.bindAddr(Port(9000)); s.listen(); var client: Socket; s.accept(client)`; `std/selectors` provides a selector API.
- Timeouts: `s.recv(data, size, timeout = ms)` fills a `var string`, or `s.recv(size, timeout = ms)` returns a string; `recvLine(timeout = ...)` and `connect(address, port, timeout)` also take a timeout (milliseconds).
- TLS: `newContext()` + `wrapSocket(ctx, socket)`; compile with `-d:ssl`.
- URLs: `import std/uri`; `let u = parseUri("https://a.b/c?x=1")`, `u.hostname`, `u.path`, `u.query`; build with `/` and `$u`; `encodeUrl`, `decodeUrl`, `encodeQuery(@[("a","b")])`, `decodeQuery`.
- Async variant: `std/asyncnet`.

Gotchas:
- Always `close` sockets (defer).
- TCP streams have no message boundaries, so frame data yourself.

Verify: a loopback echo server/client round-trips a line.

## Checked

2026-11-03. Confirmed against the net, uri and lib pages: newSocket/connect/send/recvLine, bindAddr, listen, accept, recv overloads with timeout, newContext, wrapSocket, -d:ssl, selectors, asyncnet, Uri fields hostname/path/query, parseUri, `/` operator, encodeUrl, decodeUrl, encodeQuery, decodeQuery. Real error fixed: `recv(buf, n, timeout=ms)` did not match any recv signature. Removed the non-blocking claim.

Method: documentation only; no commands were run.

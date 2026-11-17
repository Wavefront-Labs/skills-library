---
id: computing-software.software-engineering.zig.http-client-server
name: http-client-server
category: computing-software
field: software-engineering
product: zig
tags: [zig, http-client-server, zig-std-net-http, std-http, http-client, http-server, tls]
level: advanced
status: draft
description: "Fetch URLs with std.http.Client and build a minimal HTTP server with std.http.Server in Zig, noting TLS and API churn."
sources:
  - https://ziglang.org/documentation/master/std/
  - https://zig.guide/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# HTTP client and server in std.http
**Goal:** make requests and serve simple endpoints with the standard library.

```zig
var client = std.http.Client{ .allocator = alloc };
defer client.deinit();
var body = std.ArrayList(u8).init(alloc);           // 0.14 style; changes in 0.15 (unconfirmed)
defer body.deinit();
const res = try client.fetch(.{
    .location = .{ .url = "https://example.com/" },
    .response_storage = .{ .dynamic = &body },
});
std.debug.print("{d}\n", .{@intFromEnum(res.status)});
```
- `std.http.Client` includes TLS (`std.crypto.tls`) and a certificate bundle (`std.crypto.Certificate.Bundle`) loaded from the OS.
- `std.http.Server` parses requests on a connection: `var server = std.http.Server.init(connection, &read_buffer); var req = try server.receiveHead(); try req.respond("hello", .{});` (signatures changed in 0.12 and 0.15; unconfirmed).
- The fetch/server API shifted notably between releases; read the std docs for your version and keep calls behind a thin wrapper.
- For production servers evaluate ecosystem packages (e.g. `httpz`, `zap`; unconfirmed APIs) that supply routing, pooling and keep-alive.

## Gotchas
- std.http is minimal: no HTTP/2, limited server features (unconfirmed for latest).
- Set size limits on headers and bodies when serving.
- Redirect handling and decompression have options; check defaults.

## Self-check
Fetch a URL on localhost served by `python -m http.server`, print status and body length.

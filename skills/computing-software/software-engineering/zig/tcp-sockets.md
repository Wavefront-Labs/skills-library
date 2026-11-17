---
id: computing-software.software-engineering.zig.tcp-sockets
name: tcp-sockets
category: computing-software
field: software-engineering
product: zig
tags: [zig, tcp-sockets, zig-std-net-http, std-net, address-listen, accept, tcp-client]
level: advanced
status: docs-checked
description: "Open TCP listeners and connections in Zig with std.net.Address, listen, accept and connectToHost, and handle partial reads and writes."
sources:
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/net.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/posix.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TCP servers and clients with std.net
**Goal:** build a simple blocking TCP service.

```zig
const addr = try std.net.Address.parseIp("127.0.0.1", 9000);
var server = try addr.listen(.{ .reuse_address = true });
defer server.deinit();
while (true) {
    const conn = try server.accept();            // blocks
    defer conn.stream.close();
    var buf: [1024]u8 = undefined;
    const n = try conn.stream.read(&buf);
    try conn.stream.writeAll(buf[0..n]);         // echo
}

const s = try std.net.tcpConnectToHost(alloc, "example.com", 80);
defer s.close();
```
- `std.net.Stream` has `read`, `write`, `writeAll` and `close`; `Server` has `accept` and `deinit`.
- `ListenOptions.reuse_address` (default false) sets SO_REUSEADDR (on Windows the roughly equivalent option).
- `std.Thread.Pool` exists in `std/Thread/Pool.zig` for thread-per-task designs.
- Lower level: `std.posix.socket`, `bind`, `listen`, `poll`, `setsockopt`.
- The language reference says async functions regressed in 0.11.0 and are planned to return as a low-level primitive that powers I/O implementations.

## Gotchas
- The echo loop handles one connection at a time.

## Self-check
Run the echo server, connect with `nc 127.0.0.1 9000`, type a line and see it echoed.

## Checked
2026-11-02. Confirmed in 0.15.1 `lib/std/net.zig` (`Address.parseIp`, `listen`, `ListenOptions.reuse_address`, `Server.accept/deinit`, `Stream` methods, `tcpConnectToHost`, WinSock startup), `lib/std/posix.zig` and the language reference (Async Functions).
Removed: partial read/EOF semantics, thread-per-connection advice, `std.Io` interface claim, ecosystem event-loop packages, RCVTIMEO timeout recipe, `error.AddressInUse` behaviour.
Method: documentation only; no commands were run.

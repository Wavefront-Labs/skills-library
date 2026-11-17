---
id: computing-software.software-engineering.v-lang.v-net-sockets-tcp-udp
name: v-net-sockets-tcp-udp
category: computing-software
field: software-engineering
product: v-lang
tags: [v-net-sockets-tcp-udp, net-http, net, tcp, udp, socket, dial_tcp, listen_tcp, accept, tcp listener, net.tcpconn, v-lang]
level: advanced
status: docs-checked
description: "Open TCP connections and listeners with net.dial_tcp and net.listen_tcp, read and write, set timeouts, and use UDP."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TCP and UDP sockets with net

Goal: write low-level network clients and servers.

- Client: `mut c := net.dial_tcp('127.0.0.1:9000')!; defer { c.close() or {} }; c.write_string('ping\n')!; mut buf := []u8{len: 1024}; n := c.read(mut buf)!`.
- Server: `mut l := net.listen_tcp(.ip, ':9000')!; for { mut conn := l.accept()!; spawn handle(mut conn) }`.
- Timeouts: `c.set_read_timeout(5 * time.second)`, `set_write_timeout`.
- UDP: `net.listen_udp(':9001')!`, `net.dial_udp(addr)!` (both return `&UdpConn`).
- Resolution: `net.resolve_addrs(host, .ip, .tcp)!`.
- Line protocol: wrap with `io.new_buffered_reader(reader: conn)` and `read_line()`.

Gotchas:
- Close each connection in the handler that owns it; `defer` helps.
- `read` fills up to `buf.len` bytes, so a message can arrive in several reads; implement framing.

Verify: echo server test with client sending and receiving a line.

## Checked

2026-11-03. Confirmed against the V repository source (vlib modules and doc/docs.md) read in this batch: net.dial_tcp(address) !&TcpConn, net.listen_tcp(family, saddr, options) !&TcpListener, TcpListener.accept, TcpConn set_read_timeout/set_write_timeout/write_string, listen_udp and dial_udp returning !&UdpConn, resolve_addrs(addr, family, typ), io.new_buffered_reader (vlib/net, vlib/io).
Removed or corrected: UDP `read`/`write_to` detail (only RawConn.write_to was confirmed) and the unverified scaling claim about threads per connection.
Method: documentation only; no commands were run.

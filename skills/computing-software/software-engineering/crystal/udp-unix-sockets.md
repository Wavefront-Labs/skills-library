---
id: computing-software.software-engineering.crystal.udp-unix-sockets
name: udp-unix-sockets
category: computing-software
field: software-engineering
product: crystal
tags: [udp-unix-sockets, sockets, udp, udpsocket, unix-socket, unixserver, tls, openssl, ssl-socket, datagram, ipc, crystal]
level: advanced
status: draft
description: "Use UDP datagrams, Unix domain sockets and wrap TCP in TLS with OpenSSL::SSL::Socket for client and server."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# UDPSocket, UNIXSocket and TLS

Goal: other transports.

- UDP: `s = UDPSocket.new; s.bind("0.0.0.0", 5000); msg, addr = s.receive; s.send("pong", addr)`; client `s.connect(host, port); s.send "x"`.
- Unix: `UNIXServer.new("/tmp/app.sock")` then `accept`; `UNIXSocket.new(path)`; remove the stale socket file at startup.
- TLS client: `ctx = OpenSSL::SSL::Context::Client.new; ssl = OpenSSL::SSL::Socket::Client.new(tcp, ctx, hostname: host)`; verification mode `ctx.verify_mode = OpenSSL::SSL::VerifyMode::PEER` (default verify on in recent versions; confirm).
- TLS server: `OpenSSL::SSL::Context::Server.new`, `ctx.certificate_chain = path`, `ctx.private_key = path`.

Gotchas:
- UDP gives no delivery or ordering; use datagram size limits.
- Never disable certificate verification in production.
- Keep keys outside source control.

Verify: UDP echo round trip on localhost.

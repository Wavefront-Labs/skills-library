---
id: computing-software.software-engineering.ktor.ktor-raw-sockets
name: ktor-raw-sockets
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, sockets, tcp, udp, tls, kotlin, networking]
level: advanced
status: docs-checked
description: "Use Ktor raw TCP/UDP sockets: SelectorManager, bind/accept servers, connect clients, read/write channels, optional TLS via ktor-network-tls, and cleanup."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-sockets.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ktor raw TCP/UDP sockets

Ktor exposes TCP and UDP raw sockets through a suspending API built on java.nio. The page flags the sockets API as experimental, expected to evolve with potentially breaking changes.

Dependencies: `io.ktor:ktor-network`; for client TLS also `io.ktor:ktor-network-tls`.

## Server

1. Create a `SelectorManager`, call `SocketBuilder.tcp()` (from `aSocket(selectorManager)`), then `bind` to a port. The result is a `ServerSocket`. For UDP use `SocketBuilder.udp()`.
2. Call `ServerSocket.accept` to get a connected `Socket`.
3. Receive: `Socket.openReadChannel()` returns a `ByteReadChannel`; e.g. `readUTF8Line`.
4. Send: `Socket.openWriteChannel()` returns a `ByteWriteChannel`; e.g. `writeStringUtf8`.
5. Release resources with `Socket.close`.

## Client

1. Create a `SelectorManager`, call `SocketBuilder.tcp()`, then `connect` to get a connected `Socket`.
2. Read/write with the same `openReadChannel` / `openWriteChannel` calls as the server.
3. Close with both `Socket.close` and `SelectorManager.close`.

## Secure client socket (TLS)

Add `ktor-network-tls`, then call `tls()` on the connection:

```kotlin
val selectorManager = SelectorManager(Dispatchers.IO)
val socket = aSocket(selectorManager).tcp().connect("127.0.0.1", 8443).tls()
```

`tls` accepts a block to adjust parameters exposed by `TLSConfigBuilder`.

## Notes

- `ByteReadChannel` / `ByteWriteChannel` are asynchronous; call them from coroutines.
- Secure sockets are described for the client side only on this page.
- Native server targets are listed as supported.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-sockets.md.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.

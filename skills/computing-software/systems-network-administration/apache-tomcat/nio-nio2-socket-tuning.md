---
id: computing-software.systems-network-administration.apache-tomcat.nio-nio2-socket-tuning
name: nio-nio2-socket-tuning
category: computing-software
field: systems-network-administration
product: apache-tomcat
tags: [computing-software, systems-network-administration, apache-tomcat, tomcat, nio, nio2, connector-protocol, socket-buffers, usesendfile, selectortimeout, http11nioprotocol, apr]
level: advanced
status: docs-checked
description: "Choose and tune the Tomcat 10.1 NIO or NIO2 HTTP protocol handler: protocol class names, socket buffer attributes, sendfile, poller settings and OpenSSL vs JSSE selection."
sources:
  - https://tomcat.apache.org/tomcat-10.1-doc/config/http.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# NIO / NIO2 protocol handlers

Protocol values:
- `HTTP/1.1` (default) = NIO, class `org.apache.coyote.http11.Http11NioProtocol`.
- `org.apache.coyote.http11.Http11Nio2Protocol` = NIO2.
- This page defines no APR protocol value; the native library only changes the default SSL implementation to OpenSSL.

Both: non-blocking header read, keep-alive wait and TLS handshake; blocking body read and response write; limited by `maxConnections`; support Java SSL or OpenSSL.

Tuning attributes:

| Attribute | Default |
|---|---|
| `useSendfile` | true |
| `socket.appReadBufSize` / `socket.appWriteBufSize` | 8192 |
| `socket.directBuffer` / `socket.directSslBuffer` | false |
| `socket.bufferPool` | NIO -2 (computed); NIO2 500 |
| `socket.processorCache` | 0 |
| `socket.eventCache` (NIO) | 0 |
| `socket.bufferPoolSize` (NIO) | -2 (computed) |
| `pollerThreadPriority` (NIO) | 5 |
| `selectorTimeout` (NIO) | 1000 ms |
| `sniParseLimit` | 65536 |
| `socket.unlockTimeout` | 250 ms |
| `useInheritedChannel` (NIO) | false |
| `asyncTimeout` | 30000 ms |

Notes:
- Sendfile beats compression for static files above 48 KiB (see `computing-software.systems-network-administration.apache-tomcat.http-response-compression`).
- `sslImplementationName` defaults to JSSE; becomes OpenSSL when tomcat-native is installed.
- Only change buffer attributes after measuring; the defaults suit most sites.

## Checked

2026-11-04. Read the Tomcat 10.1 HTTP Connector page (config/http.html) and confirmed protocol class names, the NIO versus NIO2 comparison rows, every default in the tuning table, the 48 KiB sendfile note and sslImplementationName behaviour. Removed the startup log handler-name claim, which the page does not state.

Method: documentation only; no commands were run.

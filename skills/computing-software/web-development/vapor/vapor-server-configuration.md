---
id: computing-software.web-development.vapor.vapor-server-configuration
name: vapor-server-configuration
category: computing-software
field: web-development
product: vapor
tags: [vapor,server-configuration,http-server,port,hostname,compression,http2,swift]
level: advanced
status: docs-checked
description: "Configure Vapor's built-in HTTP server via app.http.server.configuration: hostname, port, backlog, compression, pipelining, HTTP versions and server name."
sources:
  - https://docs.vapor.codes/advanced/server/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: tune Vapor's default HTTP server (SwiftNIO-based; HTTP/1, HTTP/2, upgrades like WebSockets) through `app.http.server.configuration`.

| Option | Default | Notes |
|---|---|---|
| `hostname` | `127.0.0.1` | address to accept connections on |
| `port` | `8080` | `sudo` may be needed below 1024; above 65535 unsupported |
| `backlog` | `256` | max pending-connection queue length |
| `reuseAddress` | `true` | reuse of local addresses |
| `tcpNoDelay` | `true` | minimise TCP packet delay |
| `responseCompression` | `.disabled` | gzip; `.enabled(initialByteBufferCapacity: 1024)` sets initial buffer |
| `requestDecompression` | `.disabled` | gzip; `limit` default `.ratio(10)` |
| `supportPipelining` | `false` | HTTP pipelining |
| `supportVersions` | HTTP/1 and HTTP/2 with TLS; HTTP/1 only without | e.g. `[.two]` |
| `tlsConfiguration` | `nil` | see the TLS skill |
| `serverName` | `nil` | value of the outgoing `Server` header |

```swift
app.http.server.configuration.hostname = "dev.local"
app.http.server.configuration.port = 1337
app.http.server.configuration.backlog = 128
app.http.server.configuration.responseCompression = .enabled
app.http.server.configuration.requestDecompression = .enabled
app.http.server.configuration.supportPipelining = true
app.http.server.configuration.supportVersions = [.two]
app.http.server.configuration.serverName = "vapor"
```

Decompression limit options: `size` (max decompressed bytes), `ratio` (max as ratio of compressed bytes), `none`. Example with no limit: `.enabled(limit: .none)`. The docs note limits help stop maliciously compressed requests using large memory.

Hostname and port set here can be overridden by the `serve` command flags (`--hostname`/`-H`, `--port`/`-p`) or by parameters to `app.server.start(...)`.

Related: computing-software.web-development.vapor.vapor-server-tls-serve-command

## Checked

2026-11-08: read in full the Server page at docs.vapor.codes/advanced/server/ (every option and default in the table, decompression limit options, serve flag overrides). Every claim was found on the cited pages; nothing needed removing.

Method: docs-only read of cited pages, 2026-11-08

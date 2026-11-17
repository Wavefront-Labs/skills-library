---
id: computing-software.web-development.vapor.vapor-server-tls-serve-command
name: vapor-server-tls-serve-command
category: computing-software
field: web-development
product: vapor
tags: [vapor,vapor-tls,tls,serve-command,server-configuration,graceful-shutdown,swift]
level: advanced
status: docs-checked
description: "Enable TLS on Vapor's server, use serve flags (-H, -p, -b), start the server manually, and plug in a custom Server implementation."
sources:
  - https://docs.vapor.codes/advanced/server/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: enable TLS, control the `serve` command, start the server manually, or replace the server.

**TLS.** Set `tlsConfiguration` (default `nil`). Add `import NIOSSL` to the configuration file; you may also need NIOSSL as a dependency in Package.swift.

```swift
app.http.server.configuration.tlsConfiguration = .makeServerConfiguration(
    certificateChain: try NIOSSLCertificate.fromPEMFile("/path/to/cert.pem").map { .certificate($0) },
    privateKey: .privateKey(try NIOSSLPrivateKey(file: "/path/to/key.pem", format: .pem))
)
```

**Serve command.** `swift run App serve` (runs by default if no command is given). Parameters:

- `--hostname` / `-H`: override configured hostname
- `--port` / `-p`: override configured port
- `--bind` / `-b`: hostname and port joined by `:`

```sh
swift run App serve -b 0.0.0.0:80
```

`swift run App serve --help` lists more. The command listens for `SIGTERM` and `SIGINT` to shut down gracefully (ctrl+c sends `SIGINT`). At log level `debug` or lower, graceful-shutdown status is logged.

**Manual start.**

```swift
try app.server.start()
app.server.shutdown()
try app.server.onShutdown.wait()
```

**Custom server.** The default is `app.servers.use(.http)`. Any type conforming to `Server` can replace it:

```swift
app.servers.use { app in
    MyServer()
}
```

For leading-dot syntax, extend `Application.Servers.Provider`:

```swift
extension Application.Servers.Provider {
    static var myServer: Self {
        .init {
            $0.servers.use { app in
                MyServer()
            }
        }
    }
}

app.servers.use(.myServer)
```

Related: computing-software.web-development.vapor.vapor-server-configuration

## Checked
Read the whole Server page (vapor/docs, docs/4.0/advanced/server.md, source of the cited page) on 2026-11-08. Confirmed the TLS configuration and NIOSSL import, serve parameters and example, `--help`, SIGTERM/SIGINT graceful shutdown and debug logging, manual start, `app.servers.use(.http)` and the custom server and Provider forms. No claims removed.
Method: docs-only read of cited pages, 2026-11-08

---
id: computing-software.software-engineering.ktor.ktor-forward-headers
name: ktor-forward-headers
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, reverse-proxy, x-forwarded-for, forwarded-header, request-origin, kotlin-server]
level: advanced
status: docs-checked
description: "Recover the original client request behind a reverse proxy in Ktor using ForwardedHeaders or XForwardedHeaders and call.request.origin, including multi-proxy IP selection."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-forward-headers.md
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/forwarded-header/src/main/kotlin/com/example/Application.kt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Read original request info behind a proxy in Ktor

Install `ForwardedHeaders` or `XForwardedHeaders` (artifact `io.ktor:ktor-server-forwarded-header`) when Ktor sits behind a reverse proxy. Pick one by header family:

- `ForwardedHeaders` handles the `Forwarded` header (RFC 7239).
- `XForwardedHeaders` handles `X-Forwarded-Host`/`X-Forwarded-Server`, `X-Forwarded-For`, `X-Forwarded-By`, `X-Forwarded-Proto`/`X-Forwarded-Protocol`, and `X-Forwarded-SSL`/`Front-End-Https`.

Security: to prevent header manipulation, install these only if the application accepts connections from the reverse proxy alone.

```kotlin
fun Application.module() {
    install(ForwardedHeaders)
    install(XForwardedHeaders) {
        useFirstProxy()
    }
    routing {
        get("/hello") {
            val remoteHost = call.request.local.remoteHost
            val serverHost = call.request.local.serverHost
            val originRemoteHost = call.request.origin.remoteHost
            val originServerHost = call.request.origin.serverHost
            call.respondText("remoteHost: $remoteHost, originRemoteHost: $originRemoteHost\n" +
                    "serverHost: $serverHost, originServerHost: $originServerHost"
            )
        }
    }
}
```

`origin` needs `import io.ktor.server.plugins.*`; the plugins are in `io.ktor.server.plugins.forwardedheaders.*`.

## Reading values

- `call.request.local` describes the proxy connection.
- `call.request.origin` describes the original request once a plugin is installed.

With the plugin, `origin.serverHost` becomes the proxy and `origin.remoteHost` becomes the client; without it `remoteHost` is the proxy. `localHost`, `localPort` and `remotePort` are the same either way.

## Multiple proxies

`X-Forwarded-For` lists `<client>, <proxy1>, <proxy2>`. By default `XForwardedHeaders` puts the first entry in `call.request.origin.remoteHost`. Customize with `XForwardedHeadersConfig`:

- `useFirstProxy` / `useLastProxy`: take the first or last entry.
- `skipLastProxies`: skip N entries from the right and take the next. With 3 and `10.0.0.123, proxy-1, proxy-2, proxy-3`, the result is `10.0.0.123`.
- `skipKnownProxies`: remove listed entries and take the last remaining. Passing `listOf("proxy-1", "proxy-3")` on the same header yields `proxy-2`.
- `extractEdgeProxy`: custom extraction logic for the `X-Forward-*` headers.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-forward-headers.md, codeSnippets/snippets/forwarded-header/src/main/kotlin/com/example/Application.kt.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.

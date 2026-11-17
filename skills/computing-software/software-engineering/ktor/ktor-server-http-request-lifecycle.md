---
id: computing-software.software-engineering.ktor.ktor-server-http-request-lifecycle
name: ktor-server-http-request-lifecycle
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, httprequestlifecycle, cancellation, coroutines, client-disconnect, netty]
level: advanced
status: docs-checked
description: "Cancel Ktor request handling when the client disconnects using the HttpRequestLifecycle plugin and cancelCallOnClose, handling CancellationException and engine limits."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-http-request-lifecycle.md
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/server-http-request-lifecycle/src/main/kotlin/com/example/Application.kt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cancel work on client disconnect with HttpRequestLifecycle

By default Ktor keeps processing a request after the client disconnects. The `HttpRequestLifecycle` plugin (in `io.ktor:ktor-server-core`) cancels processing as soon as the client goes away, which helps long-running or resource-intensive requests.

Supported engines: `Netty` and `CIO`. Native server is not supported.

## Install

Install in the application module and set `cancelCallOnClose`:

```kotlin
import io.ktor.server.http.HttpRequestLifecycle

fun Application.module() {
    install(HttpRequestLifecycle) {
        cancelCallOnClose = true
    }
    // routing { ... }
}
```

With `cancelCallOnClose` enabled the plugin installs a cancellation handler per request. When a client disconnects only the coroutine handling that route is canceled. Cancellation propagates through structured concurrency: child coroutines started with `launch` or `async` are canceled too, and a `CancellationException` is thrown at the next suspension point.

## Clean up on cancellation

Catch `CancellationException` in the handler to release resources or stop background work, as in the page's example:

```kotlin
routing {
    get("/long-process") {
        try {
            while (isActive) {
                delay(10_000)
                log.info("Very important work.")
            }
            call.respond("Completed")
        } catch (e: CancellationException) {
            log.info("Cleaning up resources.")
        }
    }
}
```

## Gotchas

- Coroutine cancellation is cooperative. Blocking or CPU-bound code is not interrupted automatically; for long-running work call `call.coroutineContext.ensureActive()` so it reacts to cancellation.
- Servlet-based and other unsupported engines cannot reliably detect client disconnects; cancellation is only detected when the server tries to write the response.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-http-request-lifecycle.md, codeSnippets/snippets/server-http-request-lifecycle/src/main/kotlin/com/example/Application.kt.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.

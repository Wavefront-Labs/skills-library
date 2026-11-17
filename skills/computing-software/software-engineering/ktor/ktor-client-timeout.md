---
id: computing-software.software-engineering.ktor.ktor-client-timeout
name: ktor-client-timeout
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, kotlin, http-client, timeout, httptimeout, plugin]
level: intro
status: docs-checked
description: "Configure request, connect and socket timeouts with the Ktor client HttpTimeout plugin, globally or per request, and know which engines support which timeout."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/client-timeout.md
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/client-timeout/src/main/kotlin/com/example/Application.kt
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/client-request-retry.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ktor client timeouts (HttpTimeout)

`HttpTimeout` needs only `ktor-client-core`. It covers three timeouts:

- Request timeout: the whole HTTP call, from sending the request to receiving the response (`requestTimeoutMillis`).
- Connection timeout: establishing a connection with the server (`connectTimeoutMillis`).
- Socket timeout: maximum inactivity between two data packets (`socketTimeoutMillis`).

## Install for all requests

```kotlin
val client = HttpClient(CIO) {
    install(HttpTimeout) {
        requestTimeoutMillis = 1000
    }
}
```

Imports used on the page: `io.ktor.client.*`, `io.ktor.client.engine.cio.*`, `io.ktor.client.plugins.*`.

## Override for one request

Use the `HttpRequestBuilder.timeout { ... }` property inside the request. Timeouts set on a specific request override the global ones from `install`:

```kotlin
val response: HttpResponse = client.get("http://0.0.0.0:8080/path1") {
    timeout {
        requestTimeoutMillis = 3000
    }
}
```

## Failures

A timeout surfaces as `HttpRequestTimeoutException`, `ConnectTimeoutException` or `SocketTimeoutException`.

## Engine limitations

| Engine | Request | Connect | Socket |
|---|---|---|---|
| Darwin | yes | no | yes |
| JavaScript | yes | no | no |
| Curl | yes | yes | no |
| MockEngine | yes | no | yes |

If you also use `HttpRequestRetry` and want retries on timeouts, install `HttpRequestRetry` before `HttpTimeout`.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/client-timeout.md, codeSnippets/snippets/client-timeout/src/main/kotlin/com/example/Application.kt, topics/client-request-retry.md.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages. Added client-request-retry.md to sources (it confirms installing HttpRequestRetry before HttpTimeout).

Method: documentation only; no commands were run.

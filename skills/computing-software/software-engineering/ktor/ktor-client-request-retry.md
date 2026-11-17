---
id: computing-software.software-engineering.ktor.ktor-client-request-retry
name: ktor-client-request-retry
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, kotlin, http-client, retry, httprequestretry, backoff]
level: practitioner
status: docs-checked
description: "Retry failed Ktor client requests with HttpRequestRetry: retryOnServerErrors, exponentialDelay, retryIf, retryOnExceptionIf, delayMillis, modifyRequest, and HttpTimeout order."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/client-request-retry.md
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/client-retry/src/main/kotlin/com/example/Application.kt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Retrying failed requests in the Ktor client

By default the client does not retry requests that fail from network or server errors. The `HttpRequestRetry` plugin (only `ktor-client-core` needed) adds a retry policy: number of retries, retry conditions, and request changes before retrying.

## Install

```kotlin
val client = HttpClient(CIO) {
    install(HttpRequestRetry)
}
```

If you also use `HttpTimeout` and want retries on timeouts, install `HttpRequestRetry` first:

```kotlin
val client = HttpClient(CIO) {
    install(HttpRequestRetry) // Should be installed before HttpTimeout
    install(HttpTimeout) { /* ... */ }
}
```

## Basic policy

```kotlin
val client = HttpClient(CIO) {
    install(HttpRequestRetry) {
        retryOnServerErrors(maxRetries = 5)
        exponentialDelay()
    }
}
```

- `retryOnServerErrors`: retry when the server returns a `5xx` response, up to the given number of retries.
- `exponentialDelay`: delay between retries calculated with the exponential backoff algorithm.

## Custom conditions and delay

```kotlin
install(HttpRequestRetry) {
    maxRetries = 5
    retryIf { request, response -> !response.status.isSuccess() }
    retryOnExceptionIf { request, cause -> cause is NetworkError }
    delayMillis { retry -> retry * 3000L }   // retries in 3, 6, 9, etc. seconds
}
```

## Modify the request before retrying

```kotlin
install(HttpRequestRetry) {
    modifyRequest { request ->
        request.headers.append("x-retry-count", retryCount.toString())
    }
}
```

Other options are listed in `HttpRequestRetryConfig` in the API reference.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/client-request-retry.md, codeSnippets/snippets/client-retry/src/main/kotlin/com/example/Application.kt.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.

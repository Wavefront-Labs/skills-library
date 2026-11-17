---
id: computing-software.software-engineering.ktor.ktor-rate-limit
name: ktor-rate-limit
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, rate-limit, token-bucket, throttling, request-key, kotlin-server]
level: advanced
status: docs-checked
description: "Limit client request rates in Ktor with the RateLimit plugin: token bucket, global or named limiters, request keys, weights, per-user limits and response headers."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-rate-limit.md
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/rate-limit/src/main/kotlin/com/example/Application.kt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rate limit requests in Ktor

The `RateLimit` plugin (artifact `io.ktor:ktor-server-rate-limit`, package `io.ktor.server.plugins.ratelimit`) uses a token bucket. Each request takes one token. If tokens remain, the response carries `X-RateLimit-Limit` (capacity), `X-RateLimit-Remaining` and `X-RateLimit-Reset` (UTC seconds when the bucket refills). Otherwise the server answers `429 Too Many Requests` with `Retry-After` (seconds to wait).

## Register

Global:

```kotlin
install(RateLimit) {
    global {
        rateLimiter(limit = 5, refillPeriod = 60.seconds)
    }
}
```

Registered with `register`, applied later to routes. Without a name it is the default limiter; with `RateLimitName` it is named:

```kotlin
install(RateLimit) {
    register {
        rateLimiter(limit = 5, refillPeriod = 60.seconds)
    }
    register(RateLimitName("protected")) {
        rateLimiter(limit = 30, refillPeriod = 60.seconds)
    }
}
```

`limit` is the bucket capacity; `refillPeriod` is how often it refills (30 per minute above).

## Options inside a limiter

- `requestKey { call -> ... }`: requests with different keys get independent buckets; by default all share one. Keys need proper `equals` and `hashCode`.
- Query parameter (the example keys on `login`):

```kotlin
requestKey { applicationCall ->
    applicationCall.request.queryParameters["login"]!!
}
```

- Client IP: key on `call.request.origin.remoteHost`. Behind a proxy or load balancer, configure the Forwarded headers plugin so this is the real client.

```kotlin
register(RateLimitName("per-ip")) {
    rateLimiter(limit = 5, refillPeriod = 60.seconds)
    requestKey { call ->
        call.request.origin.remoteHost
    }
}
```

- API key: return the header value; or use the authenticated principal from API key auth.

```kotlin
register(RateLimitName("per-api-key")) {
    rateLimiter(limit = 5, refillPeriod = 60.seconds)
    requestKey { call ->
        call.request.headers["X-Api-Key"] ?: "anonymous"
    }
}
```

- Bearer token: `call.request.authorization()?.removePrefix("Bearer ") ?: "anonymous"`. For authenticated requests prefer the principal.
- Per user: nest `rateLimit(RateLimitName("per-user")) { ... }` inside `authenticate("auth") { ... }` and use `call.principal<UserIdPrincipal>()?.name ?: "anonymous"` as key.
- `requestWeight`: tokens consumed per request; it receives the call and the request key. Here the `jetbrains` key consumes one token and all others two:

```kotlin
requestWeight { applicationCall, key ->
    when (key) {
        "jetbrains" -> 1
        else -> 2
    }
}
```

- `modifyResponse { applicationCall, state -> ... }`: add custom headers, for example `applicationCall.response.header("X-RateLimit-Custom-Header", "Some value")`.

## Apply to routes

`rateLimit { ... }` with no name applies the default limiter; `rateLimit(RateLimitName("protected")) { ... }` applies a named one. A registered limiter does nothing until applied this way.

```kotlin
routing {
    rateLimit {
        get("/") {
            val requestsLeft = call.response.headers["X-RateLimit-Remaining"]
            call.respondText("Welcome to the home page! $requestsLeft requests left.")
        }
    }
    rateLimit(RateLimitName("protected")) {
        get("/protected-api") {
            val requestsLeft = call.response.headers["X-RateLimit-Remaining"]
            val login = call.request.queryParameters["login"]
            call.respondText("Welcome to protected API, $login! $requestsLeft requests left.")
        }
    }
}
```

To customize `429` responses, use the StatusPages plugin:

```kotlin
install(StatusPages) {
    status(HttpStatusCode.TooManyRequests) { call, status ->
        val retryAfter = call.response.headers["Retry-After"]
        call.respondText(text = "429: Too many requests. Wait for $retryAfter seconds.", status = status)
    }
}
```

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-rate-limit.md, codeSnippets/snippets/rate-limit/src/main/kotlin/com/example/Application.kt.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.

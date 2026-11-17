---
id: computing-software.software-engineering.ktor.ktor-call-logging
name: ktor-call-logging
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, call-logging, slf4j, mdc, logging, kotlin-server]
level: intro
status: docs-checked
description: "Log incoming Ktor requests with the CallLogging plugin: set the level, filter requests, customize the message format and add values to MDC."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-call-logging.md
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/logging/src/main/kotlin/com/example/Application.kt
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-call-id.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Log requests with Ktor CallLogging

The `CallLogging` plugin (artifact `io.ktor:ktor-server-call-logging`, package `io.ktor.server.plugins.calllogging`) logs incoming client requests through SLF4J. The docs note it is not supported on native servers. All settings are on `CallLoggingConfig`.

## Level

Default is `Level.INFO`. Change it with the `level` property inside `install(CallLogging) { ... }`, with the SLF4J `Level` type (`org.slf4j.event.*`):

```kotlin
install(CallLogging) {
    level = Level.INFO
}
```

## Filter

Assign `filter` a predicate over the call. The docs example logs only requests whose path starts with `/api/v1`:

```kotlin
install(CallLogging) {
    filter { call ->
        call.request.path().startsWith("/api/v1")
    }
}
```

## Message format

Use `format { call -> ... }` to return the log text. The docs example builds a message from the response status, the request HTTP method and the `User-Agent` header value:

```kotlin
install(CallLogging) {
    format { call ->
        val status = call.response.status()
        val httpMethod = call.request.httpMethod.value
        val userAgent = call.request.headers["User-Agent"]
        "Status: $status, HTTP method: $httpMethod, User agent: $userAgent"
    }
}
```

## MDC

`mdc` stores a value in the Mapped Diagnostic Context under a name. This adds the `name` query parameter:

```kotlin
install(CallLogging) {
    mdc("name-parameter") { call ->
        call.request.queryParameters["name"]
    }
}
```

Read it during the call's lifetime with `MDC.get("name-parameter")` (`org.slf4j.MDC`).

## Related

Combine with the `CallId` plugin and `callIdMdc` to show a call ID on each log line. General logging setup (for example logger configuration) is covered by Ktor's separate logging topic.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-call-logging.md, codeSnippets/snippets/logging/src/main/kotlin/com/example/Application.kt, topics/server-call-id.md.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages. Added server-call-id.md to sources (it confirms the callIdMdc claim).

Method: documentation only; no commands were run.

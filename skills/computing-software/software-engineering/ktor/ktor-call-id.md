---
id: computing-software.software-engineering.ktor.ktor-call-id
name: ktor-call-id
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, call-id, request-id, tracing, mdc, kotlin-server]
level: advanced
status: docs-checked
description: "Trace Ktor requests end to end with the CallId plugin: retrieve, generate, verify and reply with call IDs, and put the ID into MDC for CallLogging."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-call-id.md
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/call-id/src/main/kotlin/com/example/Application.kt
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/call-id/src/main/resources/logback.xml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Trace requests with call IDs in Ktor

The `CallId` plugin (artifact `io.ktor:ktor-server-call-id`, package `io.ktor.server.plugins.callid`) flow is: obtain an ID (retrieve from a header such as `X-Request-Id`, or generate), verify it, then send it back to the client.

## Retrieve

```kotlin
install(CallId) {
    retrieveFromHeader(HttpHeaders.XRequestId)
}
```

Or `retrieve { call -> call.request.header(HttpHeaders.XRequestId) }`. The `header` function retrieves and replies in the same header.

## Generate

When a request has no ID:

```kotlin
install(CallId) { generate(10, "abcde12345") }  // length, dictionary
```

or a block, e.g. `generate { "generated-call-id-${counter.getAndIncrement()}" }` with an atomic counter.

## Verify

Every retrieved or generated ID is checked against the default dictionary `"abcdefghijklmnopqrstuvwxyz0123456789+/=-"`. Gotcha: IDs with capital letters fail verification. Relax the rule with the `verify` function:

```kotlin
install(CallId) {
    verify { callId: String ->
        callId.isNotEmpty()
    }
}
```

## Send to client

- `replyToHeader(HttpHeaders.XRequestId)`
- `reply { call, callId -> call.response.header(HttpHeaders.XRequestId, callId) }`
- `header(HttpHeaders.XRequestId)` retrieves and replies in one call (the example installs `CallId { header(HttpHeaders.XRequestId); verify { ... } }`).

## MDC logging

Inside the `CallLogging` block call `callIdMdc` with the key, then reference that key in the logger pattern in `logback.xml` so each log line shows the ID:

```kotlin
install(CallLogging) {
    callIdMdc("call-id")
}
```

```xml
<appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
    <encoder>
        <pattern>%d{YYYY-MM-dd HH:mm:ss.SSS} [%thread] %X{call-id} %-5level %logger{36} - %msg%n</pattern>
    </encoder>
</appender>
```

On the client side Ktor has a separate `CallId` plugin for tracing client requests.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-call-id.md, codeSnippets/snippets/call-id/src/main/kotlin/com/example/Application.kt, codeSnippets/snippets/call-id/src/main/resources/logback.xml.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.

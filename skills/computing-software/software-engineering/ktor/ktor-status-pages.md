---
id: computing-software.software-engineering.ktor.ktor-status-pages
name: ktor-status-pages
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, status-pages, error-handling, exceptions, http-status, kotlin]
level: intro
status: docs-checked
description: "Configure the Ktor StatusPages plugin to map exceptions, status codes and classpath HTML files (statusFile) to custom error responses."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-status-pages.md
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/status-pages/src/main/kotlin/com/example/Application.kt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ktor StatusPages plugin

StatusPages lets a Ktor app respond appropriately to a failure state, based on a thrown exception or a status code. Add the dependency `io.ktor:ktor-server-status-pages` (package `io.ktor.server.plugins.statuspages`) and `install(StatusPages) { ... }`.

It has three options.

## exception
Handles calls that end in a `Throwable`; check the exception class inside the handler to respond with the content you need:

```kotlin
install(StatusPages) {
    exception<Throwable> { call, cause ->
        if(cause is AuthorizationException) {
            call.respondText(text = "403: $cause" , status = HttpStatusCode.Forbidden)
        } else {
            call.respondText(text = "500: $cause" , status = HttpStatusCode.InternalServerError)
        }
    }
}

class AuthorizationException(override val message: String?) : Throwable()
```

## status
Responds with specific content for a status code, for example a missing resource (`404`):

```kotlin
status(HttpStatusCode.NotFound) { call, status ->
    call.respondText(text = "404: Page Not Found", status = status)
}
```

## statusFile
Serves HTML pages from the classpath by status code. If `resources` holds `error401.html` and `error402.html`, configure `statusFile` for the `401` and `402` codes. Ktor replaces every `#` character in the file name pattern with the status code:

```kotlin
statusFile(HttpStatusCode.Unauthorized, HttpStatusCode.PaymentRequired, filePattern = "error#.html")
```

Full sample: the `status-pages` project in the ktor-documentation code snippets.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-status-pages.md, codeSnippets/snippets/status-pages/src/main/kotlin/com/example/Application.kt.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.

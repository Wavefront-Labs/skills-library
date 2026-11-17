---
id: computing-software.software-engineering.ktor.ktor-conditional-headers
name: ktor-conditional-headers
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, conditional-requests, etag, last-modified, http-headers, kotlin-server]
level: intro
status: docs-checked
description: "Skip resending unchanged content in Ktor with the ConditionalHeaders plugin, using Etag and Last-Modified versions via EntityTagVersion and LastModifiedVersion."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-conditional-headers.md
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/conditional-headers/src/main/kotlin/com/example/Application.kt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Avoid resending unchanged content with ConditionalHeaders

The `ConditionalHeaders` plugin (artifact `io.ktor:ktor-server-conditional-headers`, package `io.ktor.server.plugins.conditionalheaders`) avoids sending a response body when the resource has not changed since the client's last request. It works through two header pairs.

## Last-Modified

The `Last-Modified` response header carries the resource modification time. When the client sends `If-Modified-Since`, Ktor sends a full response only if the resource was modified after that date. For static files, Ktor adds `Last-Modified` automatically once the plugin is installed.

## Etag

The `Etag` response header identifies a specific version of a resource. When the client sends `If-None-Match` and the value matches the `Etag`, Ktor does not send the full response. You supply the `Etag` value in the plugin configuration.

## Configure versions

Call the `version` function inside the `install(ConditionalHeaders) { ... }` block. It gives you the `ApplicationCall` and the `OutgoingContent` and expects a list of resource versions. Build them with:

- `EntityTagVersion` for an `Etag`.
- `LastModifiedVersion` for `Last-Modified`.

The docs example adds both an `Etag` and a `Last-Modified` header for CSS content:

```kotlin
install(ConditionalHeaders) {
    val file = File("src/main/kotlin/com/example/Application.kt")
    version { call, outgoingContent ->
        when (outgoingContent.contentType?.withoutParameters()) {
            ContentType.Text.CSS -> listOf(
                EntityTagVersion(file.lastModified().hashCode().toString()),
                LastModifiedVersion(Date(file.lastModified()))
            )
            else -> emptyList()
        }
    }
}
```

The plugin can also be installed on a specific route rather than the whole application.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-conditional-headers.md, codeSnippets/snippets/conditional-headers/src/main/kotlin/com/example/Application.kt.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.

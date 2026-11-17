---
id: computing-software.software-engineering.ktor.ktor-partial-content
name: ktor-partial-content
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, partial-content, range-requests, streaming, resumable-download, kotlin-server]
level: intro
status: docs-checked
description: "Support HTTP range requests in Ktor with the PartialContent plugin for streaming and resumable downloads, and know its method, Content-Length and Compression limits."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-partial-content.md
  - https://github.com/ktorio/ktor-documentation/blob/main/codeSnippets/snippets/download-file/src/main/kotlin/com/example/DownloadFile.kt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Serve HTTP range requests with Ktor PartialContent

The `PartialContent` plugin (artifact `io.ktor:ktor-server-partial-content`, package `io.ktor.server.plugins.partialcontent`) lets the server answer range requests with only part of a message. Use it for streaming content or resuming partial downloads.

## Install

Add the dependency and call `install(PartialContent)`. It can be installed on the whole application or on a specific route, and native servers are supported.

## Limitations to check before relying on it

- It works only for `HEAD` and `GET`. A `Range` header on any other method gets `405 Method Not Allowed`.
- It works only for responses that define `Content-Length`.
- It disables Compression while serving ranges, so do not expect `Compression` to apply to those responses.

## Serving a file

The plugin page itself has no code; it points to the file section of the Ktor server responses docs. The `download-file` code snippet installs `PartialContent` together with `AutoHeadResponse`:

```kotlin
fun Application.main() {
    install(PartialContent)
    install(AutoHeadResponse)
    routing {
        get("/download") {
            val file = File("files/ktor_logo.png")
            call.response.header(
                HttpHeaders.ContentDisposition,
                ContentDisposition.Attachment.withParameter(ContentDisposition.Parameters.FileName, "ktor_logo.png")
                    .toString()
            )
            call.respondFile(file)
        }
        get("/downloadFromPath") {
            val filePath = Path.of("files/file.txt")
            call.response.header(
                HttpHeaders.ContentDisposition,
                ContentDisposition.Attachment.withParameter(ContentDisposition.Parameters.FileName, "file.txt")
                    .toString()
            )
            call.respond(LocalPathContent(filePath))
        }
    }
}
```

Use `call.respondFile` for a `File` and `call.respond(LocalPathContent(path))` for a `Path`. The client-side counterpart is the `client-download-file-range` example.

## Checklist

1. Add `ktor-server-partial-content`.
2. `install(PartialContent)` (imports `io.ktor.server.plugins.partialcontent.*`).
3. Respond with content that has `Content-Length` defined (the snippet responds with a file).

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-partial-content.md, codeSnippets/snippets/download-file/src/main/kotlin/com/example/DownloadFile.kt.

Removed or changed: removed an unconfirmed Content-Length/HEAD rationale for installing AutoHeadResponse and reworded the Serving a file intro to match the page.

Method: documentation only; no commands were run.

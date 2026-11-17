---
id: computing-software.software-engineering.ktor.ktor-client-responses
name: ktor-client-responses
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, kotlin, http-client, responses, streaming, downloads, multipart]
level: practitioner
status: docs-checked
description: "Read Ktor client HttpResponse status, headers and body (string, bytes, JSON, multipart) and stream large downloads to disk with HttpStatement and ByteReadChannel."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/client-responses.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Receiving responses in the Ktor client

Every request function (`request`, `get`, `post`, ...) returns an `HttpResponse`.

## Parameters

- Status: `HttpResponse.status`.
- Headers: `HttpResponse.headers` is a `Headers` map. Helpers: `contentType()`, `charset()`, `etag()`, `setCookie()`.
- Multi-value headers: `headers.getSplitValues("X-Multi-Header")` splits comma/semicolon separated values (`["1", "2", "3"]`), while the plain `headers["X-Multi-Header"]` returns them unsplit (`["1, 2", "3"]`).

## Body

- `response.body<String>()` or `response.body<ByteArray>()` for raw data. `onDownload()` shows progress.
- JSON: with `ContentNegotiation` installed, `response.body<Customer>()` deserializes into a class. The plugin exists for both client and server; use the client one.
- Multipart: read the body as `MultiPartData`. `PartData.FormItem` is a text field (read its `value`); `PartData.FileItem` is a file you can handle as a byte stream. Call `.dispose()` on each part when done to free resources.

## Memory caveat

For non-streaming requests the body is loaded and cached in memory, so repeated access works, but large responses can use a lot of memory. Stream them instead.

## Streaming

Use `client.prepareGet(url).execute { httpResponse -> ... }` (an `HttpStatement` with a scoped `execute` block) and read the `ByteReadChannel` from `httpResponse.body()` in chunks. `ByteReadChannel.readRemaining()` fetches available bytes and `Source.transferTo()` writes directly to a file.

On JVM, running `HttpStatement.execute {}` and `HttpStatement.body {}` on the engine dispatcher is opt-in: set the JVM system property `io.ktor.client.statement.useEngineDispatcher` to `true` (for example `-Dio.ktor.client.statement.useEngineDispatcher=true`).

Simple whole-file downloads:

```kotlin
client.prepareGet("https://httpbin.org/bytes/$fileSize").execute { httpResponse ->
    val channel: ByteReadChannel = httpResponse.body()
    channel.copyAndClose(file.writeChannel())
}
```

- `copyAndClose()` copies all remaining bytes to a `ByteWriteChannel` and closes both channels.
- `channel.readTo(sink)` writes straight to a `RawSink` without intermediate buffers; unlike `copyAndClose()`, the sink stays open and is closed automatically only if an error occurs.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/client-responses.md.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.

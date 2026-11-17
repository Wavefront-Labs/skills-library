---
id: computing-software.software-engineering.ktor.ktor-server-responses
name: ktor-server-responses
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, responses, respond, streaming, headers, cookies, redirect]
level: practitioner
status: docs-checked
description: "Send Ktor server responses: text, streaming, HTML, templates, objects, files, classpath resources, raw bytes, plus status, content type, headers, cookies and redirects."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-responses.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sending responses in Ktor

## Payload functions
- Text: `call.respondText("Hello, world!")`.
- Streaming text (JVM): `call.respondTextWriter { }` gives a `Writer`, closed automatically; call `flush()` to push buffered output.
- Streaming binary (JVM): `call.respondOutputStream { }` gives an `OutputStream`, closed automatically. Multiplatform: `call.respondBytesWriter { }` gives a `ByteWriteChannel`, also closed automatically.
- HTML DSL: `call.respondHtml { }` for a full document; `call.respondHtmlPartial()` for a fragment without `<html>`, `<head>`, `<body>`.
- Templates: `call.respond(...)` with template content, or `call.respondTemplate("index.ftl", mapOf("user" to sampleUser))` (FreeMarker).
- Objects: install ContentNegotiation with a converter, then `call.respond(dataObject)`.
- Files: `call.respondFile()` for a `File`; for a `Path`, `call.respond()` with `LocalPathContent`. To make a download, add a `Content-Disposition` header; the sample also installs `PartialContent` (Range requests) and `AutoHeadResponse` (HEAD answers so clients can read `Content-Length`).
- Classpath resource: `call.respondResource("public/index.html")` reads the resource stream and derives `Content-Type` from the extension. A second parameter takes the package, e.g. `call.respondResource(path, "assets")`; a missing resource throws `IllegalArgumentException` (catch it and respond `HttpStatusCode.NotFound`).
- Raw bytes: `call.respondBytes()`.

## Response parameters
- Status: `call.response.status(HttpStatusCode.OK)` or custom `HttpStatusCode(418, "I'm a tea pot")`. All payload functions also have overloads taking a status code.
- Content type: chosen automatically with ContentNegotiation; or pass it, e.g. `call.respondText("Hello, world!", ContentType.Text.Plain, HttpStatusCode.OK)`.
- Headers: `call.response.headers.append(HttpHeaders.ETag, "7c876b7e")`, `headers.appendAll("X-Custom-Header" to listOf("value1", "value2"))`, `call.response.header("Custom-Header", "Some value")`, or helpers like `call.response.etag("7c876b7e")`. Install DefaultHeaders for automatic `Server` and `Date` headers.
- Cookies: `call.response.cookies.append("yummy_cookie", "choco")`.

## Redirects
`call.respondRedirect("/moved", permanent = true)`.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-responses.md.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.

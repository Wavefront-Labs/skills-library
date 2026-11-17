---
id: computing-software.software-engineering.ktor.ktor-client-requests
name: ktor-client-requests
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, kotlin, http-client, requests, forms, multipart, urls]
level: practitioner
status: docs-checked
description: "Build Ktor client requests: HTTP method, URL components, headers, cookies, text/JSON/form/multipart/binary bodies, Unix sockets, parallel and cancelled requests."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/client-requests.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Making requests with the Ktor client

Use the suspending `client.request(url) { ... }` function; the lambda is an `HttpRequestBuilder`. It returns an `HttpResponse`. Shortcuts exist: `.get()`, `.post()`, `.put()` and so on. All are suspending, so call them from a coroutine.

## Method and URL

- Method: `method = HttpMethod.Get` inside `.request()` (imports `io.ktor.client.request.*`, `io.ktor.http.*`).
- URL as one string, or via the `url` property (a `URLBuilder`) for components.
- Path: `URLBuilder.path`, or `appendPathSegments()` for individual segments. Segments are percent-encoded; use `appendEncodedPathSegments()` to skip encoding.
- Query: `URLBuilder.parameters` (encoded by default; `encodedParameters()` to skip). `trailingQuery` keeps the `?` when there are no parameters.
- Fragment: the `fragment` property (encoded; `encodedFragment()` to skip).
- A base URL for every request belongs in the `DefaultRequest` plugin.

## Unix domain socket

Supported only by the CIO engine:

```kotlin
val client = HttpClient(CIO)
val response: HttpResponse = client.get("/") {
    unixSocket("/tmp/test-unix-socket-ktor.sock")
}
```

## Headers and cookies

- `headers { ... }` adds several at once; `appendAll()` accepts a `Map` or `vararg Pair`.
- `header(name, value)` adds one.
- `basicAuth` / `bearerAuth` add an `Authorization` header with that scheme.
- `cookie()` sends a cookie on one request. If the `HttpCookies` plugin is installed, cookies added with `cookie()` are ignored.

## Bodies via setBody()

- Text: `setBody("Body content")`.
- Objects: with `ContentNegotiation` installed, `setBody(instance)` plus `contentType(ContentType.Application.Json)`.
- Form (`application/x-www-form-urlencoded`): `submitForm(url, formParameters = parameters { ... })`. Set `encodeInQuery = true` to put the parameters in the URL.
- File upload: `submitFormWithBinaryData()` (boundary generated; file read into memory with `.readBytes()`, so small files only), or `post` with `setBody(MultiPartFormDataContent(...))`. Both build data with `formData {}`. For large files, give `MultiPartFormDataContent` an `InputProvider` (buffered stream) and watch progress with `onUpload`. The constructor also takes a custom boundary.
- Binary (`application/octet-stream`): pass a `ByteReadChannel`, for example `File.readChannel()`.

## Parallel and cancel

Requests run sequentially by default (each call suspends). Use `launch()` or `async()` to run them concurrently. To cancel, cancel the coroutine: `launch { client.get(...) }` returns a `Job`; call `job.cancel()`.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/client-requests.md.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.

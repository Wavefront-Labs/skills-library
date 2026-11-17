---
id: computing-software.software-engineering.ktor.ktor-server-requests
name: ktor-server-requests
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, requests, query-parameters, multipart, file-upload, receive, kotlin]
level: practitioner
status: docs-checked
description: "Read Ktor request data in route handlers: headers, cookies, path and query parameters, require* helpers, raw/object/form bodies and multipart file uploads."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-requests.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Handling requests in Ktor route handlers

Each handler exposes `call` (an `ApplicationCall`, one HTTP exchange). Request data is under `call.request` (`ApplicationRequest`).

## Request information
- `call.request.uri` gives the request URI.
- `call.request.headers` gives all headers; extensions such as `.acceptEncoding()`, `.contentType()`, `.cacheControl()` cover common ones.
- `call.request.cookies` gives cookies.
- `call.request.local` gives host, port and scheme.
- Behind a proxy or load balancer, install the forward-headers plugin and read `call.request.origin`.

## Parameters
- Path parameters: `call.parameters["login"]` (returns `admin` for `/user/admin` on `/user/{login}`).
- Query parameters: `call.request.queryParameters` (e.g. `price` in `/products?price=asc`); the whole string via `call.request.queryString()`.

## Required values
`requireQueryParameter()`, `requireHeader()`, `requireCookie()` and `requirePathParameter()` return a non-null value or throw `MissingRequestParameterException`:

```kotlin
post("/checkout/{cartId}") {
    val userId = call.requireCookie("userId")
    val cartId = call.requirePathParameter("cartId")
    val amount = call.requireQueryParameter("amount").toLong()
}
```

## Body
- Raw: `call.receive<String>()` or `receiveText()`; `receive<ByteArray>()`; `receive<ByteReadChannel>()` or `receiveChannel()` (also usable to stream an upload to a file).
- Object: `call.receive<Customer>()` with the ContentNegotiation plugin; use `receive<Customer?>()` if content can deserialize to `null`.
- Form parameters: `call.receiveParameters()` handles both `x-www-form-urlencoded` and `multipart/form-data`.

## Multipart
`call.receiveMultipart()` is processed sequentially, so you cannot jump to a specific part. Handle each part by type:
- `PartData.FormItem`: field value in `value`.
- `PartData.FileItem`: stream with `.provider()` (a `ByteReadChannel`) and write it using `.copyAndClose()`.
- Call `.dispose()` on each part when finished.

Binary and file parts are limited to 50MiB by default; exceeding it throws `IOException`. Override per call: `receiveMultipart(formFieldLimit = ...)`. `Content-Length` (via `call.request.header(HttpHeaders.ContentLength)`) is the whole multipart body size, not one file.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-requests.md.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.

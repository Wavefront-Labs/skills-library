---
id: computing-software.web-development.vapor.vapor-request-body-cookies-headers
name: vapor-request-body-cookies-headers
category: computing-software
field: web-development
product: vapor
tags: [vapor,vapor-request,request,cookies,headers,remote-address,swift]
level: practitioner
status: docs-checked
description: "Read the request body buffer, cookies, headers and client IP from Vapor's Request object in a route handler."
sources:
  - https://docs.vapor.codes/advanced/request/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: reach body, cookies, headers and client address through `Request` in a Vapor route handler.

`Request` is passed to every route handler and is the main entry to Vapor features (body, query, logger, client, authenticators). Using it keeps work on the correct event loop and lets services be mocked in tests. Your own services can be added to `Request` with extensions.

- **Application**: `req.application` holds the `Application`. Most of it should be set only in `configure.swift` before the app starts. `Application.eventLoopGroup` with `any()` gives an `EventLoop` for processes needing a new one. It also holds the `Environment`.
- **Body**: `req.body.data` gives the raw body as a `ByteBuffer`, usable to stream to another HTTP client. To stream to a file, use the request's `fileio` property instead.
- **Cookies**: `req.cookies` reads cookies directly (sessions are the usual cookie use).

```swift
app.get("my-cookie") { req -> String in
    guard let cookie = req.cookies["my-cookie"] else {
        throw Abort(.badRequest)
    }
    if let expiration = cookie.expires, expiration < Date() {
        throw Abort(.badRequest)
    }
    return cookie.string
}
```

- **Headers**: `req.headers` is an `HTTPHeaders`; Vapor adds extensions for common headers.

```swift
app.get("json") { req -> String in
    guard let contentType = req.headers.contentType, contentType == .json else {
        throw Abort(.badRequest)
    }
    return "JSON"
}
```

- **IP address**: `req.remoteAddress` is a `SocketAddress`; `req.remoteAddress.ipAddress` is its string form, useful for logging or rate limiting.

Gotcha: behind a reverse proxy, `remoteAddress` may not be the real client IP.

## Checked
Read the whole Request page (vapor/docs, docs/4.0/advanced/request.md, source of the cited page) on 2026-11-08. Confirmed the Application, Body, Cookies, Headers and IP Address sections, their examples and the reverse-proxy caveat. No claims removed.
Method: docs-only read of cited pages, 2026-11-08

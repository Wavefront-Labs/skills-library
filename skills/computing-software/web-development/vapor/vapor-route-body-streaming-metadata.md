---
id: computing-software.web-development.vapor.vapor-route-body-streaming-metadata
name: vapor-route-body-streaming-metadata
category: computing-software
field: web-development
product: vapor
tags: [vapor, routing, body-streaming, maxsize, case-insensitive, routes-command, route-metadata, stream]
level: advanced
status: docs-checked
description: "Control Vapor request body collection and size limits, stream uploads, enable case-insensitive routes, list routes and attach route metadata."
sources:
  - https://docs.vapor.codes/basics/routing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: tune how routes receive bodies and inspect/annotate routes.

## Body collection
Registered with `on`, a route can choose its body strategy. By default the body is collected into memory before the handler runs (this keeps content decoding synchronous), with a 16KB limit on streaming body collection. Exceeding the limit throws `413 Payload Too Large`.
```swift
// raise the app-wide limit
app.routes.defaultMaxBodySize = "500kb"

// per-route collect with its own limit (omit maxSize to use the default)
app.on(.POST, "listings", body: .collect(maxSize: "1mb")) { req in ... }

// do not buffer (large uploads)
app.on(.POST, "upload", body: .stream) { req in ... }
```
With `.stream`, `req.body.data` is `nil`; use `req.body.drain` to handle each chunk as it arrives. Collecting large bodies (file uploads) in a buffer can strain memory, which is why `.stream` exists.

## Case-insensitive routing
Routing is case-sensitive and case-preserving by default. Constant path components can be matched case-insensitively; set before application startup:
```swift
app.routes.caseInsensitive = true
```
The request is not modified; handlers still see the original path components.

## Viewing routes
```swift
print(app.routes.all) // [Route]
```
Or run the `routes` command, which prints an ASCII table of method and path:
```sh
swift run App routes
```

## Metadata
Route registration methods return the created `Route`, so you can set its `userInfo` metadata; a default helper sets a description:
```swift
app.get("hello", ":name") { req in ... }.description("says hello")
```

## Checked
Read the Body Streaming, Case Insensitive Routing, Viewing Routes and Metadata sections of the Routing page (vapor/docs, docs/4.0/basics/routing.md, source of the cited page) in full on 2026-11-08; the other sections (parameters, groups) were not read and the skill does not use them. Confirmed the 16KB default, 413 error, `defaultMaxBodySize`, `.collect(maxSize:)`, `.stream`, `req.body.drain`, `caseInsensitive` and its unmodified request, `app.routes.all`, the `routes` command and `userInfo`/description metadata. No claims removed.
Method: docs-only read of cited pages, 2026-11-08

---
id: computing-software.web-development.vapor.vapor-routes-and-parameters
name: vapor-routes-and-parameters
category: computing-software
field: web-development
product: vapor
tags: [vapor, routing, route-parameters, path-components, catchall, req-parameters, http-methods, get-post]
level: intro
status: docs-checked
description: "Register Vapor routes with HTTP-method helpers, constant, :parameter, * and ** path components, and read req.parameters including typed and catchall values."
sources:
  - https://docs.vapor.codes/basics/routing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: map method + path to a handler.

```swift
app.get("hello", "vapor") { req in "Hello, vapor!" }
app.on(.GET, "hello", "vapor") { ... }   // same, via on
```
Helpers: get, post, patch, put, delete; use `on(.OPTIONS, ...)` for others. Methods map to CRUD: GET read, POST create, PUT replace, PATCH update, DELETE delete. Path arguments are separate strings. Handlers may return anything `ResponseEncodable`: `Content`, an async closure, or an `EventLoopFuture` of one. Add `-> T` before `in` when the compiler can't infer the return type.

## Path components (string-literal expressible)
- Constant `foo`: exact match.
- Parameter `:foo`: any string, stored under the name.
- Anything `*`: any string, value discarded.
- Catchall `**`: one or more components.
```swift
app.get("foo", ":bar", "baz") { ... }   // /foo/bar/baz, /foo/qux/baz
app.get("foo", "*", "baz") { ... }
app.get("foo", "**") { ... }            // /foo/bar, /foo/bar/baz
```

## Reading parameters
```swift
app.get("hello", ":name") { req -> String in
    let name = req.parameters.get("name")!
    return "Hello, \(name)!"
}
app.get("number", ":x") { req -> String in
    guard let int = req.parameters.get("x", as: Int.self) else { throw Abort(.badRequest) }
    return "\(int) is a great number"
}
app.get("hello", "**") { req -> String in
    let name = req.parameters.getCatchall().joined(separator: " ")
    return "Hello, \(name)!"
}
```
`get(_:as:)` casts to any `LosslessStringConvertible`. Catchall values are `[String]`.

Gotchas: the force-unwrap is safe only because the route has `:name`; in middleware or code shared by several routes handle `nil`. Query-string values (`/hello/?name=foo`) are not route parameters; decode them with the Content APIs (`req.query`).

## Checked

2026-11-08: read in full the Routing page at docs.vapor.codes/basics/routing/ (method helpers, path components, req.parameters, typed and catchall parameters, query string tip). Every claim was found on the cited pages; nothing needed removing.

Method: docs-only read of cited pages, 2026-11-08

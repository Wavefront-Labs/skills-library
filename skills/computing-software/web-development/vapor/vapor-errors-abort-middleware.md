---
id: computing-software.web-development.vapor.vapor-errors-abort-middleware
name: vapor-errors-abort-middleware
category: computing-software
field: web-development
product: vapor
tags: [vapor,abort,debuggableerror,errors,errormiddleware,aborterror,swift]
level: practitioner
status: docs-checked
description: "Throw Abort and custom AbortError or DebuggableError types in Vapor, and replace ErrorMiddleware while keeping CORSMiddleware first."
sources:
  - https://docs.vapor.codes/basics/errors/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: control the HTTP status, reason and logging of errors from route handlers.

Any Swift `Error` thrown (or returned as a failed future) gives a `500` and is logged. In debug builds `ErrorMiddleware` includes the error description; it is stripped in release builds. `ErrorMiddleware` is added by default and does the conversion; without it the connection closes with no response.

## Abort
```swift
throw Abort(.notFound)                                    // default "Not Found" reason
throw Abort(.unauthorized, reason: "Invalid Credentials") // custom reason
```
In a `flatMap` closure return `req.eventLoop.makeFailedFuture(Abort(.notFound))`. On futures, `.unwrap(or: Abort(.notFound))` fails a nil result. With async/await: `guard let user = try await User.find(id, on: db) else { throw Abort(.notFound) }`.

## AbortError
Conform your error to `AbortError` and supply `reason: String` and `status: HTTPStatus` (switch on cases, e.g. `.unauthorized`, `.badRequest`).

## DebuggableError
Customises logging (`Logger.report(error:)` otherwise relies on `CustomStringConvertible`/`LocalizedError`). Use a struct so it can store source info: provide `identifier`, `reason`, `source: ErrorSource?` (init with `file: #file, function: #function, line: #line, column: #column`). Other properties include `possibleCauses` and `suggestedFixes`.

## Replace ErrorMiddleware
```swift
app.middleware = .init()   // clears defaults
app.middleware.use(RouteLoggingMiddleware(logLevel: .info))
app.middleware.use(MyErrorMiddleware())  // first
```
Very few middleware should precede error handling; `CORSMiddleware` is the notable exception.

## Checked

2026-11-07. Confirmed against the Vapor docs page(s) basics/errors, read in full with their code examples; every remaining claim matches the page text.
Method: documentation only; no commands were run.

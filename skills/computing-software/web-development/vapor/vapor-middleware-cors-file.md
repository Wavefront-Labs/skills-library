---
id: computing-software.web-development.vapor.vapor-middleware-cors-file
name: vapor-middleware-cors-file
category: computing-software
field: web-development
product: vapor
tags: [vapor,middleware,cors,asyncmiddleware,filemiddleware,swift,request-pipeline]
level: practitioner
status: docs-checked
description: "Register and order Vapor middleware, write Middleware or AsyncMiddleware, serve Public files with FileMiddleware and configure CORSMiddleware before errors."
sources:
  - https://docs.vapor.codes/advanced/middleware/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: add request/response logic around route handlers.

## Register
Globally in `configure(_:)`: `app.middleware.use(MyMiddleware())`. Per route via groups: `let group = app.grouped(MyMiddleware())`.

## Order
Requests pass through middleware in the order added; responses return in reverse. Route-specific middleware runs after application middleware. With A, B globally and C on a group: `Request -> A -> B -> C -> Handler -> C -> B -> A -> Response`. Prepend (before Vapor's defaults) with `app.middleware.use(someMiddleware, at: .beginning)`.

## Write one
Conform to `Middleware` or `AsyncMiddleware`:
```swift
struct EnsureAdminUserMiddleware: AsyncMiddleware {
    func respond(to request: Request, chainingTo next: AsyncResponder) async throws -> Response {
        guard let user = request.auth.get(User.self), user.role == .admin else {
            throw Abort(.unauthorized)
        }
        return try await next.respond(to: request)
    }
}
```
Modify the response by awaiting the next responder first:
```swift
let response = try await next.respond(to: request)
response.headers.add(name: "My-App-Version", value: "v2.5.9")
return response
```
Future style: `respond(to:chainingTo: Responder) -> EventLoopFuture<Response>`, failing with `request.eventLoop.future(error: Abort(.unauthorized))` and using `next.respond(to: request).map { ... }`. Docs suggest a `Middleware` folder in `Sources/App`.

## FileMiddleware
```swift
let file = FileMiddleware(publicDirectory: app.directory.publicDirectory)
app.middleware.use(file)
```
`Public/images/logo.png` is then reachable as `/images/logo.png`. In an Xcode project use `try FileMiddleware(bundle: .main, publicDirectory: "Public")` and Folder References, not Groups.

## CORSMiddleware
```swift
let corsConfiguration = CORSMiddleware.Configuration(
    allowedOrigin: .all,
    allowedMethods: [.GET, .POST, .PUT, .OPTIONS, .DELETE, .PATCH],
    allowedHeaders: [.accept, .authorization, .contentType, .origin, .xRequestedWith, .userAgent, .accessControlAllowOrigin]
)
let cors = CORSMiddleware(configuration: corsConfiguration)
app.middleware.use(cors, at: .beginning)
```
Gotcha: place CORS before `ErrorMiddleware`, otherwise error responses lack CORS headers and browsers cannot read them.

## Checked

2026-11-08: read in full the Middleware page at docs.vapor.codes/advanced/middleware/ (registration, order, Middleware and AsyncMiddleware, FileMiddleware, CORSMiddleware). Every claim was found on the cited pages; nothing needed removing.

Method: docs-only read of cited pages, 2026-11-08

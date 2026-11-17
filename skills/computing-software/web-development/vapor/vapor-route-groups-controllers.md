---
id: computing-software.web-development.vapor.vapor-route-groups-controllers
name: vapor-route-groups-controllers
category: computing-software
field: web-development
product: vapor
tags: [vapor, route-groups, redirect, controllers, routecollection, grouped, middleware, routing]
level: practitioner
status: docs-checked
description: "Group Vapor routes by path prefix or middleware, issue redirects with req.redirect, and organize handlers in RouteCollection controllers."
sources:
  - https://docs.vapor.codes/basics/routing/
  - https://docs.vapor.codes/basics/controllers/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: structure routes with prefixes, middleware groups and controllers.

## Path-prefix groups
All grouping methods return a `RouteBuilder`, so groups nest freely.
```swift
let users = app.grouped("users")
users.get { req in ... }              // GET /users
users.post { req in ... }             // POST /users
users.get(":id") { req in ... }       // GET /users/:id

app.group("users") { users in         // closure form
    users.get { ... }
    users.group(":id") { user in
        user.get { ... }
        user.patch { ... }
        user.put { ... }
    }
}
```
## Middleware groups
```swift
app.group(RateLimitMiddleware(requestsPerMinute: 5)) { rateLimited in
    rateLimited.get("slow-thing") { req in ... }
}
app.post("login") { ... }
let auth = app.grouped(AuthMiddleware())
auth.get("dashboard") { ... }
```
Handy for protecting subsets of routes with different authentication middleware.

## Redirects
```swift
req.redirect(to: "/some/new/path")
req.redirect(to: "/some/new/path", redirectType: .permanent)
```
`.permanent` = 301; `.normal` = 303 See Other (the default; client follows with GET); `.temporary` = 307 (client keeps the HTTP method).

## Controllers
A controller is a `RouteCollection` whose methods take a `Request` and return something `ResponseEncodable` (sync or async). Put them in the Controllers folder.
```swift
struct TodosController: RouteCollection {
    func boot(routes: RoutesBuilder) throws {
        let todos = routes.grouped("todos")
        todos.get(use: index)
        todos.post(use: create)
        todos.group(":id") { todo in
            todo.get(use: show)
            todo.delete(use: delete)
        }
    }
    func index(req: Request) async throws -> [Todo] {
        try await Todo.query(on: req.db).all()
    }
    func create(req: Request) async throws -> Todo {
        let todo = try req.content.decode(Todo.self)
        try await todo.save(on: req.db)
        return todo
    }
    // show/delete look up Todo.find(req.parameters.get("id"), on: req.db)
    // and throw Abort(.notFound) when nil
}
```
Register in routes.swift:
```swift
try app.register(collection: TodosController())
```

## Checked

2026-11-08: read in full the Routing page at docs.vapor.codes/basics/routing/ and the Controllers page at docs.vapor.codes/basics/controllers/ (groups, middleware groups, redirect types, RouteCollection). Every claim was found on the cited pages; nothing needed removing.

Method: docs-only read of cited pages, 2026-11-08

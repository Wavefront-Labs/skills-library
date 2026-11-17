---
id: computing-software.software-engineering.ktor.ktor-server-routing-organization
name: ktor-server-routing-organization
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, routing, code-organization, kotlin, route-extensions, project-structure]
level: practitioner
status: docs-checked
description: "Structure growing Ktor routing code by file, package, path nesting or feature/domain using Route extension functions, and know which pattern fits which project size."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-routing-organization.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Organizing Ktor routing as the app grows

Ktor does not enforce a routing layout; many projects combine the patterns below. Every pattern is built from extension functions on `Route`, registered inside `routing { }`.

## 1. Group by file
Put related routes in one file per domain, for example `CustomerRoutes.kt` and `OrderRoutes.kt`:

```kotlin
fun Route.customerByIdRoute() { get("/customer/{id}") { } }
fun Route.createCustomerRoute() { post("/customer") { } }
```

Register the groups with `routing { customerRoutes(); orderRoutes() }`. Best for small or medium projects where each domain has only a few routes.

## 2. Group by package (folders)
When a file gets hard to navigate, give each domain a package and one file per endpoint, plus an aggregator:

```kotlin
fun Route.customerRoutes(service: CustomerService) {
    listCustomersRoute(service)
    getCustomerRoute(service)
    createCustomerRoute(service)
    updateCustomerRoute(service)
}
```

Each endpoint function takes its dependencies as parameters (for example `service: CustomerService`) and is small, e.g. `post("/customer") { val body = call.receive<CustomerDto>(); call.respond(service.create(body)) }`. Ideal for large APIs with many endpoints.

## 3. Group by path and nest resources
Keep every handler for one path together, and nest child resources:

```kotlin
routing {
    route("/customer") {
        get { /* list */ }
        post { /* create */ }
        route("/{id}") {
            get { }
            put { }
            delete { }
        }
    }
}
```

This keeps related endpoints visually close and mirrors the HTTP API shape.

## 4. Group by feature or domain
A more scalable layout as the application grows: a `routes/` package with a sub-package per feature (`customer/CustomerRoutes.kt`, `Create.kt`, `Details.kt`; `order/OrderRoutes.kt`, `Shipment.kt`). `CustomerRoutes` wraps its endpoints in `route("/customer") { get("/{id}") { ... } post { ... } }`. Feature boundaries stay clear and routing files stay small.

Size guide from the page: grouping by file suits small or medium projects with few routes per domain; grouping by package suits large applications with many endpoints; grouping by domain or feature becomes more scalable as the application grows.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-routing-organization.md.

Removed or changed: changed 'most scalable layout' to the page's 'more scalable as the application grows' and replaced the unbacked 'choose by size' line (including the path-nesting and feature-package size advice) with the page's own size guidance.

Method: documentation only; no commands were run.

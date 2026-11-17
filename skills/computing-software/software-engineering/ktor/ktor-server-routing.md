---
id: computing-software.software-engineering.ktor.ktor-server-routing
name: ktor-server-routing
category: computing-software
field: software-engineering
product: ktor
tags: [ktor, routing, path-parameters, kotlin, regex-routes, route-tracing]
level: intro
status: docs-checked
description: "Define Ktor server routes with verb functions, path patterns (wildcard, tailcard, {param}, regex), nesting, Route extension functions and route tracing."
sources:
  - https://github.com/ktorio/ktor-documentation/blob/main/topics/server-routing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ktor server routing

Routing is the core Ktor plugin for serving incoming requests. Use the `routing { }` function (shorthand for `install(RoutingRoot) { }`, import `io.ktor.server.routing.*`).

## Define a route
A route needs an HTTP verb, a path pattern and a handler. Use `route("/hello", HttpMethod.Get) { handle { ... } }` or the shorter verb functions `get`, `post`, `put`, `head` and so on:

```kotlin
routing {
    get("/hello") {
        call.respondText("Hello")
    }
}
```

## Path patterns
- `/user/{login}`: path parameter, mandatory; read with `call.parameters["login"]`.
- `/user/{login?}`: optional parameter; optional parameters may only appear at the end of the path.
- `/user/*`: wildcard, matches any one segment but cannot be missing (`/user/john` matches, `/user` does not).
- `/user/{...}`: tailcard, matches the rest of the path and can be empty (matches `/user` and `/user/john/settings`).
- `/user/{param...}`: path parameter with tailcard; read all segments with `call.parameters.getAll("param")`.
- `Regex(...)`: works with `route`, `get`, `post` etc. Named groups `(?<id>\d+)` are readable via `call.parameters["id"]`; unnamed groups only match, they cannot be read. The regex must consume whole path segments (`Regex("[a-z]+")` matches the `hello` part of `hello/1` and leaves `/1` for the next route).

`call.parameters` also contains query string parameters. Ktor distinguishes paths with and without a trailing slash; install the `IgnoreTrailingSlash` plugin to change that.

## Group and nest
Put verbs in one `routing` block, or group by path with `route("/customer") { get { } post { } }`. Nested `route` calls each add a path segment (`route("/order") { route("/shipment") { get { } } }` serves `/order/shipment`).

## Extension functions
Split routes into `fun Route.getOrderRoute() { get("/order/{id}") { } }` and register them inside `routing { getOrderRoute() }`.

## Trace routes
With logging configured, Ktor emits TRACE output showing why a route did not match (for example `FAILURE "No matched subtrees found"`). On the Native server, set the `KTOR_LOG_LEVEL` environment variable to `TRACE`.

## Checked

Date: 2026-11-07. Read each cited page in full, including embedded snippet files, and confirmed the claims in this skill against them: topics/server-routing.md.

Removed or changed: nothing; every claim, name and code sample was confirmed by the cited pages.

Method: documentation only; no commands were run.

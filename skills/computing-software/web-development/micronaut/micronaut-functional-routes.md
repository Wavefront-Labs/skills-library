---
id: computing-software.web-development.micronaut.micronaut-functional-routes
name: micronaut-functional-routes
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, functional-routes, http-routes, route-builder, route-groups, route-filters]
level: advanced
status: docs-checked
description: "Declare Micronaut HTTP routes in code with HttpRoutes and HttpRouteBuilder: handlers, body stages, groups, filters, conditions and error routes (experimental API)."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/functionalRoutes.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/functionalRoutes/functionalRoutesDeclaring.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/functionalRoutes/functionalRoutesGroups.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/functionalRoutes/functionalRoutesFilters.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/functionalRoutes/functionalRoutesConditions.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/functionalRoutes/functionalRoutesErrors.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Micronaut functional routes

Goal: handle HTTP requests with functions instead of controller methods. The page warns that the APIs in `web.router.builder`, `http.body.AsyncRequestBody`, `http.body.BodyElements` and `http.form` are experimental and may change.

## Declare routes
Define an `HttpRoutes` bean and declare routes on the `HttpRouteBuilder` it receives in `routes(...)`. You can implement `HttpRoutes` in a class or return it as a lambda from a factory method. Handler routes use the same server pipeline as controllers (argument binding, body readers and writers, content negotiation, application filters, CORS, error handling, executor selection). They coexist with controllers and honour `micronaut.server.context-path`. The order of `HttpRoutes` beans does not give their routes priority, and routes are fixed once the router is created.

Build a route in this order: HTTP method and URI, settings (`produces`, `consumes`, `executeOn`, `nonBlocking()`), optionally a body stage, then exactly one terminal call (`handle`, `handleAsync` or `respond`). An unfinished route fails application startup. `GET(uri, handler)` is a shortcut for `GET(uri).handle(handler)`.

```java
routes.GET("/items/{id}", (request, pathVariables) -> {
    long id = pathVariables.getLong("id");   // missing or invalid value gives 400
    return HttpResponse.ok(lookup(id));
});
routes.POST("/items")
    .body(Item.class)                         // decoded before the handler runs
    .handle((request, pathVariables, item) -> HttpResponse.ok(save(item)));
```

- A handler receives the request and `PathVariables`; throw `HttpStatusException` to return a status such as 404.
- Body stages: `body(Item.class)` or `body(Argument.listOf(Item.class))` decode the body; `body()` gives an async handler an `AsyncRequestBody` to read itself. `handleAsync` without a body stage does not read the body. `HttpRouteBuilder.nullableBody(...)` allows a missing body (null is passed instead of a 400).
- Invalid bodies produce 400, unsupported content types 415.
- `produces` and `consumes` set media types; routes use JSON by default and `consumesAll()` accepts any content type.
- `executeOn` selects a named executor, `nonBlocking()` marks the handler for event-loop execution; otherwise server thread selection applies as for a controller.
- Methods: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `route(HttpMethod, uri)`, `route(Set<HttpMethod>, uri)`, `route(String, uri)` for custom methods, and `any(uri)` for every method. A method-specific route beats `any(...)` on an otherwise equal match.
- `GET` also handles `HEAD`. A method mismatch gives 405 with an `Allow` header (not for paths matched by `any(...)`).
- Exceptions, including checked ones, go through the error routes. `responseType(Class)` or `responseType(Argument)` supplies a declared type to the response writer.

## Groups and filters
`routes.path(prefix, group -> ...)` groups routes under a prefix (it may contain path variables, not a query or fragment); `routes.group(group -> ...)` shares settings without a prefix. Groups nest. Group settings (media types, executor, annotations, conditions, order, attributes, port) are defaults that a route or nested group can override, and they apply to routes declared earlier in the callback too. A route at `/` maps to the group prefix.

Filter scopes:
- Route filters: `routes.GET(uri).before(...).and().handle(...)`.
- Group filters: apply to matched routes in the group and nested groups.
- Server filters: `routes.serverFilter(patterns...)` on the top-level builder only; they cover controllers, static resources and unmatched requests (404, 405, 415, 406). `preMatching()` runs before routing and can rewrite the URI used for route selection; only a pre-matching server filter can change which route is selected.

Group and route filters run only after a route matches, so they do not cover 404, 405, 415 or 406.

| Method | Behaviour |
|---|---|
| `before(...)` | change the request in place and continue |
| `beforeReplacing(...)` | return a response to stop, a replacement request to continue, or null to keep the current request |
| `after(...)` | change the response in place |
| `afterReplacing(...)` | return a replacement response, or null to keep the current one |

Each has an asynchronous variant such as `beforeAsync` returning a `CompletionStage`. Filters normally run on the filter-chain thread; use `executeOn(...)` then `and()` for blocking work. Order: server filters (with `@ServerFilter` beans, sorted by order), outer then nested group filters, route filters, handler; responses pass back in reverse. Body media types: a form route consumes the form media types regardless of the group; error and status routes do not inherit group media types or executors.

## Conditions, order, errors
- `where(...)` with `RequestCondition` matches on headers, query parameters, cookies, method, host, address or time, combined with `all`, `any`, `and`, `or`, `not`. A rejected condition removes the route from consideration; if none matches the response is 404. Keep conditions fast, non-blocking and free of side effects.
- `ValueMatcher` offers `equalTo`, `startsWith`, `oneOf`, `regex` and `present`; matching is case-sensitive unless `ignoringCase()`, and `regex` matches the whole value.
- Use `peerAddress(...)` for checks on the actual connection address; `remoteAddress(...)` uses the client-address resolver and can read forwarded headers, so use it for access control only behind a trusted proxy.
- `order(int)`: lower wins ties, default `0`; it does not override media-type matching or URI specificity. Remaining ties are ambiguous and produce 400.
- Body conditions (`RequestCondition.body(...)`, `bodyText(...)`, `bodyBytes(...)`, `bodyAsync(...)`) buffer the body; the limit defaults to `micronaut.server.max-request-buffer-size`; they cannot sit inside `any`, `or` or `not`.
- `constrain(...)` restricts path variables (predicates, collections of allowed strings or `ValueMatcher`).
- `attribute(name, value)` adds route metadata.
- `port(...)` restricts a route or group to a port (integer or property expression, 1 to 65535) and makes the server open it. Once any route declares a dedicated port, routes without one match only the default ports.
- `error(type, handler)` and `status(status, handler)` (plus `errorAsync`, `statusAsync`): on the top-level builder they are global (like `@Error(global = true)`); inside a group they are local to it and nested groups. Lookup: local `@Error` methods of the bean, innermost group outward, then global. Requests that match no route use only global handlers.
- Route and group response filters also apply to error-handler responses; if the error handler fails the server returns its default error response.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against all six cited pages. Removed: the sample code that relied on unread snippet files (tenant header filter, `getString`, `HttpResponse.created` and `noContent`), the `form()` FormData detail, and the closing claims about auto-validation and OpenAPI discovery, which none of the pages state.

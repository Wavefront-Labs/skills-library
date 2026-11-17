---
id: computing-software.web-development.micronaut.micronaut-routing-uri-templates
name: micronaut-routing-uri-templates
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, routing, uri-templates, path-variables, route-condition, routebuilder]
level: practitioner
status: docs-checked
description: "Map Micronaut controller routes with RFC-6570 URI templates, path variables, multiple URIs, route conditions, programmatic routes and compile-time validation."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/routing.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/pathVariables.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Route requests with URI templates

Goal: map HTTP methods and paths to controller methods.

## Annotations

`@Controller` value and method annotations take RFC-6570 URI templates. Method annotations: `@Get`, `@Post`, `@Put`, `@Patch`, `@Delete`, `@Head`, `@Options`, `@Trace`. All default to `/`. For non-standard verbs: `@CustomHttpMethod(method = "LOCK", value = "/{name}")`.

## Path variables

A variable binds automatically when the argument name matches; use `@PathVariable` for a different name or a default:

```java
@Controller("/issues")
public class IssuesController {
    @Get("/{number}")
    public String issue(Integer number) { return "Issue # " + number + "!"; }

    @Get("/issue/{number}")
    public String issueFromId(@PathVariable("number") Integer id) { return "Issue # " + id + "!"; }

    @Get("/default{/number}") // slash inside braces = optional variable
    public String issueFromIdOrDefault(@PathVariable(defaultValue = "0") Integer number) { ... }
}
```

Per the page's tests: `/issues/12` answers "Issue # 12", an invalid number gives 400, and a missing required variable gives 404. Optional variables need `@Nullable` (or `defaultValue`).

| Template | Matches |
|---|---|
| `/books/{id}` | `/books/1` |
| `/books/{id:2}` | variable of two characters max |
| `/books{/id}` | `/books/10` or `/books` |
| `/book{/id:[a-zA-Z]+}` | optional variable with regex |
| `/books{?max,offset}` | optional query parameters |
| `/books{/path:.*}{.ext}` | `/books/foo/bar.xml` |

Reserved characters such as `/` are excluded by default; `/books/{+path}` matches `/books/foo` and `/books/foo/bar`.

## More routing features

- Multiple URIs: `@Get(uris = {"/{name}", "/person/{name}"})` creates one route per template. A variable missing from some templates is treated as optional.
- Route condition: `@RouteCondition("#{request.parameters.getFirst('v').orElse(null) == '2'}")` (an EL expression with a `request` variable); server routes only, ignored on declarative clients.
- OPTIONS without an Origin header: set `micronaut.server.dispatch-options-requests: true`.
- Programmatic: subclass `DefaultRouteBuilder`, inject the controller, call e.g. `GET("/issues/show/{number}", issuesController, "issue", Integer.class)`. The route targets the bean of that type, so it must resolve to a single bean. Java method references cannot be used (type erasure).
- Build/match URIs with `UriMatchTemplate.of("/hello/{name}")`: `match(path)` and `expand(map)`.

## Compile-time validation

Add `io.micronaut:micronaut-http-validation` to the `annotationProcessor` scope. Compilation fails if an optional URI variable has a parameter that is neither `@Nullable` nor `Optional`, or a URI variable is missing from the method arguments. Disable with `-Dmicronaut.route.validation=false` (or remove the dependency).

## Checked

2026-11-08. Checked against the cited Micronaut 5.3.x guide .adoc source (raw file on GitHub) plus the Java doc-snippet sources the page includes via snippet:: (test-suite sources in micronaut-core 5.3.x), which hold the code shown. Pages were matched claim by claim (annotations, property names, class names, version gates, defaults) with a phrase checker over all pages and snippets, with targeted reads of the sections behind each unmatched item; pages were not all read line by line. Removed anything the pages did not state.

Method: documentation only; no commands were run.

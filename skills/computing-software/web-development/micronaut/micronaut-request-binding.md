---
id: computing-software.web-development.micronaut.micronaut-request-binding
name: micronaut-request-binding
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, request-binding, request-bean, query-value, header, cookie-value, binding]
level: practitioner
status: docs-checked
description: "Bind Micronaut controller parameters from headers, cookies, query values, body, streams and beans, and handle nullable and date types."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/binding.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bind request data to controller arguments

Goal: pick the right binding annotation or type for each part of a request.

## Annotations

All accept a `name` member; without it the parameter name is used.

| Annotation | Binds from |
|---|---|
| `@Body` | request body |
| `@CookieValue` | cookie |
| `@Header` | HTTP header |
| `@QueryValue` | query parameter |
| `@Part` | part of a multipart request |
| `@RequestAttribute` | request attribute (typically set in filters) |
| `@PathVariable` | path |
| `@RequestBean` | any Bindable value into one bean |

```java
@Get("/cookieName")     public String a(@CookieValue("myCookie") String myCookie)
@Get("/cookieInferred") public String b(@CookieValue String myCookie)   // same cookie
@Get("/headerName")     public String c(@Header("Content-Type") String contentType)
```

Use the explicit name when it contains hyphens (not valid in variable names).

## Nullability

A missing `@Header String contentType` makes the route unsatisfiable and returns 400 BAD REQUEST. Make it optional with `@Nullable @Header String contentType` (null is passed). `java.util.Optional` works but is discouraged for parameters.

## Dates and types

Date-times following RFC-1123 bind directly (`@Header ZonedDateTime date`); customize with `@Format("dd/MM/yyyy hh:mm:ss a z")`. Any type convertible from String via `ConversionService` can be bound; add a `TypeConverter` bean or register one via `TypeConverterRegistrar`. `BasicAuth` is bound by type.

## Multiple values into a POJO

- All query values: use the exploded operator, e.g. `@Get("/bookmarks/list{?paginationCommand*}")` with `@Valid @Nullable PaginationCommand`.
- Mixed sources: `@RequestBean`, e.g. `@Get("/movie/ticket/{movieId}{?minPrice,maxPrice}") ... list(@Valid @RequestBean MovieTicketBean bean)`. The bean is `@Introspected` and has fields annotated `@PathVariable`, `@QueryValue`, plus typed fields such as `HttpRequest<?>`. It may be a mutable getter/setter bean or an immutable one with an all-argument constructor (or `@Creator`). Compile with `-parameters` to use an immutable bean from another jar.

## InputStream body

```java
@Post(value = "/read", processes = MediaType.TEXT_PLAIN)
@ExecuteOn(TaskExecutors.IO)
String read(@Body InputStream inputStream) throws IOException { ... }
```

Reading the stream must be offloaded from the event loop.

## Resolution order

1. URI variables. 2. Query parameters for a `GET`. 3. `@Body` if present and the request allows a body. 4. Without `@Body`, parse the body (JSON or form data) and bind arguments from it (e.g. `Integer x, Integer y` from `{"x":10,"y":20}` as `application/json`, or `x=10&y=20` as `application/x-www-form-urlencoded`). 5. Otherwise 400 BAD REQUEST.

## Checked

2026-11-08. Checked against the cited Micronaut 5.3.x guide .adoc source (raw file on GitHub) plus the Java doc-snippet sources the page includes via snippet:: (test-suite sources in micronaut-core 5.3.x), which hold the code shown. Pages were matched claim by claim (annotations, property names, class names, version gates, defaults) with a phrase checker over all pages and snippets, with targeted reads of the sections behind each unmatched item; pages were not all read line by line. Removed anything the pages did not state.

Method: documentation only; no commands were run.

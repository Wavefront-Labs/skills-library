---
id: computing-software.software-engineering.quarkus.quarkus-rest-request-parameters
name: quarkus-rest-request-parameters
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, rest, jakarta-rest, query-param, request-parameters, java]
level: intro
status: docs-checked
description: "Bind path, query, header, cookie, form and matrix values in Quarkus REST endpoints with @RestPath/@RestQuery etc., group them in a bean, split delimited values."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/rest.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Binding request parameters in Quarkus REST

Use this when writing `quarkus-rest` endpoints that read parts of the HTTP request.

## Annotations

| HTTP element | Annotation |
|---|---|
| Path parameter | `@RestPath` (or nothing) |
| Query parameter | `@RestQuery` |
| Header | `@RestHeader` |
| Cookie | `@RestCookie` |
| Form parameter | `@RestForm` |
| Matrix parameter | `@RestMatrix` |

All live in `org.jboss.resteasy.reactive`. If you give no name, the Java parameter name is used; give one for headers like `@RestHeader("X-Cheese-Secret-Handshake")`. `@RestPath` is optional: a parameter whose name matches a URI template variable is assumed to be a path parameter. The standard `@PathParam`, `@QueryParam`, `@HeaderParam`, `@CookieParam`, `@FormParam`, `@MatrixParam` also work but require the name.

```java
@Path("/cheeses/{type}")
public class Endpoint {
    @POST
    public String allParams(@RestPath String type, @RestMatrix String variant,
                            @RestQuery String age, @RestCookie String level,
                            @RestHeader("X-Cheese-Secret-Handshake") String handshake,
                            @RestForm String smell) { ... }
}
```

## Prerequisite

Compile with parameter names kept: `-parameters` for javac, or `<parameters>` / `<maven.compiler.parameters>` in Maven.

## Grouping into a class

Put the annotated fields in a container class (or a record) and take it as `@BeanParam Parameters parameters`. `@BeanParam` is required for Jakarta REST compliance so tools like OpenAPI can introspect the parameters.

## Multi-value query parameters

`@RestQuery("name") List<String> names` collects repeated `?name=foo&name=bar`. To split one delimited value, add `@Separator(",")` (`org.jboss.resteasy.reactive.Separator`):

```java
public String hello(@RestQuery("name") @Separator(",") List<String> names)
```

Verify: `GET /hello?name=foo,bar` returns `hello foo bar` (the page's example, which joins names with a space).

## Collect everything

A bare `@RestQuery` or `@RestHeader` (no name) on a `MultivaluedMap<String, String>` gathers all query parameters or all headers; repeated names give one entry with all values. Specifying a name disables this behaviour.

## Conversion types

Besides `String`, parameters may be primitives, types with a single-`String` constructor, types with static `valueOf`/`fromString` (enums use `fromString`), types with a registered `ParamConverterProvider`, and `List`/`Set`/`SortedSet` of those. Dates: `java.time.Temporal` types work; set a pattern with `@org.jboss.resteasy.reactive.DateFormat`.

## Gotcha: silent 4xx

Parameter-handling exceptions are not logged by default. To see why a status was returned:

```properties
quarkus.log.category."org.jboss.resteasy.reactive.server.handlers.ParameterHandler".level=DEBUG
```

## Checked

2026-11-07. Matched against the text (with includes) of: rest.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.

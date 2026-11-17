---
id: computing-software.software-engineering.quarkus.quarkus-rest-exception-mapping
name: quarkus-rest-exception-mapping
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, rest, exception-mapping, server-exception-mapper, error-handling, java]
level: practitioner
status: docs-checked
description: "Turn exceptions into HTTP responses in Quarkus REST with WebApplicationException, @ServerExceptionMapper, global mappers, @UnwrapException and the Jackson mapper opt-out."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/rest.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exception mapping in Quarkus REST

## Simple case

Throw a `jakarta.ws.rs.WebApplicationException` or a subtype (`BadRequestException` gives 400, `NotFoundException("msg")` gives 404). Change its log level with:

```properties
quarkus.log.category."WebApplicationException".level=DEBUG
```

## Mapping service exceptions

For exceptions thrown from layers that know nothing of Jakarta REST, annotate a method with `@org.jboss.resteasy.reactive.server.ServerExceptionMapper`. It takes the exception type as a parameter and returns `RestResponse` (or `Response`, or `Uni<RestResponse>` / `Uni<Response>`):

```java
@ServerExceptionMapper
public RestResponse<String> mapException(UnknownCheeseException x) {
    return RestResponse.status(Response.Status.NOT_FOUND, "Unknown cheese: " + x.name);
}
```

Other allowed parameters: any context object (for example `UriInfo`) and `ContainerRequestContext`.

## Scope

A mapper declared inside a REST endpoint class only handles exceptions thrown in that same class. For a global mapper, declare it in a class that is not a REST endpoint (the page uses a plain `ExceptionMappers` class). The standard Jakarta REST `ExceptionMapper` provider style also works.

## Gotchas

- `@ServerExceptionMapper` methods do not run CDI interceptors (such as method-level security) that apply to other methods of the class; add the interceptor annotations to the method to opt in.
- Quarkus REST does not log the original exception by default (for security). To see it before mapping runs, set `quarkus.log.category."org.jboss.resteasy.reactive.common.core.AbstractResteasyReactiveContext".level=DEBUG`.
- Response filters (`ContainerResponseFilter`, `@ServerResponseFilter`) are still called for handled exceptions.
- Exception mappers are not invoked on streamed `Multi` responses, because part of the response may already be written.

## Wrapped exceptions

Mappers normally ignore the cause. If your exception arrives wrapped (for example `CompletionException`), put `@UnwrapException` on the wrapper type, or on any class with the wrapper types as the annotation value (`@UnwrapException({CompletionException.class, RuntimeException.class})`). The `strategy` attribute (`ExceptionUnwrapStrategy`) is:

- `UNWRAP_IF_NO_MATCH` (default): unwrap only if neither the exception nor any supertype has a mapper.
- `UNWRAP_IF_NO_EXACT_MATCH`: unwrap if there is no mapper for the exact type.
- `ALWAYS`: unwrap first, fall back to the wrapper's mappers only if no cause matches.

## Jackson: MismatchedInputException

With Jackson, Quarkus ships a built-in mapper for `MismatchedInputException` (HTTP 400). Because it is a subtype of `JsonMappingException`, it beats your `JsonMappingException` mapper. Disable it:

```properties
quarkus.rest.exception-mapping.disable-mapper-for=io.quarkus.resteasy.reactive.jackson.runtime.mappers.BuiltinMismatchedInputExceptionMapper
```

## Checked

2026-11-07. Matched against the text (with includes) of: rest.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.

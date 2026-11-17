---
id: computing-software.web-development.micronaut.micronaut-error-handling
name: micronaut-error-handling
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, error-handling, error-annotation, exception-handler, status-handler, error-response]
level: practitioner
status: docs-checked
description: "Handle errors in a Micronaut server with @Error methods, status handlers, ExceptionHandler beans, built-in handlers and error response formatting."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/errorHandling.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/errorHandling/statusHandlers.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/errorHandling/localErrorHandling.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/errorHandling/globalErrorHandling.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/errorHandling/exceptionHandler.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/errorHandling/exceptionHandler/customExceptionHandler.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/errorHandling/exceptionHandler/builtInExceptionHandlers.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/errorHandling/errorFormatting.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Handle errors

Goal: turn exceptions and status codes into the responses you want.

## @Error methods

`@Error` methods must live in a class annotated `@Controller`. It takes an exception class or an HTTP status; if the exception is a method argument, omit the annotation's exception property. Local (default) handlers only respond to exceptions from routes in the same controller and are searched first. Global handlers can answer any exception.

```java
@Error                                   // local, by argument type
public HttpResponse<JsonError> jsonError(HttpRequest request, JsonSyntaxException e) {
    JsonError error = new JsonError("Invalid JSON: " + e.getMessage())
            .link(Link.SELF, Link.of(request.getUri()));
    return HttpResponse.<JsonError>status(HttpStatus.BAD_REQUEST, "Fix Your JSON").body(error);
}

@Error(global = true)
public HttpResponse<JsonError> error(HttpRequest request, Throwable e) {
    return HttpResponse.<JsonError>serverError().body(new JsonError("Bad Things Happened: " + e.getMessage()));
}

@Error(status = HttpStatus.NOT_FOUND)
public HttpResponse<JsonError> notFound(HttpRequest request) {
    return HttpResponse.<JsonError>notFound().body(new JsonError("Person Not Found"));
}
```

Rules: no identical global `@Error` declarations; identical non-global ones cannot repeat in one controller; if the same parameter exists as global and local, the local one wins. Handlers can use request binding annotations (e.g. headers), but binding the body may fail if the original bytes were already discarded after binding to the route's parameter.

## ExceptionHandler

Implement `ExceptionHandler<E, R>` as a bean. An `@Error` capturing the same exception has precedence over it. Example: unhandled `OutOfStockException` yields 500; to answer 400:

```java
@Produces
@Singleton
@Requires(classes = {OutOfStockException.class, ExceptionHandler.class})
public class OutOfStockExceptionHandler implements ExceptionHandler<OutOfStockException, HttpResponse> {
    private final ErrorResponseProcessor<?> errorResponseProcessor;
    // constructor injection omitted
    @Override
    public HttpResponse handle(HttpRequest request, OutOfStockException e) {
        return errorResponseProcessor.processResponse(ErrorContext.builder(request)
                .cause(e).errorMessage("No stock available").build(), HttpResponse.badRequest());
    }
}
```

Built-in handlers include `ConstraintExceptionHandler` (`ConstraintViolationException`), `ContentLengthExceededHandler`, `ConversionErrorHandler`, `DuplicateRouteHandler`, `HttpStatusHandler` (`HttpStatusException`, `UnsupportedMediaException`, `NotFoundException`, `NotAcceptableException`), `NotAllowedExceptionHandler`, `JsonExceptionHandler`, `URISyntaxHandler`, `UnsatisfiedArgumentHandler`, `UnsatisfiedRouteHandler`.

## Error response format

Responses are built by an `ErrorResponseProcessor` bean. JSON uses a `JsonErrorResponseBodyProvider` (default: vnd.error); HTML uses an `HtmlErrorResponseBodyProvider`, localizable with message codes `<status>.error.bold`, `<status>.error.title`, `<status>.error`.

For unhandled exceptions the response omits the exception message (it stays in server logs). Set `micronaut.server.error-response-include-message` to `always`, or `on-param` (message included when the request has a `message` query parameter other than `false`); default `never`. This may expose sensitive details and is not recommended for production. To change anything beyond error items, override the exception handler handling that exception.

## Checked
2026-11-07. Every claim, parameter, default, config key, class, method and code block was compared with the cited pages and their included snippets; nothing needed changing.

Method: documentation only; no commands were run.

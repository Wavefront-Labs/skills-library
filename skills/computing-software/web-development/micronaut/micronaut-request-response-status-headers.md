---
id: computing-software.web-development.micronaut.micronaut-request-response-status-headers
name: micronaut-request-response-status-headers
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, request-response, http-status, content-disposition, httprequest, serverrequestcontext]
level: practitioner
status: docs-checked
description: "Take full control of a Micronaut request and response: HttpRequest binding, HttpResponse factories, @Status, custom status codes and @ContentDisposition."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/requestResponse.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/statusAnnotation.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/contentDispositionAnnotation.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Control the request, response, status and download headers

Goal: read the whole request, build the response, set the status code and force a download.

## Bindable request interfaces

Controller parameters can be `HttpRequest`, `HttpHeaders`, `HttpParameters` (URI variables and request parameters) or `Cookies`. Declare `HttpRequest<MyClass>` with a concrete generic type if you need the body; otherwise it may not be available.

## Build the response

Use the static factories of `HttpResponse`, which return a `MutableHttpResponse`:

```java
@Controller("/request")
public class MessageController {
    @Get("/hello")
    public HttpResponse<String> hello(HttpRequest<?> request) {
        String name = ...;   // value of the query parameter "name", read from the request
        return HttpResponse.ok("Hello " + name + "!!").header("X-My-Header", "Foo");
    }
}
```

## Getting the request elsewhere

- `ServerRequestContext.currentRequest()` returns an `Optional<HttpRequest>` from a static context. It generally works inside a reactive flow, but the recommended way is to take the request as an argument and pass it down; the context is not propagated when other threads emit the data.
- With Project Reactor, prefer the Reactor context, which does not use a thread local:

```java
return Mono.deferContextual(ctx -> {
    HttpRequest<?> request = ctx.get(ServerRequestContext.KEY);
    ...
});
```

## Status codes

The default status is 200. Three ways to change it:

```java
@Status(HttpStatus.CREATED)
@Get(produces = MediaType.TEXT_PLAIN)
public String index() { return "success"; }

@Get("/http-status")
public HttpStatus httpStatus() { return HttpStatus.CREATED; }

@Get(value = "/http-response", produces = MediaType.TEXT_PLAIN)
public HttpResponse httpResponse() { return HttpResponse.status(HttpStatus.CREATED).body("success"); }
```

For codes outside the `HttpStatus` enum use `HttpResponse#status(int, String)`.

Since 5.3.0, an action returning `CompletionStage<HttpStatus>` treats the completed status as a deliberate response with no body (`CompletableFuture.completedFuture(HttpStatus.ACCEPTED)` answers `202 Accepted`). Before, it answered `404 Not Found` by default, or `204 No Content` when `micronaut.server.not-found-on-missing-body` was `false`. An applicable `@Status` still takes precedence for the asynchronous result.

## Content-Disposition

`@ContentDisposition` sends the header regardless of return type:

```java
@ContentDisposition(filename = "report.csv")
@Get(value = "/report", produces = MediaType.TEXT_PLAIN)
public String report() { return "name,amount\nwidget,42"; }

@ContentDisposition(type = ContentDisposition.Type.INLINE)
@Get(value = "/preview", produces = MediaType.TEXT_PLAIN)
public String preview() { ... }
```

The first yields `Content-Disposition: attachment; filename="report.csv"; filename*=utf-8''report.csv`, prompting a download; `INLINE` asks the browser to display the response instead.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against `requestResponse.adoc`, `statusAnnotation.adoc` and `contentDispositionAnnotation.adoc`: bindable interfaces, the `HttpRequest<MyClass>` body note, `MutableHttpResponse` factories, `ServerRequestContext` caveat, Reactor context alternative, default 200, the three status styles, `HttpResponse#status(int,String)`, the 5.3.0 `CompletionStage<HttpStatus>` change and the `Content-Disposition` header text. Removed: the `getFirst("name")` call, which the pages do not show.

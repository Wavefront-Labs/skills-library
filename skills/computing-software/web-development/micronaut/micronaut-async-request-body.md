---
id: computing-software.web-development.micronaut.micronaut-async-request-body
name: micronaut-async-request-body
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, async-request-body, asyncrequestbody, completionstage, body-elements, request-body-copy]
level: advanced
status: docs-checked
description: "Read a Micronaut request body on demand with AsyncRequestBody: decode, text, elements, copy in filters, and the buffer limits and 4xx errors involved."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/asyncRequestBody.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AsyncRequestBody

Goal: let a route or filter decide how and when to read the body, returning a `CompletionStage` instead of blocking. `AsyncRequestBody` and `BodyElements` (package `io.micronaut.http.body`) are experimental and may change.

## Decode and read

```java
@Post
public CompletionStage<HttpResponse<Person>> save(AsyncRequestBody body) {
    return body.body(Person.class)
        .thenCompose(this::store)
        .thenApply(HttpResponse::created);
}
```

`body(Type)` decodes like a `@Body` argument (same readers and errors): malformed JSON gives `400 Bad Request`; a body above `micronaut.server.max-request-buffer-size` gives `413 Request Entity Too Large`.

Other reads:

- `text()`, `text(maximumBytes)`, `text(maximumBytes, charset)`
- `bytes(maximumBytes)`
- `transferTo(path)`: writes to a new file without buffering, so the buffer limit does not apply
- `takeBody()`: a `CloseableByteBody`, which you must consume or close
- `discardBody()`; `form()` and `parts()` (see the form uploads page)
- `hasBody()` and `expectedBodySize()` inspect without reading

`body`, `text` and `bytes` are always limited by `max-request-buffer-size`; `maximumBytes` can only lower it. To read bigger bodies use `elements`, `transferTo` or `takeBody()`.

## Rules

- The body can be read once; a second read throws `IllegalStateException`. Unread bodies are discarded at request end.
- Work must be part of the returned stage: reads left open (e.g. `elements`, `transferTo` not returned) are aborted when the method completes.
- `body` and `elements` refuse `Publisher`, `CompletableFuture`, other async types and `InputStream` (`IllegalArgumentException`).

## Elements of a JSON array or stream

```java
@Post(uri = "/import", consumes = {MediaType.APPLICATION_JSON, MediaType.APPLICATION_JSON_STREAM})
public CompletionStage<String> importPeople(AsyncRequestBody body) {
    AtomicInteger count = new AtomicInteger();
    return body.elements(Person.class)
        .forEach(person -> store(person).thenRun(count::incrementAndGet))
        .thenApply(done -> "Imported " + count.get());
}
```

The next element is read when the consumer's stage completes; `next()` reads one (empty `Optional` at the end). The buffer limit applies per element (whole body limited by `micronaut.server.max-request-size`); oversized element gives `413`; other media types give `415 Unsupported Media Type`. Non-Netty servers (e.g. servlet) need `micronaut-http-netty` on the runtime classpath or the first read fails with `UnsupportedOperationException`. Consumers must not block.

## Filters: copy to peek

A `@ServerFilter` `@RequestFilter` method may declare `AsyncRequestBody`. Reading it directly consumes the body, so the route later fails (500 for body-reading arguments). To look and leave it for the route, read a copy:

```java
@ServerFilter("/messages")
public class SpamFilter {
    @RequestFilter
    public CompletionStage<@Nullable HttpResponse<?>> rejectSpam(AsyncRequestBody body) {
        return body.copy().text()
            .thenApply(text -> text.contains("spam") ? HttpResponse.badRequest("Spam is not accepted") : null);
    }
}
```

A copy is held entirely to `max-request-buffer-size` (`413` above it), for streaming reads too. `form(FormOptions.defaults().withRawValues())` reads urlencoded values without percent-decoding.

## Checked
2026-11-07. Every claim, parameter, default, config key, class, method and code block was compared with the cited pages and their included snippets; nothing needed changing.

Method: documentation only; no commands were run.

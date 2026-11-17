---
id: computing-software.web-development.micronaut.micronaut-filter-read-request-body
name: micronaut-filter-read-request-body
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, filter-body, byte-body, async-request-body, split-backpressure, request-body]
level: advanced
status: docs-checked
description: "Read or log a request body inside a Micronaut filter while the controller still receives it, using AsyncRequestBody copy() or ByteBody split() with the right backpressure mode."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/filters/filterBodyBuffer.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/byteBody.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/byteBody/byteBodyExample.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/byteBody/byteBodyPrimary.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/byteBody/byteBodySplitting.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Reading the request body in a Micronaut filter

Goal: inspect the body bytes (checksum, signature, logging) before the route runs without stealing the body from the controller's `@Body` argument.

## Option 1: buffer a copy with AsyncRequestBody
Take an `AsyncRequestBody` argument in a request filter method (or `AsyncRequestBody.of(request)`, Netty server), read a `copy()`, and complete with `null` to proceed.

```java
@ServerFilter("/checksum")
public class ChecksumFilter {
    @RequestFilter
    @PreMatching
    public CompletionStage<@Nullable HttpResponse<?>> verify(HttpRequest<?> request) {
        String expected = request.getHeaders().get("X-Content-SHA256");
        return AsyncRequestBody.of(request)
            .copy()
            .bytes(1024 * 1024)            // buffers without blocking the event loop
            .thenApply(bytes -> sha256(bytes).equals(expected)
                ? null                      // proceed; route still reads the body
                : HttpResponse.badRequest("Checksum mismatch"));
    }
}
```

The controller then simply declares `@Body String body`.

- The copy is held in memory, limited by `micronaut.server.max-request-buffer-size` and by the smaller limit passed to `bytes`; a bigger body fails with `ContentLengthExceededException`, answered `413 Request Entity Too Large`.
- Reading without `copy()` consumes the body. Each `AsyncRequestBody.of` call is an independent reader sharing consumption state.
- Nothing is read until the filter reads, so other requests keep streaming. With `Expect: 100-continue`, `100 Continue` is sent only when the filter reads; a filter answering `401` first never gets the body.
- An unsupported server (e.g. some servlet servers) throws `UnsupportedOperationException` for `AsyncRequestBody.of`; take the argument in the filter method instead.

## Option 2: split the ByteBody
`ServerHttpRequest.byteBody()` is claimed once (a primary operation such as `toInputStream()`, `toByteArrayPublisher()`, or `buffer()`, which is capped by `max-request-buffer-size`). To share it, `split()` before claiming; the split result is a `CloseableByteBody` you must close.

```java
@RequestFilter
public void logBody(ServerHttpRequest<?> request) {
    try (CloseableByteBody ourCopy = request.byteBody()
             .split(ByteBody.SplitBackpressureMode.SLOWEST)
             .allowDiscard()) {
        Flux.from(ourCopy.toByteArrayPublisher())
            .onErrorComplete(ByteBody.BodyDiscardedException.class)
            .subscribe(array -> LOG.info("Received body: {}", Base64.getEncoder().encodeToString(array)));
    }
}
```

Backpressure modes: `SLOWEST` (default; consumers read concurrently), `FASTEST`, `ORIGINAL`, `NEW`.

## Gotcha: deadlock with SLOWEST
If one body is read to completion before the other is read at all (buffer a copy in the filter, then let the controller read), `SLOWEST` deadlocks: the request hangs until the idle timeout and `100 Continue` is never sent. Use `split(SplitBackpressureMode.FASTEST)` for that pattern. If one body may never be consumed, close it or call `allowDiscard()`. `InputStream` access blocks, so use `@ExecuteOn(TaskExecutors.BLOCKING)`.

## Checked

2026-11-08. Checked against the cited Micronaut 5.3.x guide .adoc source (raw file on GitHub) plus the Java doc-snippet sources the page includes via snippet:: (test-suite sources in micronaut-core 5.3.x), which hold the code shown. Pages were matched claim by claim (annotations, property names, class names, version gates, defaults) with a phrase checker over all pages and snippets, with targeted reads of the sections behind each unmatched item; pages were not all read line by line. Removed anything the pages did not state.

Method: documentation only; no commands were run.

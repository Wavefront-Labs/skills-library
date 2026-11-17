---
id: computing-software.web-development.micronaut.micronaut-sse-streaming-responses
name: micronaut-sse-streaming-responses
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, sse, server-sent-events, streaming, writable, file-download, streamedfile]
level: practitioner
status: docs-checked
description: "Stream responses from Micronaut controllers: server-sent events, chunked Publishers, blocking Writable/InputStream output, file downloads and 404-on-null behaviour."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/sse.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/serverIO.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/transfers.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Streaming responses and downloads in Micronaut

## Server-sent events
Return a Reactive Streams `Publisher` that emits `io.micronaut.http.sse.Event` objects. The response is `text/event-stream`, and each payload (for example a `Headline` data class) is converted to JSON. Build events with `Event.of(value)`; the methods of the `Event` interface customise the data sent, including event ids, comments and retry timeouts. The publisher can emit from a background task, an event system and so on. The page's example uses Reactor `Flux.generate` and notes that it runs on the controller's thread; you could use `subscribeOn` or map an existing hot `Flux`.

You typically want to schedule SSE streams on a separate executor: the page's example puts `@ExecuteOn` on the controller method to run the stream on the I/O executor.

Output looks like:
```
data: {"title":"Micronaut 1.0 Released","description":"Come and get it"}
data: {"title":"Micronaut 2.0 Released","description":"Come and get it"}
```

## Chunked Publisher responses
Returning a `Publisher<String>`, `Flux<byte[]>`, `Flux<ByteBuf>` or `Flux<Book>` (a POJO is encoded as JSON by default, without blocking) uses `Transfer-Encoding: chunked` and keeps writing until the publisher calls `onComplete`. The server requests one item, writes it, then requests the next, controlling back pressure. `Flowable` equivalents work too. Scheduling any blocking I/O done on subscribing is up to the publisher implementation. Using Reactor `Flux` or `Mono` needs the Micronaut Reactor dependency, and RxJava `Flowable`, `Single` or `Maybe` needs the Micronaut RxJava dependency, for the converters.

## Blocking output
- Return a `io.micronaut.core.io.Writable` from any controller method (it has signatures for writing to a `Writer` or `OutputStream`); the blocking I/O is shifted to the I/O thread pool so the Netty event loop is not blocked. Configure that pool in the server thread pool settings.
- Return an `InputStream`; its contents become the response body, and reading is offloaded to the IO thread pool if the controller method runs on the event loop.

## 404 behaviour
Returning `null` or an empty `Mono` triggers a 404. An empty `Publisher` or `Flux` is a streaming response, which gives an empty array for JSON; annotate the method with `@SingleResult` to disable streaming. Set `micronaut.server.not-found-on-missing-body` to `false` to disable the 404 on a null body or empty publisher.

## Sending files
- Return a `File`: its `Content-Type` is calculated from the file name. To control the media type or force a download (`Content-Disposition`), return a `SystemFile`: `new SystemFile(file).attach("myfile.txt")` or `new SystemFile(file, MediaType.TEXT_HTML_TYPE)`.
- For data without a `File` (for example resources in JAR files) return a `StreamedFile`: `new StreamedFile(inputStream, MediaType.TEXT_PLAIN_TYPE)`. Its constructor also accepts a `java.net.URL`, and `attach(String filename)` sets `Content-Disposition`.
- Avoid `PipedInputStream` / `PipedOutputStream` as the source of a `StreamedFile` or other `InputStream` response: the page warns of broken-pipe errors on short-lived threads, especially when the blocking executor uses virtual threads. Prefer a file, URL or reactive `Publisher`.
- The server returns `304 Not Modified` if the file is unchanged and the request has the appropriate header. If the client accepts encoded responses, text-based files larger than 1KB are encoded by default; the threshold is configurable (see the server configuration reference). File responses include caching headers by default; the `Cache-Control` options are in the same reference.
- A reactive stream (`Flux`, `Flowable` or any `Publisher`) is returned without buffering the whole response. To force a browser download of streamed data such as CSV lines, set a `Content-Disposition: attachment` header. Wrapping the stream in `HttpResponse<Flux<String>>` still streams; it only lets you set headers or a custom status.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against `sse.adoc`, `serverIO.adoc` and `transfers.adoc`. Removed: the full controller and CSV code samples (pages embed them from source files that were not readable; the CSV header value and `/headlines` route were not stated) and the claim that the text-file encoding threshold is the only configurable detail.

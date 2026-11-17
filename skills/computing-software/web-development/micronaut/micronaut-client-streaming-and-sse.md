---
id: computing-software.web-development.micronaut.micronaut-client-streaming-and-sse
name: micronaut-client-streaming-and-sse
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, http-client, streaming, json-stream, server-sent-events, sse, read-idle-timeout]
level: practitioner
status: docs-checked
description: "Consume JSON streams and Server Sent Events from Micronaut clients with Publisher, BodyElements or SseClient, and adjust read-idle-timeout."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpClient/clientAnnotation/clientAnnotationStreaming.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpClient/lowLevelHttpClient/clientStreaming.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: read a streamed response without blocking.

## Declarative JSON stream

```java
@Client("/streaming")
public interface HeadlineClient {
    @Get(value = "/headlines", processes = APPLICATION_JSON_STREAM)
    Publisher<Headline> streamHeadlines();
}
```

A JSON stream (`application/x-json-stream`, one object per line) is not valid JSON, so it cannot be `application/json`. The client handles both: JSON-stream objects, and a JSON array served as `application/json` when the return is a non-single `Publisher` (elements stream as they arrive). Take the first element with `Mono.from(client.streamHeadlines()).block()`.

## Low-level streaming

`ReactorStreamingHttpClient` offers `dataStream(request)` (`Flux` of `ByteBuffer`), `exchangeStream(request)` (`HttpResponse` wrapping that flux) and `jsonStream(request)`:

```java
Flux<Headline> headlineStream = Flux.from(client.jsonStream(
        GET("/streaming/headlines"), Headline.class));
```

Subscribe with a `Subscriber` whose `onSubscribe` calls `s.request(1)` to control back pressure. The server does not need to be Micronaut.

## Without Reactive Streams

Return `CompletionStage<BodyElements<T>>` from a declarative method (the stage completes when the response arrives):

```java
BodyElements<Headline> headlines = headlineClient.streamHeadlines()
        .toCompletableFuture().get(10, TimeUnit.SECONDS);
Optional<Headline> first = headlines.next().toCompletableFuture().get(10, TimeUnit.SECONDS);
headlines.close();   // discards the rest and releases the connection
```

`CompletionStage<HttpResponse<BodyElements<T>>>` also exposes status and headers. `AsyncStreamingHttpClient` (from `toAsyncStreaming()` on a `StreamingHttpClient`, or injected) has `jsonStream`, `exchangeJsonStream`, `dataStream`, `exchangeStream`; `forEach` reads all elements. Close streams you do not read to the end. Error statuses fail the stage with `HttpClientResponseException`. Stages complete on an I/O thread: do not block in them.

## Read timeout

Streaming responses ignore the default `readTimeout` (10 s). Instead `read-idle-timeout` (default 5 minutes) closes idle connections. For longer gaps:

```yaml
micronaut:
  http:
    client:
      read-idle-timeout: 10m
```

## Server Sent Events

`SseClient` streams SSE. A declarative method that processes `TEXT_EVENT_STREAM`:

```java
@Client("/streaming/sse")
public interface HeadlineClient {
    @Get(value = "/headlines", processes = TEXT_EVENT_STREAM)
    Publisher<Event<Headline>> streamHeadlines();
}
```

The generic type may be `Event<T>` (full event) or a POJO (only the JSON data).

`exchangeEventStream` serves endpoints that answer with either one body or an event stream; each event arrives wrapped in an `HttpResponse` exposing status and headers:

```java
Flux.from(sseClient.exchangeEventStream(request, Argument.STRING, Argument.STRING))
    .mapNotNull(HttpResponse::body).map(Event::getData);
```

Error statuses fail the publisher with `HttpClientResponseException` carrying the decoded error body. The async variant on `AsyncStreamingHttpClient` returns a stage whose `body()` is a `BodyElements<Event<T>>`; `eventStream` sets `Accept: text/event-stream`. Keep the connection reserved only until the elements are read or closed.

## Checked
2026-11-07. Every claim, parameter, default, config key, class, method and code block was compared with the cited pages and their included snippets; nothing needed changing.

Method: documentation only; no commands were run.

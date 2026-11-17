---
id: computing-software.software-engineering.quarkus.quarkus-rest-multi-streaming
name: quarkus-rest-multi-streaming
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, rest, streaming, mutiny, server-sent-events, restmulti]
level: advanced
status: docs-checked
description: "Stream Quarkus REST responses with Multi: RestMulti headers/status, concurrent demand, JSON objects without an array, and Server-Sent Events including custom events."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/rest.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Streaming responses in Quarkus REST

Return `io.smallrye.mutiny.Multi` from an endpoint to stream element by element (text or binary).

## Caveat

Response filters and exception mappers are not invoked on streamed responses: headers and status cannot be changed after the initial response, and part of the body may already be sent.

## Headers and status: RestMulti

Return `org.jboss.resteasy.reactive.RestMulti` to set them:

```java
return RestMulti.fromMultiData(logs).status(222).header("foo", "bar").build();
```

When headers or status come from an async call, use `RestMulti.fromUniResponse(uni, SomeResponse::data, r -> Map.of("MyHeader", List.of(r.myHeader())))`: the second argument extracts the `Multi` of data, the third the header map.

## Concurrency and ordering

By default `RestMulti` signals demand of 1, preserving sequential order. Call `.withDemand(5)` to let up to 5 items be produced concurrently; order in the output is then not guaranteed. Higher demand uses more resources and loads downstream services; consider `Multi.capDemandsTo(long)` or `capDemandsUsing(LongFunction)`.

## JSON objects without an array

With `application/json`, items are wrapped in a JSON array by default. Use `.encodeAsJsonArray(false)` on the builder to emit separate objects (the prose mentions `encodeAsArray`, while the code example uses `encodeAsJsonArray(false)`). Clients then need different parsing, but can consume objects as they arrive.

## Server-Sent Events

Annotate with `@RestStreamElementType(MediaType.APPLICATION_JSON)` to send each element as JSON; no `@Produces(MediaType.SERVER_SENT_EVENTS)` needed:

```java
@GET
@RestStreamElementType(MediaType.APPLICATION_JSON)
public Multi<Book> stream() { return books; }
```

For custom events (e.g. the SSE `event` field), inject `jakarta.ws.rs.sse.Sse` and return `Multi<OutboundSseEvent>`:

```java
return books.map(b -> sse.newEventBuilder().name("book").data(b.title).build());
```

with `@RestStreamElementType(MediaType.TEXT_PLAIN)`.

Warning: `RestMulti.fromUniResponse` cannot manipulate headers or status for SSE responses, because they cannot be delayed until the response is available.

## Related

Async endpoints returning `Uni` cancel the pipeline when the HTTP connection closes; `@org.jboss.resteasy.reactive.server.Cancellable` controls this on classes or methods.

## Checked

2026-11-07. Matched against the text (with includes) of: rest.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.

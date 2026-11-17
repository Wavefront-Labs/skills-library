---
id: computing-software.web-development.micronaut.micronaut-low-level-http-client
name: micronaut-low-level-http-client
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, http-client, low-level-client, retrieve, exchange, multipart]
level: intro
status: docs-checked
description: "Use the Micronaut HttpClient directly: inject it, retrieve or exchange GET and POST requests (text, JSON, form, multipart), add headers and enable tracing."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpClient/lowLevelHttpClient.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpClient/lowLevelHttpClient/clientBasics.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpClient/lowLevelHttpClient/clientPostRequests.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpClient/lowLevelHttpClient/clientUploads.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: call HTTP endpoints with the low-level `io.micronaut.http.client.HttpClient`.

## Obtain a client

```java
@Client("https://api.twitter.com/1.1") @Inject HttpClient httpClient;
```

In Kotlin escape the placeholder: `@field:Client("\${myapp.api.twitter.url}") @Inject lateinit var httpClient: HttpClient`. The `@Client` value is an absolute URI, a relative URI (current server) or a service identifier. `@Client` is a custom scope that stops clients at application shutdown. `HttpClient.create(...)` also works but is not recommended: you must shut it down yourself and no injection happens.

`ReactorHttpClient` (Micronaut Reactor) returns `Flux` instead of `Publisher`. `AsyncHttpClient` returns `CompletionStage`; the future from `exchange` or `retrieve` owns the request, so cancelling it or completing it exceptionally (including `orTimeout`) aborts the work, but cancelling only a dependent stage (`thenApply`, ...) does not. Do not block these futures on a client event loop.

## GET

- `retrieve` returns the body (a `String` by default); `exchange` returns the whole `HttpResponse`.
- `toBlocking()` gives a blocking client; the guide uses it for illustration only. In controllers return a `Mono`/`Flux` instead.

```java
String result = client.toBlocking().retrieve("/hello/John");

Flux<String> response = Flux.from(client.retrieve(
        GET("/hello/John").header("X-My-Header", "SomeValue")));

Flux<Map> m = Flux.from(client.retrieve(GET("/greet/John"), Map.class));
// Argument.of(Map.class, String.class, String.class) customises key/value types
Flux<Message> p = Flux.from(client.retrieve(GET("/greet/John"), Message.class));

Flux<HttpResponse<Message>> call = Flux.from(client.exchange(GET("/greet/John"), Message.class));
Optional<Message> body = call.blockFirst().getBody(Message.class);
```

JSON is decoded with Jackson. For other content types register an `io.micronaut.http.codec.MediaTypeCodec` bean.

## POST and other methods

`HttpRequest` has factories `GET, OPTIONS, HEAD` (no body), `POST, PUT, PATCH` (body required) and `DELETE`; `create` takes any `HttpMethod`.

```java
client.exchange(POST("/hello", "Hello John")
        .contentType(MediaType.TEXT_PLAIN_TYPE)
        .accept(MediaType.TEXT_PLAIN_TYPE), String.class);   // default type is application/json

client.exchange(POST("/greet", new Message("Hello John")), Message.class);    // JSON
client.exchange(POST("/amazon/book/{title}", new Book("The Stand")), Book.class); // URI template filled from the body
client.exchange(POST("/amazon/book/{title}", new Book("The Stand"))
        .contentType(MediaType.APPLICATION_FORM_URLENCODED), Book.class);     // form data
```

## Multipart upload

```java
MultipartBody requestBody = MultipartBody.builder()
        .addPart("data", file.getName(), MediaType.TEXT_PLAIN_TYPE, file)
        .build();                                   // at least one part required
HttpRequest.POST("/multipart/upload", requestBody)
        .contentType(MediaType.MULTIPART_FORM_DATA_TYPE)
```

## Tracing

Enable request/response tracing in `logback.xml`: `<logger name="io.micronaut.http.client" level="TRACE"/>`. For per-client loggers set `micronaut.http.client.logger-name` (and `micronaut.http.services.<name>.logger-name`) and add matching `<logger>` entries.

## Checked

2026-11-08. Checked against the cited Micronaut 5.3.x guide .adoc source (raw file on GitHub) plus the Java doc-snippet sources the page includes via snippet:: (test-suite sources in micronaut-core 5.3.x), which hold the code shown. Pages were matched claim by claim (annotations, property names, class names, version gates, defaults) with a phrase checker over all pages and snippets, with targeted reads of the sections behind each unmatched item; pages were not all read line by line. Removed anything the pages did not state.

Method: documentation only; no commands were run.

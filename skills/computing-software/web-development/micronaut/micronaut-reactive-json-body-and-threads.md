---
id: computing-software.web-development.micronaut.micronaut-reactive-json-body-and-threads
name: micronaut-reactive-json-body-and-threads
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, reactive-server, json-binding, body-annotation, execute-on, reactive-responses, jackson]
level: practitioner
status: docs-checked
description: "Read JSON and raw request bodies non-blockingly in Micronaut, return reactive types, and offload blocking work with @ExecuteOn or subscribeOn."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/reactiveServer.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/reactiveServer/bodyAnnotation.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/reactiveServer/reactiveResponses.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/jsonBinding.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/jsonBinding/bindingUsingPOJOs.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/jsonBinding/bindingUsingReactiveFrameworks.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/jsonBinding/serializationUsingJacksonDatabind.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/jsonBinding/serializeUsingMicronautSerialization.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reactive bodies, JSON and the event loop

Goal: accept JSON/text bodies without blocking, and keep blocking I/O off the Netty event loop.

## Choose a JSON serializer

Controllers consume and produce JSON by default. Since 4.0 you must pick one: `micronaut-jackson-databind`, or Micronaut Serialization (`micronaut-serde-processor` as `annotationProcessor` plus `micronaut-serde-jackson`, group `io.micronaut.serde`). Both support Jackson annotations, and incoming JSON is read non-blockingly. With Jackson Databind and Kotlin data classes, native image needs `@ReflectiveAccess` on those classes.

## Read the body

```java
@Post
public HttpResponse<Person> save(@Body Person person) { ... }          // plain POJO

@Post @SingleResult
public Publisher<HttpResponse<Person>> save(@Body Publisher<Person> person) {
    ...   // the Publisher emits the POJO once the JSON has been read; return an HttpResponse
}

@Post
public CompletableFuture<HttpResponse<Person>> save(@Body CompletableFuture<Person> person) { ... }
```

A POJO method runs only once the data has been read, non-blockingly. The body argument of `@Body` can also be a reactive type or a `CompletableFuture`. For text, a `@Post` with the `text/plain` media type (default is `application/json`) and a `@Size`-constrained `@Body String` works (the page's example limits it to 1KB), but `@Size` does not limit what the server buffers; `micronaut.server.maxRequestSize` does (default maximum 10MB). For large data, accumulating a `String` in memory may strain the server; stream with `@Body Publisher<String>` and a collect step instead, and annotate a single-item result with `@SingleResult`. Body arguments of types that do not require conversion cause decoding of the request to be skipped.

## Reactive return types

Controllers may return `Publisher`, `Mono`, `CompletableFuture`, `HttpResponse<Publisher<String>>`, a `CharSequence` or a POJO (RxJava types too). Reactor `Flux`/`Mono` need the Micronaut Reactor dependency; RxJava types need the Micronaut RxJava dependency. A `Flux` response uses `Transfer-Encoding: chunked`; a single-result `Mono` populates `Content-Length`.

## Offload blocking work

Controllers run on the event loop thread, and reactive returns are subscribed there too, so move blocking I/O (JDBC, JPA) elsewhere. Configure the pool:

```yaml
micronaut:
  executors:
    io:
      type: fixed
      nThreads: 75
```

Then either annotate a controller/filter (type or method level) with `@ExecuteOn(TaskExecutors.IO)` (any named executor under `micronaut.executors` works), or use the reactive library:

```java
PersonController(@Named(TaskExecutors.IO) ExecutorService executorService, PersonService personService) {
    this.scheduler = Schedulers.fromExecutorService(executorService);
    ...
}
@Get @SingleResult
Publisher<Person> byName(String name) {
    return Mono.fromCallable(() -> personService.findByName(name)).subscribeOn(scheduler);
}
```

Kotlin `suspend` routes resume on the selected executor; an explicit `withContext` still wins. Under `micronaut.server.thread-selection` `AUTO`, `IO` or `BLOCKING`, a `suspend` route is offloaded; keep it on the event loop with `@NonBlocking`. For database work, configure a thread pool matching the maximum connections of the database connection pool.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against all eight cited pages: JSON default and the 4.0 serializer choice, both dependency sets, the Kotlin native-image warning, non-blocking reads, the `@Size` and `maxRequestSize` note (10MB), the response type table, chunked versus Content-Length, the executor YAML, `@ExecuteOn` scope, `subscribeOn` and the Kotlin suspend notes. Removed: route paths, `HttpResponse.created`, and `personService` lookups. The `subscribeOn` snippet is illustrative: the page confirms the injected I/O executor, `Mono::fromCallable` and `subscribeOn`, but its `Schedulers` call is in an unread source file.

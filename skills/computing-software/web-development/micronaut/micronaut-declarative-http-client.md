---
id: computing-software.web-development.micronaut.micronaut-declarative-http-client
name: micronaut-declarative-http-client
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, http-client, declarative-client, client-annotation, introduction-advice]
level: intro
status: docs-checked
description: "Define a Micronaut declarative HTTP client with @Client on an interface, choose a target URI and return type, and reuse a shared operations interface."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpClient/clientAnnotation.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: get a compile-time-implemented HTTP client by declaring an interface annotated with `@Client`.

## Steps

1. Put the HTTP annotations on a shared interface (they work on both server and client). `jakarta.validation` constraints are allowed; for them add the `micronaut-validation` module.

```java
@Validated
public interface PetOperations {
    @Post
    @SingleResult
    Publisher<Pet> save(@NotBlank String name, @Min(1L) int age);
}
```

2. The server side can implement the same interface with `@Controller("/pets")`.
3. Declare the client (the guide puts it in `src/test/java`):

```java
@Client("/pets")
public interface PetClient extends PetOperations {
    @Override
    @SingleResult
    Publisher<Pet> save(@NotBlank String name, @Min(1L) int age);
}
```

4. `@Inject` the client wherever it is needed.

`@Client` can be placed on any interface or abstract class; Introduction Advice implements the abstract methods at compile time.

## `@Client` value

- An absolute URI, e.g. `https://api.twitter.com/1.1`
- A relative URI: the target is the current server (useful for testing)
- A service identifier (Service Discovery); the usual production choice

## Return types

Anything convertible to a `Publisher` works (Reactor `Flux`/`Mono`, RxJava), including `Mono<HttpResponse<String>>` for the full response, plus `CompletableFuture<String>`. A plain type such as `String` or a POJO (`Book show()`) is also accepted, but any return type other than a reactive type or `CompletableFuture` results in a blocking request, which the guide does not recommend except for testing.

## Gotchas

- Overriding `save` in the client is required if you compile without `-parameters` (Java does not keep parameter names in bytecode); with `-parameters` it is not needed.
- When overriding, redeclare validation annotations: they are not `@Inherited`.
- `@Produces`/`@Consumes` mean different things on client and server: on a client `@Produces` describes how the method's *parameters* are formatted when sent; on a controller it describes the formatting of the *return value*.

## Checked
2026-11-07. Every claim, parameter, default, config key, class, method and code block was compared with the cited pages and their included snippets; nothing needed changing.

Method: documentation only; no commands were run.

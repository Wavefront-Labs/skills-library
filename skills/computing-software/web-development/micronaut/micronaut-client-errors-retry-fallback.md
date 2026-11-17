---
id: computing-software.web-development.micronaut.micronaut-client-errors-retry-fallback
name: micronaut-client-errors-retry-fallback
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, http-client, error-handling, retryable, fallback, recoverable]
level: practitioner
status: docs-checked
description: "Handle 400+ responses from Micronaut clients, bind error bodies to a POJO, and add @Retryable, @CircuitBreaker and @Fallback to a declarative client."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpClient/clientAnnotation/clientError.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpClient/lowLevelHttpClient/lowLevelClientError.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpClient/lowLevelHttpClient/bindErrors.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpClient/clientAnnotation/clientRetry.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpClient/clientAnnotation/clientFallback.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: decide how client failures surface and recover from them.

## Error model

A response with status 400 or higher creates an `HttpClientResponseException` that holds the original response.
- Reactive return types: the exception is passed through the publisher as an error.
- Blocking return types: the exception is thrown and the caller must catch it.

Exception, declarative client only: a 404 for a blocking return type is **not** an error and nothing is thrown (this includes `void`). An `HttpResponse` return gives the original response, `Optional` gives an empty optional, any other type gives `null`.

## Bind the error body to a POJO

Pass a success type and an error type to `exchange`:

```java
try {
    client.toBlocking().exchange(HttpRequest.GET("/books/1680502395"),
        Argument.of(Book.class),          // success type
        Argument.of(CustomError.class));  // error type
} catch (HttpClientResponseException e) {
    Optional<CustomError> err = e.getResponse().getBody(CustomError.class);
}
```

## Retry

Since Micronaut 4.0 declarative clients no longer invoke fallbacks by default. To restore that, add the `micronaut-retry` dependency and annotate each client with `@Recoverable`. Put `@Retryable` or `@CircuitBreaker` on the `@Client` interface:

```java
@Client("/pets")
@Retryable
public interface PetClient extends PetOperations { ... }
```

With `@Retryable`, all thrown exceptions are retried by default, including every 4xx except the declarative-client 404 case above. Filter responses that should not be retried with a `RetryPredicate`.

## Fallback

`@Fallback` marks a class used once all retries are exhausted. It is not strictly tied to retry: for any `@Recoverable` class, a failing call (or an emitted error for reactive types) triggers a search for a `@Fallback` class.

```java
@Fallback
public class PetFallback implements PetOperations {
    @Override
    @SingleResult
    public Publisher<Pet> save(String name, int age) {
        Pet pet = new Pet();
        pet.setAge(age);
        pet.setName(name);
        return Mono.just(pet);
    }
}
```

Tip from the guide: if fallbacks only support testing against external services, define them in `src/test/java` so they stay out of production code, and specify `@Recoverable(api = PetOperations.class)` on the declarative client when not using hystrix.

## Checked
2026-11-07. Every claim, parameter, default, config key, class, method and code block was compared with the cited pages and their included snippets; nothing needed changing.

Method: documentation only; no commands were run.

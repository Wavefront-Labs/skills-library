---
id: computing-software.web-development.micronaut.micronaut-client-request-binding
name: micronaut-client-request-binding
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, http-client, declarative-client, request-binding, query-value, client-argument-request-binder]
level: practitioner
status: docs-checked
description: "Control how declarative client method arguments become body, headers, query values and cookies, including Format styles and custom argument binders."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpClient/clientAnnotation/clientParameters.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpClient/clientAnnotation/clientHeaders.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: map declarative `@Client` method arguments onto the outgoing request.

## Default behaviour

A `@Post` method with parameters sends them as a JSON body by default (e.g. `{"name":"Dino", "age":10}`). `@Client` supports the same HTTP annotations as the server. Combine a URI template with `@Body`:

```java
@Post("/{name}")
Mono<Pet> save(
    @NotBlank String name,   // part of the URI
    @Body @Valid Pet pet)    // request body
```

## Parameter annotations

| Annotation | Purpose |
|---|---|
| `@Body` | body of the request |
| `@CookieValue` | sent as a cookie |
| `@Header` | sent as an HTTP header |
| `@QueryValue("userAge") Integer age` | customise the URI parameter name |
| `@PathVariable` | bind only from a path variable |
| `@RequestAttribute` | set as a request attribute |

Always use `@Produces`/`@Consumes` instead of supplying a `Content-Type` or `Accept` header.

## Type-bound parameters

`BasicAuth` sets `Authorization`; `HttpHeaders` adds many headers; `Cookies` / `Cookie` add cookies; `Locale` sets `Accept-Language` (annotate with `@QueryValue` or `@PathVariable` to fill a URI variable instead).

## Query formatting

`@Format` together with `@QueryValue` accepts `"csv"`, `"ssv"`, `"pipes"`, `"multi"`, `"deep-object"` (like the OpenAPI v3 `style`). It applies only to `Iterable`, `Map` or an `@Introspected` POJO. For `["Mike","Adam","Kate"]`: csv gives `param=Mike,Adam,Kate`; multi gives `param=Mike&param=Adam&param=Kate`; deep-object gives `param[0]=Mike&param[1]=Adam&param[2]=Kate`.

## Static headers via configuration

`@Header` is repeatable at type level and accepts placeholders:

```java
@Client("/pets")
@Header(name="X-Pet-Client", value="${pet.client.id}")
public interface PetClient extends PetOperations { ... }
```

Set `pet.client.id: foo` in `application.yml`, or supply a `PET_CLIENT_ID` environment variable. For dynamic headers use a client filter.

## Custom binders

Binder beans are picked up automatically; annotation binders are searched before type binders. Custom annotations must be annotated `@Bindable`.

- By argument annotation: implement `AnnotatedClientArgumentRequestBinder<Metadata>` with `getAnnotationType()` and `bind(context, uriContext, value, request)`; annotate it `@Singleton`; in `bind` call e.g. `request.header("X-Metadata-" + key, ...)`.
- By argument type: implement `TypedClientArgumentRequestBinder<Metadata>` (`argumentType()` returns `Argument.of(Metadata.class)`, plus `bind`).
- By method annotation (a `@Bindable` annotation with `@Target(METHOD)`): implement `AnnotatedClientRequestBinder<NameAuthorization>`; its `bind(MethodInvocationContext, ClientRequestUriContext, MutableHttpRequest)` can call `uriContext.addQueryParameter("name", ...)`.

Without a binder an unrecognised argument is converted to a string and appended as a query parameter.

## Checked
2026-11-07. Every claim, parameter, default, config key, class, method and code block was compared with the cited pages and their included snippets; nothing needed changing.

Method: documentation only; no commands were run.

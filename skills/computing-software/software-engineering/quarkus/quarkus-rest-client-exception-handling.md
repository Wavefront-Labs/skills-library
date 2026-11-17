---
id: computing-software.software-engineering.quarkus.quarkus-rest-client-exception-handling
name: quarkus-rest-client-exception-handling
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, rest-client, exception-handling, client-exception-mapper, microprofile, java]
level: advanced
status: docs-checked
description: "Handle error responses in Quarkus REST Client: ResponseExceptionMapper, @ClientExceptionMapper, @Blocking mappers for InputStream, and disabling the default mapper."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/rest-client.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Exception handling in the Quarkus REST Client

## Default behaviour

The MicroProfile REST Client spec mandates a default mapper that throws when the HTTP status is higher than 400. That is surprising if your client method returns `jakarta.ws.rs.core.Response` (or `org.jboss.resteasy.reactive.RestResponse`) so the caller can inspect the status. Disable it for a declarative client with its config key:

```properties
quarkus.rest-client.bar.disable-default-mapper=true
```

for a client declared `@RegisterRestClient(configKey = "bar")`. Programmatic clients: `QuarkusRestClientBuilder.disableDefaultMapper()`. The page's caution says `RestResponse` return types require disabling the default mapper, or a `WebApplicationException` is thrown for non-2xx statuses.

## Custom mappers

Implement `org.eclipse.microprofile.rest.client.ext.ResponseExceptionMapper<RuntimeException>`, with `toThrowable(Response)` returning an exception to throw, or `null` to pass to the next mapper in the chain. `getPriority` orders mappers; lower values run first.

Registration:

- Annotate the class with `@Provider` to apply to every client (unless `quarkus.rest-client.provider-autodiscovery` is `false`).
- Or `@RegisterProvider(MyResponseExceptionMapper.class)` on a specific client interface.
- Or the `providers` property of the proper `quarkus.rest-client` configuration group.

## Simpler: @ClientExceptionMapper

A static method on the client interface handles responses of 400 or above, for that client only:

```java
@ClientExceptionMapper
static RuntimeException toException(Response response) {
    if (response.getStatus() == 500) {
        return new RuntimeException("The remote service responded with HTTP 500");
    }
    return null;
}
```

The default priority applies unless you set the `priority` attribute. A `java.lang.reflect.Method` parameter may be added to learn which client method was invoked.

## Reading the body: @Blocking

Mappers run on the event loop by default. Reading an `InputStream` entity there (for a method returning `InputStream`) throws `BlockingNotAllowedException`. Add `@Blocking` (`io.smallrye.common.annotation.Blocking`) to the mapper class or to the `@ClientExceptionMapper` method so it runs on the worker pool, then `response.readEntity(String.class)` is allowed.

## Checked

2026-11-07. Matched against the text (with includes) of: rest-client.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.

---
id: computing-software.web-development.micronaut.micronaut-http-client-configuration
name: micronaut-http-client-configuration
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, http-client, configuration, per-client-config, event-loop, address-resolver, http-services]
level: practitioner
status: docs-checked
description: "Configure Micronaut HTTP clients globally or per service: read timeout, named config beans, custom DNS resolver, pools, event loop and Jackson settings."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpClient/lowLevelHttpClient/clientConfiguration.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpClient/clientAnnotation/clientJackson.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: tune HTTP client behaviour for all clients or one service.

## Global defaults

`DefaultHttpClientConfiguration` backs `micronaut.http.client.*`:

```yaml
micronaut:
  http:
    client:
      read-timeout: 5s
```

Netty beans are on by default: `netty.enabled=false` disables all Netty integration, `micronaut.http.client.netty.enabled=false` only the Netty client.

## Per service

```yaml
micronaut:
  http:
    services:
      foo:
        urls:
          - http://foo1
          - http://foo2
        read-timeout: 5s
```

Inject with `@Client("foo") @Inject ReactorHttpClient httpClient;`. When a config is used through `@Client`, all other attributes on the annotation are ignored except the service id.

Alternatively define a named bean extending `HttpClientConfiguration`:

```java
@Named("twitter")
@Singleton
class TwitterHttpClientConfiguration extends HttpClientConfiguration {
    public TwitterHttpClientConfiguration(ApplicationConfiguration configuration) { super(configuration); }
}
```

It is picked up by `@Client("twitter")` with service discovery, or by `@Client(value = "https://api.twitter.com/1.1", configuration = TwitterHttpClientConfiguration.class)` without it.

## Custom DNS resolver (Netty client)

Name an `AddressResolverGroup` bean and reference it with `address-resolver-group-name`:

```java
@Factory
class CustomAddressResolverGroupFactory {
    @Singleton
    @Named("custom")
    AddressResolverGroup<?> customAddressResolverGroup() { return DefaultAddressResolverGroup.INSTANCE; }
}
```

```
micronaut.http.services.foo.urls[0]=https://api.example.com
micronaut.http.services.foo.address-resolver-group-name=custom
```

The name must match an existing bean. When set, `dns-resolution-mode` is ignored.

## Event loop group

The default Netty `EventLoopGroup` is shared by workers and clients. Resize it with `micronaut.netty.event-loops.default.num-threads`, or define another (e.g. `other`) and select it for clients with `micronaut.http.client.event-loop-group: other`, useful for CPU-intensive client work.

## Jackson for clients

A default `ObjectMapper` is used; global settings such as `jackson.serialization.indentOutput: true` also affect the server. Client-specific settings: `@JacksonFeatures(enabledSerializationFeatures = WRAP_ROOT_VALUE, ...)` on the `@Client` interface. For anything else, write a `BeanCreatedEventListener` for the `ObjectMapper`. Prefer depending on `JsonMapper` for portability across JSON implementations.

## Checked

2026-11-08. Checked against the cited Micronaut 5.3.x guide .adoc source (raw file on GitHub) plus the Java doc-snippet sources the page includes via snippet:: (test-suite sources in micronaut-core 5.3.x), which hold the code shown. Pages were matched claim by claim (annotations, property names, class names, version gates, defaults) with a phrase checker over all pages and snippets, with targeted reads of the sections behind each unmatched item; pages were not all read line by line. Removed anything the pages did not state.

Method: documentation only; no commands were run.

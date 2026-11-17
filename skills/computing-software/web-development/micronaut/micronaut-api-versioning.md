---
id: computing-software.web-development.micronaut.micronaut-api-versioning
name: micronaut-api-versioning
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, api-versioning, version-annotation, default-version, versioned-client, request-version-resolver]
level: practitioner
status: docs-checked
description: "Version Micronaut routes with @Version, enable header or parameter resolution, set a default version, and version declarative client requests."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/apiVersioning.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# API versioning

Goal: serve several versions of the same route and call versioned endpoints.

## Version routes

```java
@Controller("/versioned")
class VersionedController {
    @Version("1")
    @Get("/hello")
    String helloV1() { return "helloV1"; }

    @Version("2")
    @Get("/hello")
    String helloV2() { return "helloV2"; }
}
```

Enable versioning:

```yaml
micronaut:
  router:
    versioning:
      enabled: true
```

By default the version comes from the `X-API-VERSION` header or the `api-version` request parameter. Configure both:

```yaml
micronaut:
  router:
    versioning:
      enabled: true
      parameter:
        enabled: false
        names: 'v,api-version'
      header:
        enabled: true
        names:
          - 'X-API-VERSION'
          - 'Accept-Version'
```

`parameter.names` is a comma-separated list; `header.names` is a list. For another strategy implement `RequestVersionResolver`, which receives the `HttpRequest`.

## Default version

```yaml
micronaut:
  router:
    versioning:
      enabled: true
      default-version: 3
```

A route is not matched when all hold: a default version is configured, the request carries no version, the route defines a version, and that version differs from the default. If the request specifies a version, the default has no effect.

## Versioned client requests

`@Version` also works on declarative clients, at type level or per method (method wins for that method). By default the value is sent in the `X-API-VERSION` header:

```java
@Client("/hello")
@Version("1")
public interface HelloClient {
    @Get("/greeting/{name}")
    String sayHello(String name);

    @Version("2")
    @Get("/greeting/{name}")
    @SingleResult
    Publisher<String> sayHelloTwo(String name);
}
```

Change the header name(s) under `micronaut.http.client.versioning.<key>.headers`, where `default` is the default configuration and a client-specific key is the value passed to `@Client` (e.g. `greeting-service` for `@Client('greeting-service')`):

```yaml
micronaut:
  http:
    client:
      versioning:
        default:
          headers:
            - 'Accept-Version'
            - 'X-API-VERSION'
```

Defaults are governed by `DefaultClientVersioningConfiguration`.

## Checked
2026-11-07. Every claim, parameter, default, config key, class, method and code block was compared with the cited pages and their included snippets; nothing needed changing.

Method: documentation only; no commands were run.

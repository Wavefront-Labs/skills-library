---
id: computing-software.web-development.micronaut.micronaut-custom-endpoint
name: micronaut-custom-endpoint
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, custom-endpoint, management, endpoint-annotation, read-write-delete, sensitive, endpoints]
level: practitioner
status: docs-checked
description: "Build a custom Micronaut management endpoint with @Endpoint, @Read, @Write, @Delete and @Sensitive, then configure its enablement, sensitivity and base path."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/management/buildingEndpoints.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/management/buildingEndpoints/endpointAnnotation.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/management/buildingEndpoints/endpointMethod.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/management/buildingEndpoints/endpointSensitivity.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/management/buildingEndpoints/endpointConfiguration.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Build a custom management endpoint

Goal: expose your own application data over HTTP using the same mechanism as the built-in endpoints (the `management` dependency provides it).

## Declare the endpoint

Annotate a class with `@Endpoint`. A single String argument is the endpoint id. Named arguments:

| Argument | Meaning |
|---|---|
| `id` | endpoint id/name |
| `prefix` | prefix used when configuring the endpoint (default `endpoints`) |
| `defaultEnabled` | enabled when no configuration is set |
| `defaultSensitive` | sensitive when no configuration is set |

```java
@Endpoint(id = "date",
          prefix = "custom",
          defaultEnabled = true,
          defaultSensitive = false)
public class CurrentDateEndpoint {
```

## Map HTTP methods

Public methods respond to GET (`@Read`), POST (`@Write`) and DELETE (`@Delete`).

```java
@Read
public Date currentDate() { return currentDate; }

@Read(produces = MediaType.TEXT_PLAIN)
public String currentDatePrefix(@Selector String prefix) {
    return prefix + ": " + currentDate;
}

@Write
public String reset() { currentDate = new Date(); return "Current date reset"; }
```

- `@Read` takes an optional `produces` media type (default `application/json`); `@Selector` binds the extra path segment (`GET /date/the_date_is`).
- `@Write` takes an optional `consumes` (default `application/json`):

```java
@Write(consumes = MediaType.APPLICATION_FORM_URLENCODED, produces = MediaType.TEXT_PLAIN)
public String updateMessage(String newMessage) { ... return "Message updated"; }

@Delete
public String deleteMessage() { ... return "Message deleted"; }
```

```bash
curl -X POST http://localhost:65013/message -H 'Content-Type: application/x-www-form-urlencoded' -d $'newMessage=A new message'
curl -X DELETE http://localhost:65013/message
```

## Per-method sensitivity

`@Sensitive` on a method overrides the endpoint-wide setting:

```java
@Endpoint(id = "alerts", defaultSensitive = false)
public class AlertsEndpoint {
    @Delete @Sensitive(true)                       // always sensitive
    void clearAlerts() { alerts.clear(); }

    @Write(consumes = MediaType.TEXT_PLAIN)
    @Sensitive(property = "add.sensitive", defaultValue = true)
    void addAlert(@Body String alert) { alerts.add(alert); }
}
```

The key is built as prefix + id + `property`, so `endpoints.alerts.add.sensitive` decides `addAlert`; if unset, `defaultValue` applies (it defaults to `true`).

## Configure

```yaml
endpoints:
  <any endpoint id>:
    enabled: Boolean
    sensitive: Boolean
```

- Endpoint `foo` is configured under `endpoints.foo`; `endpoints.all.*` supplies defaults, and a specific `endpoints.foo.enabled=true` beats `endpoints.all.enabled=false`.
- The base path is `/` by default. Set `endpoints.all.path` (e.g. `/endpoints/`) to move all endpoints; the leading and trailing `/` are required unless `micronaut.server.context-path` is set, in which case the leading `/` is not needed.

## Checked
2026-11-07. Every claim, parameter, default, config key, class, method and code block was compared with the cited pages and their included snippets; nothing needed changing.

Method: documentation only; no commands were run.

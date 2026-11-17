---
id: computing-software.web-development.micronaut.micronaut-cors-configuration
name: micronaut-cors-configuration
category: computing-software
field: web-development
product: micronaut
tags: [micronaut, cors, cross-origin, allowed-origins, coep, corp, security-headers]
level: practitioner
status: docs-checked
description: "Enable and tune CORS in a Micronaut server with micronaut.server.cors configurations, the @CrossOrigin annotation, and the COEP and CORP response headers."
sources:
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/serverConfiguration/cors.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/serverConfiguration/cors/corsConfiguration.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/serverConfiguration/cors/corsAllowedOrigins.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/serverConfiguration/cors/annotationBasedCors.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/serverConfiguration/corsCrossOriginEmbedderPolicy.adoc
  - https://github.com/micronaut-projects/micronaut-core/blob/5.3.x/src/main/docs/guide/httpServer/serverConfiguration/corsCrossOriginResourcePolicy.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Micronaut CORS configuration

Goal: allow browser cross-origin requests to a Micronaut server. By default CORS requests are rejected.

## Enable
```yaml
micronaut:
  server:
    cors:
      enabled: true
```
Enabling alone is "wide open": any origin is allowed. Providing any entry under `configurations` replaces that default. Configuration names (`all`, `web`, `mobile`) are only labels; a request origin is matched against each configuration's allowed origins (exactly or by regex).

```yaml
micronaut:
  server:
    cors:
      enabled: true
      configurations:
        web:
          allowed-origins:
            - http://foo.com
          allowed-origins-regex: '^http(|s):\/\/www\.google\.com$'
          allowed-methods: [POST, PUT]
          allowed-headers: [Content-Type, Authorization]
          exposed-headers: [Content-Type, Authorization]
          allow-credentials: true
          allow-private-network: false
          max-age: 3600
```

## Per-option facts from the docs
- Omit `allowed-origins` and `allowed-origins-regex` to allow any origin for that configuration. Several origins go in `allowed-origins` as a list.
- The regex goes through `Pattern.compile` and `Matcher#matches`. If you set the regex but not `allowed-origins`, origins default to none, not any. Use regexes carefully: attackers can register domains matching a loose pattern.
- Values left unset take the defaults of the matching `CorsOriginConfiguration` fields; check that class's API page for them.

## Per-route: @CrossOrigin
`@CrossOrigin` on a controller or method applies CORS to just those endpoints and maps one-to-one to the configuration properties; `@CrossOrigin("https://foo.com")` sets only the origin. Unset attributes use the same defaults.

```java
@Controller("/hello")
public class CorsController {
    @CrossOrigin("https://myui.com")
    @Get(produces = MediaType.TEXT_PLAIN)
    public String cors() { return "Welcome to the worlds of CORS"; }

    @Produces(MediaType.TEXT_PLAIN)
    @Get("/nocors")      // https://myui.com is not allowed here
    public String nocorstoday() { return "No more CORS for you"; }
}
```

## Cross-origin isolation headers
CORS does not need to be enabled for these:
```yaml
micronaut:
  server:
    cors:
      cross-origin-embedder-policy: require-corp   # unsafe-none | require-corp | credentialless
      cross-origin-resource-policy: same-origin    # same-origin | same-site | cross-origin
```

## Checked
2026-11-07. Checked against the CORS pages. Removed default values for credentials, private network, max-age, exposed headers, methods and headers, and the single-header option, because the cited pages do not state them.

Method: documentation only; no commands were run.

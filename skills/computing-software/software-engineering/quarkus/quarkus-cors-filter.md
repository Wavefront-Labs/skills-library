---
id: computing-software.software-engineering.quarkus.quarkus-cors-filter
name: quarkus-cors-filter
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, cors, http, security, origin, headers]
level: intro
status: docs-checked
description: "Enable and configure the Quarkus CORS filter: allowed origins (incl. regex), methods, headers, programmatic HttpSecurity setup, dev-mode wildcard and debugging 403 rejections."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/security-cors.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quarkus CORS filter

Extension: `io.quarkus:quarkus-vertx-http`. The filter intercepts all HTTP requests, adds CORS headers, answers preflight requests immediately, and rejects non-compliant regular CORS requests with HTTP 403.

## Enable and configure

```properties
quarkus.http.cors.enabled=true
quarkus.http.cors.origins=http://example.com,http://www.example.io,/https://([a-z0-9\\-_]+)\\\\.app\\\\.mydomain\\\\.com/
quarkus.http.cors.methods=GET,PUT,POST
quarkus.http.cors.headers=X-Custom
quarkus.http.cors.exposed-headers=Content-Disposition
quarkus.http.cors.access-control-max-age=24H
quarkus.http.cors.access-control-allow-credentials=true
```

- If `origins` is not set, CORS is not permitted and only same-origin requests work.
- Regular expressions go between slashes. In `application.properties` escape special characters with four backslashes: `\\\\.` matches a literal dot, `\\.` matches any character. Wrong escaping can create security holes, so verify before deploying.

## Accepting all origins

`quarkus.http.cors.origins=*` in production is a severe risk. The only acceptable case is a read-only public API with no side effects (no cookies, no data written); there `quarkus.http.cors.return-exact-origins=false` returns a literal `*` and avoids the `Vary: Origin` header, improving HTTP caching. For development only:

```properties
quarkus.http.cors.enabled=true
%dev.quarkus.http.cors.origins=/.*/
```

## Programmatic setup

Use either properties or code, not both. Observe the `io.quarkus.vertx.http.security.HttpSecurity` CDI event:

```java
void configure(@Observes HttpSecurity httpSecurity) {
    httpSecurity.cors(CORS.builder()
            .origin("https://example.com")
            .method("POST")
            .build());
}
```

`httpSecurity.cors("https://example.com")` is the short form (`io.quarkus.vertx.http.security.CORS` is the builder).

## CSRF side effect

The filter also helps prevent CSRF through Origin verification, but first confirm browsers actually send an `Origin` header for your cross-origin requests, especially HTML forms.

## Debugging rejections

A rejected request gets 403 with a status message starting `CORS Rejected`, without saying why. Enable the reason in logs:

```properties
quarkus.log.category."io.quarkus.vertx.http.runtime.cors.CORSFilter".level=DEBUG
```

Compare the logged origin, method and headers with `quarkus.http.cors.origins`, `methods` and `headers`; browser dev tools also report the failed check.

## Checked

2026-11-07. Read in full: security-cors.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.

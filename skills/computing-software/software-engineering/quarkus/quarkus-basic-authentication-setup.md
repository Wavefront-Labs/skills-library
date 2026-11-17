---
id: computing-software.software-engineering.quarkus.quarkus-basic-authentication-setup
name: quarkus-basic-authentication-setup
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, basic-authentication, http-security, httpsecurity, authorization-header, realm]
level: intro
status: docs-checked
description: "Understand Quarkus built-in HTTP Basic authentication, its limitations, and enable it programmatically with the HttpSecurity CDI event."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/security-basic-authentication.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quarkus Basic authentication: concepts and programmatic setup

Quarkus ships a built-in Basic authentication mechanism. It relies only on HTTP headers: no cookies, session identifiers or login pages.

## How it works

The client sends `Authorization: Basic <credentials>` on every request, where credentials are the Base64 encoding of `user:password`. Example: user `Alice` with password `secret` gives `Authorization: Basic QWxpY2U6c2VjcmV0`.

Base64 is encoding only, not encryption or hashing, so Basic gives no confidentiality. Use it with HTTPS.

## Limitations to weigh before choosing it

- Credentials travel as plain text. The risk grows when a load balancer terminates HTTPS and forwards to Quarkus over HTTP, and in multi-hop setups where HTTPS covers only client to first endpoint and credentials are propagated onward over HTTP.
- Credentials are sent with every request, increasing exposure.
- The application must manage usernames, passwords and roles securely, which adds complexity. Mechanisms that delegate this to specialised services may be safer.

## Enable programmatically

Observe the `io.quarkus.vertx.http.security.HttpSecurity` CDI event and call `basic(...)` with a realm name:

```java
package org.acme.http.security;

import io.quarkus.vertx.http.security.HttpSecurity;
import jakarta.enterprise.event.Observes;

public class HttpSecurityConfiguration {

    void configure(@Observes HttpSecurity httpSecurity) {
        httpSecurity.basic("QuarkusTestRealm");
    }
}
```

This enables Basic authentication with the `QuarkusTestRealm` realm.

## Gotchas

- If you generate an OpenAPI schema document with the SmallRye OpenAPI extension, Basic authentication must be enabled at build time with the `quarkus.http.auth.basic` configuration property.
- Role-based access control on top of Basic uses the standard `@RolesAllowed`, `@DenyAll` and `@PermitAll` annotations on REST endpoints and CDI beans.
- The page's metadata lists the extensions `quarkus-vertx-http`, `quarkus-elytron-security-jdbc`, `quarkus-elytron-security-ldap` and `quarkus-security-jpa-reactive`.

## Checked

2026-11-07. Read in full: security-basic-authentication.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: an inference about the extensions serving as a credential store; the line now only lists the extensions in the page metadata.

Method: documentation only; no commands were run.

---
id: computing-software.software-engineering.quarkus.quarkus-http-permission-path-matching
name: quarkus-http-permission-path-matching
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, http-permissions, authorization, path-matching, role-policy, httpsecurity, securityidentity]
level: practitioner
status: docs-checked
description: "Write Quarkus quarkus.http.auth.permission and policy rules: built-in policies, wildcard and longest-path matching, shared checks, role mapping, programmatic setup."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/security-authorize-web-endpoints-reference.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quarkus HTTP authorization by configuration

## Built-in policies

`deny` (nobody), `permit` (everybody), `authenticated` (authenticated users). Define role policies with `quarkus.http.auth.policy.<name>.roles-allowed=user,admin`. Bind them via permission sets:

```properties
quarkus.http.auth.permission.permit1.paths=/public/*
quarkus.http.auth.permission.permit1.policy=permit
quarkus.http.auth.permission.permit1.methods=GET
quarkus.http.auth.permission.deny1.paths=/forbidden
quarkus.http.auth.permission.deny1.policy=deny
quarkus.http.auth.permission.roles1.paths=/roles-secured/*,/other/*,/api/*
quarkus.http.auth.permission.roles1.policy=role-policy1
```

Listing only `GET` means other methods on that path are rejected. An exact path such as `/forbidden` also secures `/forbidden/`; to permit the slash form add a more specific exact permission for `/forbidden/`.

## Matching rules

- Trailing `*` matches zero or more segments but not a word continuing the prefix: `/public*` does not match `/public-info`. A `*` elsewhere matches exactly one segment, enclosed by slashes (`/api/*/detail`).
- Longest path wins; less specific sets are ignored once a more specific one matches. Among wildcard patterns, the longest sub-path leading to the `*` wins.
- For the same path, a permission with an explicit matching method beats one without methods.
- If several permissions win at once, all must allow access (for example both `user` and `admin` roles).
- Paths must not contain a semicolon. For matrix-parameter decisions use a custom `HttpSecurityPolicy`.
- Test every path; overlapping or multi-wildcard expressions are easy to get wrong. For JAX-RS prefer annotations plus `quarkus.security.jaxrs.deny-unannotated-endpoints` or `quarkus.security.jaxrs.default-roles-allowed`.

## Other options

- `quarkus.http.auth.permission.<name>.enabled=false` disables a set; re-enable at runtime with `-Dquarkus.http.auth.permission.permit1.enabled=true`.
- Paths not starting with `/` get `quarkus.http.root-path` prepended; a leading slash makes the path used as-is.
- Role mapping per policy: `quarkus.http.auth.policy.admin-policy1.roles.admin=Admin1`. Global mapping, no path securing: `quarkus.http.auth.roles-mapping.admin=Admin1`. Programmatic: `httpSecurity.rolesMapping("admin", "Admin1")`.
- Shared checks: `quarkus.http.auth.permission.custom1.shared=true` always applies in addition to the single most specific unshared match, and shared checks run before unshared ones. Many shared checks are less efficient.

## Programmatic equivalent

```java
void configure(@Observes HttpSecurity httpSecurity) {
    httpSecurity
        .get("/public/*").permit()
        .path("/roles-secured/*", "/other/*", "/api/*").roles("admin", "user")
        .path("/forbidden").authorization().deny();
}
```

## Custom policy

Create an `@ApplicationScoped` bean implementing `io.quarkus.vertx.http.runtime.security.HttpSecurityPolicy` (`checkPermission` returning `CheckResult.permit()` or `deny()`, and `name()`). Reference it with `quarkus.http.auth.permission.custom1.policy=custom`, or bind it with `@AuthorizationPolicy(name = "custom")`. A policy with no `name()` is global. To inject request-scoped beans such as `UriInfo`, apply the policy to Jakarta REST endpoints via `@AuthorizationPolicy` or `applies-to=jaxrs`.

## Checked

2026-11-07. Read in full: security-authorize-web-endpoints-reference.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.

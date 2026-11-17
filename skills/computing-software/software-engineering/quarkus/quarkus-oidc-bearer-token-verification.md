---
id: computing-software.software-engineering.quarkus.quarkus-oidc-bearer-token-verification
name: quarkus-oidc-bearer-token-verification
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, oidc, bearer-token, jwt, introspection, jwk, issuer]
level: practitioner
status: docs-checked
description: "Configure how Quarkus OIDC verifies bearer tokens: local JWK checks, forced introspection, issuer and audience claims, discovery-off endpoint paths, and introspection caching."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/security-oidc-bearer-token-authentication.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quarkus OIDC bearer token verification

Use this when a Quarkus `service` application (extension `quarkus-oidc`) must accept bearer access tokens from an OIDC provider such as Keycloak and you need to control how they are verified.

## Default verification

- A JWT is verified with a JWK from a local `JsonWebKeySet` fetched from the provider's JWK endpoint, matched by the token `kid` header.
- If no key matches, the key set is refreshed, but only once per `quarkus.oidc.token.forced-jwk-refresh-interval` (default 10 minutes).
- If there is still no match, the JWT is sent to the provider's introspection endpoint.
- Opaque tokens (binary or encrypted JWT) are always introspected.

## Tune introspection

Only JWTs and a key always available: disable fallback introspection.

```properties
quarkus.oidc.token.allow-jwt-introspection=false
quarkus.oidc.token.allow-opaque-token-introspection=false
```

Force JWTs to be introspected remotely, either by configuring only an introspection path:

```properties
quarkus.oidc.auth-server-url=http://localhost:8180/realms/quarkus
quarkus.oidc.discovery-enabled=false
quarkus.oidc.introspection-path=/protocol/openid-connect/tokens/introspect
```

or by keeping discovery and requiring introspection only:

```properties
quarkus.oidc.auth-server-url=http://localhost:8180/realms/quarkus
quarkus.oidc.token.require-jwt-introspection-only=true
```

The first saves the discovery call and the unused key fetch but needs the endpoint address configured manually; the second is simpler but still does a discovery call. Introspected data is available as `io.quarkus.oidc.TokenIntrospection` (injectable, or the `SecurityIdentity` `introspection` attribute).

## Discovery off: explicit paths

Discovery uses `/.well-known/openid-configuration` under `quarkus.oidc.auth-server-url`. If unavailable, set `quarkus.oidc.discovery-enabled=false` and relative `quarkus.oidc.token-path`, `quarkus.oidc.jwks-path`, `quarkus.oidc.user-info-path`, `quarkus.oidc.introspection-path`.

## Claims

- After the signature and `exp` check, `iss` is compared to the discovered `issuer`, or to `quarkus.oidc.token.issuer` if set.
- If the issuer cannot match (internal vs external host, tenant template), `quarkus.oidc.token.issuer=any` skips the check. Use it last. With Keycloak, prefer starting it with `KEYCLOAK_FRONTEND_URL`.
- Verify audience with `quarkus.oidc.token.audience` (for example `${quarkus.oidc.client-id}`).
- `quarkus.oidc.client-id` is required when tokens are introspected remotely (always for opaque tokens). Do not set a client secret if no remote OIDC call is needed.

## Cache introspection and UserInfo

Opaque token plus `UserInfo` means two remote calls per request. Enable the default in-memory cache:

```properties
quarkus.oidc.token-cache.max-size=1000
quarkus.oidc.token-cache.time-to-live=3M
quarkus.oidc.token-cache.clean-up-timer-interval=1M
```

`max-size` is 0 by default, so the cache is off until set. Per tenant, `allow-token-introspection-cache` and `allow-user-info-cache` can deny storing. A custom `@ApplicationScoped` `@Alternative` `@Priority(1)` bean can implement `TokenIntrospectionCache` and `UserInfoCache`.

For deeper checks, register a Jose4j `Validator` `@ApplicationScoped` `@Unremovable` bean (all tenants), or bind it with `@TenantFeature`.

## Checked

2026-11-07. Matched against the text (with includes) of: security-oidc-bearer-token-authentication.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.

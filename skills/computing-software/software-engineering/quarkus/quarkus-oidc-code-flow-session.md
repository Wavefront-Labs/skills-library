---
id: computing-software.software-engineering.quarkus.quarkus-oidc-code-flow-session
name: quarkus-oidc-code-flow-session
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, oidc, authorization-code-flow, session, cookies, token-state-manager, refresh-token]
level: advanced
status: docs-checked
description: "Manage the Quarkus OIDC web-app session: state and session cookies, TokenStateManager strategies and encryption, ID token refresh, session age and session-expired page."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/security-oidc-code-flow-authentication.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quarkus OIDC code flow session lifetime

For a `quarkus.oidc.application-type=web-app` application, Quarkus OIDC keeps session, code flow and post-logout state in cookies.

## Cookies

- `quarkus.oidc.authentication.cookie-path` (default `/`) keeps the cookie visible across protected paths with different roots.
- `quarkus.oidc.authentication.cookie-path-header` (for example `X-Forwarded-Prefix`) sets the path dynamically; if the header is absent, `cookie-path` is used.
- `quarkus.oidc.authentication.cookie-domain` (for example `company.net`) when services span several subdomains.
- State cookies: a state cookie and matching `state` query parameter are created at redirect; default age 5 minutes via `quarkus.oidc.authentication.state-cookie-age`. Names are unique per flow to support multiple tabs; `quarkus.oidc.authentication.allow-multiple-code-flows=false` disables this.

## Session cookie and TokenStateManager

The default `io.quarkus.oidc.TokenStateManager` stores ID, access and refresh tokens in an encrypted session cookie, keeping the endpoint stateless. Narrow what is kept with `quarkus.oidc.token-state-manager.strategy`: `id-refresh-tokens` (ID and refresh only) or `id-token` (ID only). Keep the access token if you need `UserInfo`, downstream calls, or roles from it.

If the cookie exceeds 4KB (browser limits), set `quarkus.oidc.token-state-manager.split-tokens=true`, or store tokens in a database/Redis (`quarkus-oidc-db-token-state-manager`, `quarkus-oidc-redis-token-state-manager`).

```properties
quarkus.oidc.application-type=web-app
quarkus.oidc.token-state-manager.split-tokens=true
quarkus.oidc.token-state-manager.encryption-secret=<32+ character secret>
```

The secret must be at least 32 characters. Without it, `quarkus.oidc.credentials.secret` or `credentials.jwt.secret` is hashed. Set it explicitly for mTLS or `private_key_jwt` client authentication; otherwise a random key is generated, which breaks multi-pod deployments. `encryption-required=false` disables encryption.

A custom `@ApplicationScoped @Alternative @Priority(1)` `TokenStateManager` may implement `createTokenState`, `getTokens`, `deleteTokens`. If external storage lost the tokens, `getTokens` must return `null` or throw `AuthenticationFailedException`; both remove the cookie and redirect to re-authenticate.

## Refresh and session age

- By default logout follows ID token expiry; the user is redirected to the provider, and re-authenticated silently if the provider session is active.
- `quarkus.oidc.token.refresh-expired=true` refreshes ID, access and refresh tokens using the refresh token.
- Session age = ID token lifespan + `quarkus.oidc.authentication.session-age-extension` + `quarkus.oidc.token.lifespan-grace`. Keep it longer than the ID token and close to the refresh token lifespan. Use `session-age-extension` for real extensions; `lifespan-grace` only for clock skew.
- `quarkus.oidc.token.refresh-token-time-skew` refreshes proactively before expiry (set below the ID token lifespan).
- Concurrent requests with a provider that limits refresh token reuse: set `quarkus.oidc.token.refresh-token-cache-time-to-live` (for example `5S`) only if needed.
- `quarkus.oidc.authentication.session-expired-page=/session-expired-page` sends users to a public page first.

The session cannot be extended indefinitely: once the refresh token expires the user must re-authenticate.

## Checked

2026-11-07. Matched against the text (with includes) of: security-oidc-code-flow-authentication.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.

---
id: computing-software.software-engineering.quarkus.quarkus-oidc-logout
name: quarkus-oidc-logout
category: computing-software
field: software-engineering
product: quarkus
tags: [quarkus, oidc, logout, back-channel-logout, session, authorization-code-flow, auth0]
level: practitioner
status: docs-checked
description: "Configure Quarkus OIDC logout: RP-initiated, back-channel, front-channel and local logout with OidcSession, post-logout redirect, Auth0 workaround, Clear-Site-Data."
sources:
  - https://github.com/quarkusio/quarkus/blob/main/docs/src/main/asciidoc/security-oidc-code-flow-authentication.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quarkus OIDC logout options

All for `quarkus.oidc.application-type=web-app`. Optionally send `Clear-Site-Data` on every logout: `quarkus.oidc.logout.clear-site-data=cache,cookies`.

## User-initiated (RP-initiated) logout

```properties
quarkus.oidc.logout.path=/logout
quarkus.oidc.logout.post-logout-path=/welcome.html

quarkus.http.auth.permission.authenticated.paths=/logout
quarkus.http.auth.permission.authenticated.policy=authenticated
quarkus.http.auth.permission.public.paths=/welcome.html
quarkus.http.auth.permission.public.policy=permit
```

A request to the logout path (relative to the endpoint, for example `https://application.com/webapp/logout`) redirects the user to the provider, then back to the post-logout path. That URI must be registered as a valid `post_logout_redirect_uri` at the provider. When `post-logout-path` is set, a `q_post_logout` cookie (suffixed with the tenant id in multi-tenant setups, for example `q_post_logout_tenant_1`) and a matching `state` parameter are used; verify they match, for example in a Jakarta REST filter. Consider setting `quarkus.oidc.authentication.cookie-path` to a path common to all resources.

## Providers without end_session_endpoint (Auth0)

```properties
quarkus.oidc.end-session-path=v2/logout
quarkus.oidc.logout.post-logout-uri-param=returnTo
quarkus.oidc.logout.extra-params.client_id=${quarkus.oidc.client-id}
```

`end-session-path` can also override a discovered global logout URL with an application-specific one.

## Back-channel and front-channel

```properties
quarkus.oidc.logout.backchannel.path=/back-channel-logout
quarkus.oidc.logout.frontchannel.path=/front-channel-logout
```

Register the absolute back-channel URL in the provider's admin console. If the provider sets no expiry claim in the logout token, configure `quarkus.oidc.token.age=10S` so verification can succeed. The front-channel path is compared to the request path (rarely used).

## Local logout

Logout from the provider may be unwanted (for example Google SSO). Inject `io.quarkus.oidc.OidcSession` and call `oidcSession.logout().await().indefinitely()` to clear only the local session cookie. `OidcSession` also gives the tenant id and session expiry.

## Revoking tokens

Inject `OidcProviderClient`, `AccessTokenCredential`, `RefreshToken`; chain `oidcSession.logout()` with `revokeAccessToken(...)` and `revokeRefreshToken(...)`. Alternatively revoke in an `@ObservesAsync SecurityEvent` listener when the type is `SecurityEvent.Type.OIDC_LOGOUT_RP_INITIATED`.

## Checked

2026-11-07. Matched against the text (with includes) of: security-oidc-code-flow-authentication.adoc. Each command, config key, class, method and default stated above was matched to page text or an embedded example. Removed or reworded: nothing; no claim failed the check.

Method: documentation only; no commands were run.

---
id: computing-software.cybersecurity-defensive.pomerium.front-channel-single-sign-out
name: front-channel-single-sign-out
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [front-channel-logout, sign-out, csrf-token, well-known-pomerium, single-sign-out]
level: advanced
status: docs-checked
description: "Configure OIDC Front-Channel Logout with Pomerium, check IdP support, register the logout URI and sign out through the route, not the authenticate URL."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/capabilities/authentication.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Pomerium follows OpenID Connect Front-Channel Logout 1.0.

1. Check IdP support: its `/.well-known/openid-configuration` must show `frontchannel_logout_session_supported` as `true`.
2. Register a `frontchannel_logout_uri` containing `/.pomerium/sign_out`, matching the external route, e.g. `app.corp.example.com/.pomerium/sign_out`.

Flow when correct:
1. The proxy gets the sign-out request and clears the local Pomerium session.
2. It redirects to the authenticate service's `/.pomerium/sign_out`.
3. The authenticate service clears the remote application session.

Signing out through the authenticate service URL is not recommended: it does not delete the session cookie on the route itself. Point sign-out requests at the external route.

Pomerium's `/.well-known/pomerium` endpoint exposes `authentication_callback_endpoint`, `jwks_uri` and `frontchannel_logout_uri`. The sign-out endpoint accepts GET and POST but needs a CSRF token, taken from the `X-CSRF-Token` response header of the well-known endpoint or the `_pomerium_csrf` cookie.

From JavaScript, build the page origin plus `/.pomerium/sign_out` and add `pomerium_redirect_uri` (URL-encoded) for the post-logout page.

## Checked

2026-11-04. Confirmed against the Authentication page: Front-Channel Logout 1.0, frontchannel_logout_session_supported, frontchannel_logout_uri, three-step flow, well-known endpoint fields, CSRF token sources, JavaScript sign-out example. Softened an absolute prohibition to the page's not recommended.

Method: documentation only; no commands were run.

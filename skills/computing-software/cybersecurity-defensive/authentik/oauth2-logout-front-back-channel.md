---
id: computing-software.cybersecurity-defensive.authentik.oauth2-logout-front-back-channel
name: oauth2-logout-front-back-channel
category: computing-software
field: cybersecurity-defensive
product: authentik
tags: [authentik, backchannel-logout, frontchannel-logout, oidc, single-logout, logout-uri]
level: advanced
status: docs-checked
description: "Configure OIDC front-channel and back-channel logout on an authentik OAuth2 provider: Logout URI, method, logout token claims, triggers and limits."
sources:
  - https://docs.goauthentik.io/add-secure-apps/providers/oauth2/frontchannel_and_backchannel_logout/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: have authentik notify relying parties when a user session ends. The RP must support OIDC front-channel or back-channel logout, be reachable from authentik, use HTTPS in production, and expose a logout endpoint. (Marked as preview, introduced in 2025.8.)

## Configure
**Applications > Providers**, edit the OAuth2 provider, set **Logout URI** (a single URL, e.g. `https://app.example.com/oauth/backchannel-logout`) and **Logout Method** (**Front-channel** or **Back-channel**), then **Finish**.

## Back-channel
authentik POSTs `logout_token=<signed JWT>` (form encoded) server to server. Claims: `iss`, `sub`, `aud` (client ID), `iat`, `jti`, `events`, and `sid` when available. It fires when the user logs out via a logout flow, an admin deletes the session, the account is deactivated, or the session expires or is revoked. It is the only method that works for administrative termination.

## Front-channel
authentik injects an iframe logout stage into the logout flow that loads the RP's URL with query parameters `iss` and `sid`, for example `https://app.example.com/oauth/logout?iss=https://authentik.company&sid=session_id`. The user then continues the logout flow. It only works for user-initiated logouts through a logout flow because it needs a browser session.

## RP-initiated logout
Redirecting to the `end_session` endpoint ends only that application's session by default. For full Single Logout choose the provider's logout behavior in the Single Logout settings.

## Checked
2026-11-03. Every remaining option, endpoint, value and example was read against the authentik documentation page https://docs.goauthentik.io/add-secure-apps/providers/oauth2/frontchannel_and_backchannel_logout/.
Nothing was removed.
Method: documentation only; no commands were run.

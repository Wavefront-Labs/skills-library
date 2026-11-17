---
id: computing-software.cybersecurity-defensive.identity-protocols.oidc-rp-initiated-logout
name: oidc-rp-initiated-logout
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oidc-rp-initiated-logout, oidc-logout, rp-initiated-logout, end_session_endpoint, post_logout_redirect_uri, id_token_hint, identity-protocols]
level: practitioner
status: docs-checked
description: "Log out at the OP from the RP with end_session_endpoint, id_token_hint, post_logout_redirect_uri, state and the registration of redirect URIs."
sources:
  - https://openid.net/specs/openid-connect-rpinitiated-1_0.html
  - https://openid.net/specs/openid-connect-frontchannel-1_0.html
  - https://openid.net/specs/openid-connect-backchannel-1_0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RP-Initiated Logout

Goal: end the OP session when the user logs out of the app.

Method: redirect to the OP's `end_session_endpoint` (from discovery; GET or POST) with `id_token_hint=<id_token>` (recommended), `post_logout_redirect_uri=<uri>`, `state=<s>`, and optionally `client_id`, `logout_hint` and `ui_locales`. The OP should ask the user whether to log out, ends its session, notifies logged-in RPs via their registered logout mechanism, then redirects to the post-logout URI with `state`. Register `post_logout_redirect_uris`; the value sent must exactly match a registered one.

Gotchas:
- Without a valid `id_token_hint` (or if it does not belong to the current session) the OP must ask the user to confirm, and must not do post-logout redirection unless it can confirm the target by other means. Logout requests without a valid hint are a denial-of-service vector.
- `client_id` is mainly for sending `post_logout_redirect_uri` when no `id_token_hint` is sent; if both are present the OP must verify they match.
- `logout_hint` is interpreted at the OP's discretion.
- The OP should accept expired ID Tokens as hints for a current or recent session.
- Whether the RP logs out locally before redirecting is up to the RP: logout notifications can be unreliable and the user might not approve OP logout.
- The OP must not redirect when it detects errors in the request.

Verify: log out and check the RP lands on the registered post-logout page with `state`.

## Checked
2026-11-02. Confirmed against OpenID Connect RP-Initiated Logout 1.0 (sections 2, 2.1, 3, 3.1, 4, 6). Removed: "many OPs show a confirmation page and ignore the redirect" (replaced with the spec rules), "destroy the local session before redirecting" (spec leaves it to the RP) and "OP cookie is cleared".
Method: documentation only; no commands were run.

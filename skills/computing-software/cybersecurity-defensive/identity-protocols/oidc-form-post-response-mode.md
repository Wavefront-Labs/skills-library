---
id: computing-software.cybersecurity-defensive.identity-protocols.oidc-form-post-response-mode
name: oidc-form-post-response-mode
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oidc-form-post-response-mode, oidc-response-modes, form_post, response_mode, post-response, authorization-response, identity-protocols]
level: practitioner
status: docs-checked
description: "Deliver authorization responses by auto-submitted POST with response_mode=form_post, and the CSRF, CSP and cookie consequences."
sources:
  - https://openid.net/specs/oauth-v2-form-post-response-mode-1_0.html
  - https://openid.net/specs/oauth-v2-multiple-response-types-1_0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# form_post response mode

Goal: keep codes and tokens out of URLs.

Method: request `response_mode=form_post`. The OP returns an HTML form whose values are the authorization response parameters (`code`, `state`, `id_token` and so on), auto-submitted by the user agent as an HTTP POST (`application/x-www-form-urlencoded`) to the client's redirect URI. The form `action` must be the redirect URI and the method must be POST.

Gotchas:
- Because the response is intended to be used once, the OP must instruct the user agent and intermediaries not to store or reuse it (the spec's example sends `Cache-Control: no-cache, no-store`).
- The client must be able to process the message regardless of how the form submission was triggered (any technique the user agent supports may be used).
- The spec states it is safe to return responses whose default mode is query or fragment using `form_post`.
- Your callback therefore receives a POST, not a GET; routes and CSRF middleware must accept it.

Verify: complete a login and confirm the callback receives a POST with no code in the URL.

## Checked
2026-11-02. Confirmed against OAuth 2.0 Form Post Response Mode (sections 2, 4, Appendix A). Removed: the SameSite cookie guidance, CSP `form-action` note and "implicit and hybrid should use form_post", none of which the spec states.
Method: documentation only; no commands were run.

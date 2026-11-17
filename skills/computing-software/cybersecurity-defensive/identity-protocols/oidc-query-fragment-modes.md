---
id: computing-software.cybersecurity-defensive.identity-protocols.oidc-query-fragment-modes
name: oidc-query-fragment-modes
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oidc-query-fragment-modes, oidc-response-modes, response_mode, query, fragment, jarm, query.jwt, identity-protocols]
level: advanced
status: docs-checked
description: "Pick query, fragment, form_post or the JARM jwt modes for the response type, and why code with fragment or token in query is disallowed."
sources:
  - https://openid.net/specs/oauth-v2-multiple-response-types-1_0.html
  - https://openid.net/specs/oauth-v2-jarm.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# query, fragment and query.jwt response modes

Goal: choose a response mode that fits the flow.

Defaults: `query` for response type `code`; `fragment` for `token` and for `id_token`, `code token`, `code id_token`, `id_token token` and `code id_token token`, where the query encoding must not be used. `response_mode` is not recommended when it names the default. All parts of a multiple-valued response should use the same mode. JARM adds `query.jwt`, `fragment.jwt`, `form_post.jwt` and `jwt` (the default encoding for the type: `query.jwt` for `code`, `fragment.jwt` for `token` and the other types except `none`): the response is one parameter named `response` containing a JWT with `iss`, `aud`, `exp` and the response parameters (such as `code`, `state`).

Gotchas:
- `query.jwt` must not be used with response types containing `token` or `id_token` unless the JWT is encrypted.
- JARM validation: check `iss`, `aud` equals your `client_id`, `exp`, and the signature before reading the code.
- `form_post` (a separate spec) is safe for responses whose default is query or fragment.

Verify: inspect the callback of each mode in a test client.

## Checked
2026-11-02. Confirmed against OAuth 2.0 Multiple Response Type Encoding Practices (sections 2, 5) and JARM (sections 2.1, 2.3). Removed: remarks about fragments not reaching the server, referrer/log leakage and "keep codes short-lived".
Method: documentation only; no commands were run.

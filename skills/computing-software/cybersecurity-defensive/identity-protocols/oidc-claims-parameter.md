---
id: computing-software.cybersecurity-defensive.identity-protocols.oidc-claims-parameter
name: oidc-claims-parameter
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oidc-claims-parameter, oidc-userinfo-claims, claims-parameter, essential, aggregated-claims, distributed-claims, _claim_names, identity-protocols]
level: advanced
status: docs-checked
description: "Request specific claims with the claims JSON parameter (essential, value, values) and read aggregated and distributed claims via _claim_names and _claim_sources."
sources:
  - https://openid.net/specs/openid-connect-core-1_0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Claims request parameter, aggregated and distributed claims

Goal: ask precisely for claims and handle claims from other providers.

Method: `claims={"userinfo":{"email":{"essential":true}},"id_token":{"acr":{"essential":true,"values":["urn:mace:incommon:iap:silver"]},"auth_time":{"essential":true}}}` (UTF-8 JSON, form-urlencoded in the request). `value`/`values` request particular values. If `acr` is requested as essential with `value`/`values` and the requirement cannot be met, the OP must treat that as a failed authentication attempt rather than return a weaker value. A `userinfo` request needs a `response_type` that issues an access token.

Aggregated claims: `_claim_names` maps claim names to a key in `_claim_sources`, whose member holds a `JWT` containing the claims. Distributed claims: the source member holds an `endpoint` (which must return the claim as a JWT) and optionally an `access_token`.

Gotchas:
- Support is optional; OPs advertise it with `claims_parameter_supported` (default false in Discovery), and an OP that ignores the parameter returns whatever claims it thinks useful.
- Not returning a requested claim is not an error, even if essential (except the `acr` and `sub` cases above); handle missing claims, including ones listed in `_claim_sources`.
- If both `acr_values` and an individual `acr` claim request with specific values are used, the behaviour is unspecified.

Verify: check discovery for `claims_parameter_supported` and `claims_supported`, and test an essential claim.

## Checked
2026-11-02. Confirmed against OpenID Connect Core 1.0 sections 5.5, 5.5.1, 5.5.1.1 and 5.6.2, and Discovery section 3. Removed: advice to verify aggregated JWT signatures separately and the SSRF allow-list note, which Core does not state.
Method: documentation only; no commands were run.

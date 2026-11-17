---
id: computing-software.cybersecurity-defensive.identity-protocols.oidc-scope-claim-mapping
name: oidc-scope-claim-mapping
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oidc-scope-claim-mapping, oidc-userinfo-claims, scopes, profile, email, address, phone, offline_access, email_verified, identity-protocols]
level: practitioner
status: docs-checked
description: "Map OIDC scopes to standard claims: profile, email, address, phone, offline_access, and decide which claims go in the ID token versus UserInfo."
sources:
  - https://openid.net/specs/openid-connect-core-1_0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Standard scopes and claim sets

Goal: request the smallest claim set.

- `openid`: required for an OpenID Connect request; the UserInfo response always includes `sub`.
- `profile`: name, family_name, given_name, middle_name, nickname, preferred_username, profile, picture, website, gender, birthdate, zoneinfo, locale, updated_at.
- `email`: `email`, `email_verified`.
- `address`: `address` JSON object. `phone`: `phone_number`, `phone_number_verified`.
- `offline_access`: requests a refresh token usable when the user is not present; `prompt=consent` must be used unless other conditions allow it, and the OP must ignore it unless the response type returns an authorization code.

Gotchas:
- Claims from these scopes are voluntary claims; the user may decline some and an OP may omit them without error.
- `email_verified` is a boolean claim; link accounts by email only if it is true and the issuer's verification is trusted.
- With a response type that issues an access token (for example `code`) the scope claims come from the UserInfo endpoint; with `id_token` only they come in the ID Token.
- Claims like `groups` or `roles` are not in the Core standard claim set.

Verify: request each scope separately and diff the claims.

## Checked
2026-11-02. Confirmed against OpenID Connect Core 1.0 sections 5.1, 5.3.2, 5.4 and 11. Removed: "some vendors send strings" and the claim that the OP decides ID token or UserInfo "(confirm)", now replaced by the section 5.4 rule.
Method: documentation only; no commands were run.

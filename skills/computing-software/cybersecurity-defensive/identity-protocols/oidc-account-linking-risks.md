---
id: computing-software.cybersecurity-defensive.identity-protocols.oidc-account-linking-risks
name: oidc-account-linking-risks
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oidc-account-linking-risks, oidc-security-considerations, account-linking, email_verified, iss-sub, noauth, account-takeover, identity-protocols]
level: advanced
status: docs-checked
description: "Link OIDC logins to local accounts safely: key on iss plus sub, never trust unverified email, and handle multi-tenant issuers and nOAuth-style attacks."
sources:
  - https://openid.net/specs/openid-connect-core-1_0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Account linking and email claim pitfalls

Goal: avoid account takeover through claims.

Method:
- Key accounts on the pair (`iss`, `sub`). `sub` is locally unique and never reassigned only within its Issuer, and is at most 255 ASCII characters, so store `iss` with it.
- `email_verified` true means the OP took affirmative steps to ensure the address was controlled by the End-User when verification was performed; how an address is verified is context specific and depends on the trust framework or contractual agreements. Link by email only when it is true and you accept that issuer's verification.

Gotchas:
- An OP may choose not to return a requested claim (not an error), so `email` and `email_verified` can be absent.
- `email_verified` is a JSON boolean in the spec; treat a missing value as not verified.

Verify: log in with a test OP that returns `email_verified: false` and confirm no existing account is linked.

## Checked
2026-11-02. Confirmed against OpenID Connect Core 1.0: ID Token `iss`/`sub` definitions (section 2), `email_verified` definition (5.1), claims may be omitted (5.3.2). Removed: the nOAuth tenant-admin, pre-hijacking and multi-IdP trust-surface claims, which Core does not state.
Method: documentation only; no commands were run.

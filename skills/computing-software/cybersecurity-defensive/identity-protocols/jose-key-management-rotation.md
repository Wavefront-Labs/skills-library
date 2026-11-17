---
id: computing-software.cybersecurity-defensive.identity-protocols.jose-key-management-rotation
name: jose-key-management-rotation
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [jose-key-management-rotation, jose-jwe-jwk, key-rotation, kms, hsm, signing-key, emergency-rotation, identity-protocols]
level: advanced
status: docs-checked
description: "Generate and rotate signing keys for token issuers: HSM or KMS storage, rotation schedule, overlapping publication and emergency revocation."
sources:
  - https://www.rfc-editor.org/rfc/rfc7517
  - https://www.rfc-editor.org/rfc/rfc7638
  - https://www.rfc-editor.org/rfc/rfc8725
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JOSE key generation, storage and rotation

Goal: rotate keys without invalidating live tokens.

Method:
1. Give every key its own `kid` (RFC 7517: different keys in one JWK Set SHOULD use distinct `kid` values; `kid` is used to choose among the keys of a JWK Set during key rollover). An RFC 7638 thumbprint is one value that may be used as a `kid`.
2. Publish the new public key in the JWK Set next to the old one before any token is signed with it.
3. Switch signing to the new key and put its `kid` in the JWS/JWE header so verifiers pick the right key.
4. Keep the old public key in the set until every token signed with it has expired, then remove it.

Gotchas:
- Verifiers choose the key from the `kid` header; RFC 8725 says the application must validate a received `kid` so that it cannot cause SQL or LDAP injection.
- Validate that the keys used for a JWT belong to its `iss` (RFC 8725, validate issuer and subject).

Verify: run a rotation in staging and replay old tokens.

## Checked

Date: 2026-11-02. Confirmed in RFC 7517 (kid, JWK Set, key rollover), RFC 7638 (thumbprint usable as kid) and RFC 8725 (kid injection, issuer key validation). Removed as not stated there: KMS/HSM non-exportable keys, rotation interval of months, emergency-rotation procedure, JWKS cache-period advice, cross-purpose key reuse guidance.

Method: documentation only; no commands were run.

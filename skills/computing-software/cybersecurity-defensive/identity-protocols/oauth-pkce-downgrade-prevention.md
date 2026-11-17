---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-pkce-downgrade-prevention
name: oauth-pkce-downgrade-prevention
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-pkce-downgrade-prevention, oauth-pkce, pkce-downgrade, plain, code_challenge_methods_supported, enforcement, identity-protocols]
level: advanced
status: docs-checked
description: "Stop PKCE downgrade: AS rejects plain, requires the verifier whenever a challenge was issued, and clients check code_challenge_methods_supported."
sources:
  - https://www.rfc-editor.org/rfc/rfc7636
  - https://www.rfc-editor.org/rfc/rfc9700
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Preventing PKCE downgrade and plain method

Goal: ensure the PKCE protection cannot be stripped.

Method:
- AS: accept `plain` only for clients that cannot support `S256`; enforce the `code_verifier` at the token endpoint if a challenge was in the authorization request, and accept a token request with a `code_verifier` only if a challenge was present (RFC 9700 section 2.1.1).
- Client: check `code_challenge_methods_supported` in AS metadata; always send `S256` (the method defaults to `plain` when `code_challenge_method` is absent).
- Attack: attacker removes `code_challenge` from the authorization request in transit; an AS that does not require it then accepts a token request without a verifier.

Gotchas:
- Public clients MUST use PKCE and the AS MUST support it (RFC 9700); a server may use a deployment-specific way to signal support instead of publishing metadata, so test S256 if the field is absent.

Verify: send a token request with a `code_verifier` for a code issued without a challenge and expect rejection.

## Checked

2026-11-02. Confirmed against RFC 9700 section 2.1.1 (downgrade rule, support detection, metadata field) and RFC 7636 sections 4.2 to 4.6 (`plain` default, `S256`, verifier check). Removed: the OAuth 2.1 statement and the fail-closed rule (not in either RFC).
Method: documentation only; no commands were run.

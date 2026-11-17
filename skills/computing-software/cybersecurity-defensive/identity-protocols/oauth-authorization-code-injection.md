---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-authorization-code-injection
name: oauth-authorization-code-injection
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-authorization-code-injection, oauth-authorization-code-security, code-injection, code-replay, single-use, pkce, revoke-on-reuse, identity-protocols]
level: advanced
status: docs-checked
description: "Defend against stolen or injected authorization codes with PKCE binding, single use, short lifetime and revoking tokens issued from a replayed code."
sources:
  - https://www.rfc-editor.org/rfc/rfc6749
  - https://www.rfc-editor.org/rfc/rfc9700
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Authorization code injection and replay

Goal: make a leaked or injected code useless.

Method:
- AS: codes short-lived and single-use (RFC 6749 recommends a maximum lifetime of 10 minutes), bound to the client and redirect URI they were issued for and, when one was sent, to the `code_challenge`.
- On a second use of a code, reject it and, when possible, revoke the tokens already issued from it (RFC 6749 section 4.1.2).
- Public clients MUST use PKCE; it is RECOMMENDED for confidential clients (RFC 9700 section 2.1.1). The AS must enforce the `code_verifier` whenever a `code_challenge` was sent, and accept a `code_verifier` only if a challenge was present.
- Client: bind each authorization request to the user agent (PKCE or one-time `state`) and reject callbacks that match no pending request.

Gotchas:
- Attack (RFC 9700 section 4.5): the attacker injects a stolen authorization code into the attacker's own session with the client, to associate that session with the victim's resources or identity. A PKCE verifier mismatch stops it.
- Codes in logs and Referer headers: avoid third-party scripts on the callback page and set `Referrer-Policy: no-referrer`.

Verify: redeem the same code twice and check that the second attempt is rejected and the first token is revoked.

## Checked

2026-11-02. Confirmed against RFC 6749 (maximum code lifetime of 10 minutes recommended, single use, revocation on reuse) and RFC 9700 (PKCE rules, verifier enforcement and downgrade rule, code injection description, CSRF prevention, `Referrer-Policy: no-referrer`). Removed: the 60-second lifetime (not in either RFC) and corrected the attack description, which had it reversed.
Method: documentation only; no commands were run.

---
id: computing-software.cybersecurity-defensive.identity-protocols.oidc-nonce-replay-protection
name: oidc-nonce-replay-protection
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oidc-nonce-replay-protection, oidc-id-token, nonce, state, csrf, replay, session-binding, identity-protocols]
level: practitioner
status: docs-checked
description: "Bind the browser session to the ID token with nonce and to the callback with state: generation, storage, one-time use and the difference between them."
sources:
  - https://openid.net/specs/openid-connect-core-1_0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nonce and state usage

Goal: block login CSRF and token replay.

Method:
- `state` (RECOMMENDED): opaque value maintaining state between request and callback; CSRF mitigation is typically done by cryptographically binding it to a browser cookie. Authorization servers echo it back; implicit-flow clients must verify it equals the one sent.
- `nonce`: a string with sufficient entropy to prevent guessing, passed unmodified from the authentication request to the ID Token. If it was sent, the ID Token must contain it and the client must check it matches and should check for replay. Required for the implicit flow.
- Core's implementation note: for web server clients store a cryptographically random value as an HttpOnly session cookie and use a cryptographic hash of it as the `nonce`; compare the ID Token nonce with the hash of the cookie to detect replay by third parties. For browser clients the random value can be kept in HTML5 local storage, with its hash used as the nonce.

Gotchas:
- The nonce must be unguessable and include per-session state.
- In the code flow `nonce` is optional in the request.

Verify: replay a captured callback in a new browser and confirm failure.

## Checked
2026-11-02. Confirmed against OpenID Connect Core 1.0 sections 3.1.2.1, 3.1.3.7, 3.2.2.1, 3.2.2.9 and 15.5.2. Removed: the 128-bit state minimum, "PKCE verifier can serve as state", "delete after one use", "localStorage readable by XSS" (Core itself describes local storage) and "some OPs require nonce".
Method: documentation only; no commands were run.

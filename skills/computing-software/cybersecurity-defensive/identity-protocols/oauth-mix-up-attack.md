---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-mix-up-attack
name: oauth-mix-up-attack
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-mix-up-attack, oauth-security-bcp, mix-up, malicious-authorization-server, iss, redirect-uri-per-as, identity-protocols]
level: sme
status: docs-checked
description: "Understand the OAuth mix-up attack where a malicious AS tricks a client, and apply iss checks, per-AS redirect URIs and exact token endpoint binding."
sources:
  - https://www.rfc-editor.org/rfc/rfc9700
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mix-up attack and defences

Goal: stop cross-AS code redemption.

Attack: a client supports several ASes. The attacker's AS (A-AS) is presented as an option; the user is redirected to the honest AS (H-AS) but the client believes it started with A-AS. The honest AS returns a code to the shared redirect URI; the client, still assuming A-AS issued it, redeems it at A-AS's token endpoint, so the attacker obtains the code and can exchange it (public clients) or inject it (RFC 9700 section 4.4.1).

Defences (clients that use two or more ASes MUST prevent mix-up): for each authorization request store the issuer the request was sent to, bound to the user agent, and then either validate the `iss` parameter or ID Token `iss` against it (RFC 9207), or use a distinct redirect URI per issuer (SHOULD be used only if other options are not available).

Gotchas:
- Storing only the AS URL is not enough: an attacker can pair an honest authorization endpoint with a token endpoint under its own control.
- An attacker AS can arise through dynamic registration or a compromised AS; some variants misuse OpenID Connect Discovery.

Verify: configure the client to compare iss with the AS stored in session and test a mismatch.

## Checked

2026-11-02. Confirmed against RFC 9700 sections 2.1, 4.4.1 and 4.4.2 (attack steps, variants, the two defences) and RFC 9207. Removed: the claim that the PKCE verifier leaks, the statement that PKCE alone does not stop it, and the dynamic AS selection remark.
Method: documentation only; no commands were run.

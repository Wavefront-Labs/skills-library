---
id: computing-software.cybersecurity-defensive.identity-protocols.fapi2-sender-constraining-choice
name: fapi2-sender-constraining-choice
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [fapi2-sender-constraining-choice, fapi2, mtls, dpop, sender-constrained, cnf, identity-protocols]
level: sme
status: docs-checked
description: "Pick mTLS or DPoP for FAPI 2.0 sender-constrained tokens: what the profile allows, TLS termination, DPoP replay mitigations and browser keys."
sources:
  - https://openid.net/specs/fapi-security-profile-2_0.html
  - https://www.rfc-editor.org/rfc/rfc8705
  - https://www.rfc-editor.org/rfc/rfc9449
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing mTLS versus DPoP in FAPI

Goal: choose the binding that fits the deployment.

What FAPI 2.0 Security Profile (section 5.3.2.1) says: an authorization server shall use one of MTLS (RFC 8705) or DPoP (RFC 9449) for sender-constrained access tokens, and shall authenticate clients using MTLS (RFC 8705 section 2) or `private_key_jwt`. The profile's change table notes that, due to the lack of tight integration with the TLS layer, DPoP can be easier to deploy in some scenarios. If using DPoP, the server may use the server-provided nonce mechanism and shall support authorization code binding to the DPoP key.

Trade-offs, as the specs state them:
- mTLS (RFC 8705): the token is bound to the client certificate (thumbprint, `cnf` claim). If TLS is terminated at a load balancer or reverse proxy, how the client certificate metadata reaches the application server is out of scope of RFC 8705 (section 6.5), so you must design and secure that path yourself.
- DPoP (RFC 9449): an application-layer proof, so it does not depend on the TLS layer. The profile's section 6.2 warns that DPoP proofs can be replayed and reused with an altered request, since DPoP does not sign the body or most headers; mitigations it lists are short-lived nonces, `jti` replay prevention at the resource server, signed requests (FAPI Message Signing) and considering MTLS instead. It says these may not be necessary for many ecosystems.
- Browser clients: RFC 9449 says that if the private key is non-extractable (possible with WebCrypto), DPoP renders exfiltrated tokens alone unusable; code running in the client can still use the key to make proofs.
- Cuckoo's token (profile section 6.3): stolen-token injection can bypass either binding; mitigations include different DPoP keys or certificates per authorization server.

Decision rule (judgement, not from the specs): choose mTLS where you control TLS termination and certificate lifecycle (typical server-to-server), and DPoP where TLS is terminated by intermediaries you do not control or the client is a browser or mobile app. Never accept a token in a form that permits use without its proof.

Gotchas:
- The profile also tells servers not to use refresh token rotation except in extraordinary circumstances.

Verify: present the access token without a proof and expect a 401 with a `WWW-Authenticate: DPoP` challenge (error `invalid_token`, or `use_dpop_nonce` when a nonce is required).

## Checked

2026-11-09. Read FAPI 2.0 Security Profile sections 5.3.2.1, the change table and 6.1 to 6.3, RFC 8705 section 6.5 and 7.1 to 7.2, and the RFC 9449 introduction and DPoP error examples. Replaced the old fapi-2_0-security-profile.html URL (renamed to fapi-security-profile-2_0.html). Removed: the message-signing source, "silently weakens" proxy claim, header trust model, replay-cache and per-request nonce claims presented as universal.
Method: documentation only; no commands were run.

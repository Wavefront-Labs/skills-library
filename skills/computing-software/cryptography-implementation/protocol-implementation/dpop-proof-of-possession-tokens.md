---
id: computing-software.cryptography-implementation.protocol-implementation.dpop-proof-of-possession-tokens
name: dpop-proof-of-possession-tokens
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, dpop-proof, dpop, rfc-9449, oauth, proof-of-possession, jwt, sender-constrained-tokens, jwk-thumbprint]
level: advanced
status: docs-checked
description: "Implement and validate OAuth DPoP (RFC 9449): proof JWT header and claims, ath and nonce, jkt binding, replay cache, and resource server checks."
sources: ["https://www.rfc-editor.org/rfc/rfc9449", "https://www.rfc-editor.org/rfc/rfc7638", "https://www.rfc-editor.org/rfc/rfc8725"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DPoP proof-of-possession tokens

DPoP binds an access token to a client key so a stolen token is useless without the private key.

## Proof JWT (sent in the `DPoP` header on each request)
Header: `{"typ": "dpop+jwt", "alg": "ES256", "jwk": {<client public key>}}`
Claims:
| Claim | Value |
|---|---|
| `jti` | Unique id (replay detection) |
| `htm` | HTTP method, e.g. `POST` |
| `htu` | Target URI without query and fragment |
| `iat` | Issue time |
| `ath` | base64url(SHA-256(access token)) - on resource requests |
| `nonce` | Server-supplied nonce (`DPoP-Nonce` response header), when required |

## Token request
Client sends `DPoP: <proof>` to the token endpoint; the authorisation server issues a token with
`"cnf": {"jkt": "<JWK thumbprint>"}` and `token_type: DPoP`.

## Resource request
`Authorization: DPoP <access_token>` plus a fresh `DPoP: <proof>` with `ath`.

## Server validation checklist
1. Not more than one `DPoP` header; parse as JWT with `typ` = `dpop+jwt`.
2. `alg` is a registered asymmetric signature algorithm (not `none`, not a MAC) acceptable to local policy; `jwk`
   contains no private key.
3. Signature verifies with the embedded `jwk`.
4. `htm` matches the request method and `htu` matches the request URI, ignoring query and fragment.
5. `iat` is within an acceptable time window and, when the server requires one, `nonce` matches a recent server nonce.
6. `jti` not seen before within the window (replay cache keyed by jti; reject or hash oversized jti values to avoid
   memory exhaustion).
7. Resource server: `ath` equals the hash of the presented token; thumbprint of `jwk` equals token `cnf.jkt`.
   `ath` alone does not stop proof replay, so still check the time window, `htm` and `htu`.

## Client notes
- Keep the private key as protected as the platform allows; a stolen key defeats the binding.
- When the server answers with `use_dpop_nonce` and a `DPoP-Nonce` header, retry with a proof that includes that
  nonce. Generate a fresh proof for every retry.

## Verify
- [ ] Replayed proof is rejected; proof for a different URL or method is rejected.
- [ ] Token used with a different key's proof is rejected.

## Checked
2026-11-01. Confirmed against RFC 9449: sections 4.2 (header and claims), 4.3 (validation), 5 and 6 (token_type
DPoP, cnf.jkt as base64url SHA-256 JWK thumbprint), 7 (Authorization: DPoP, ath), 8 and 9 (nonce, use_dpop_nonce),
11 (jti tracking, asymmetric algorithms only). Removed: a fixed 60 s window and the WebCrypto, Android Keystore and
Secure Enclave key-storage specifics (not in the RFC).
Method: documentation only; no commands were run.

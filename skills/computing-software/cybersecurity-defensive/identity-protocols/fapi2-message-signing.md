---
id: computing-software.cybersecurity-defensive.identity-protocols.fapi2-message-signing
name: fapi2-message-signing
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [fapi2-message-signing, fapi2, fapi, message-signing, jar, jarm, non-repudiation, identity-protocols]
level: sme
status: docs-checked
description: "Add non-repudiation to FAPI 2.0: signed authorization requests (JAR), signed responses (JARM), signed introspection responses and ID tokens."
sources:
  - https://openid.net/specs/fapi-message-signing-2_0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FAPI 2.0 Message Signing

Goal: produce verifiable evidence of requests and responses. Non-repudiation here means the owner of the signing key cannot convincingly deny having signed the data; it is achieved with application-level signatures stored with the payload and metadata.

Covered messages (section 5.2): NR1 pushed authorization requests, NR2 front-channel authorization requests, NR3 authorization responses, NR4 introspection responses, NR5 ID tokens. Each of the first three methods is a separate conformance option, so an ecosystem may adopt only some.

Requirements (the page fetched was draft fapi-message-signing-2_0-02; re-check the current text):
- Signed requests, JAR (RFC 9101): the AS must support, require and verify signed request objects. `aud` must be (or contain) the AS issuer URL; `nbf` must be present and no more than 60 minutes in the past; `exp` no more than 60 minutes after `nbf`; the AS accepts `typ` of `oauth-authz-req+jwt`. Clients send all authorization parameters to the PAR endpoint in a JAR, with `aud`, `nbf` and `exp` (lifetime at most 60 minutes).
- Signed responses, JARM: the AS must support, require and issue signed authorization responses; clients set `response_mode=jwt` and verify the signature. When using JARM, only the RFC 9207 `iss` parameter should be repeated inside the JWT per the spec's note.
- Signed introspection, RFC 9701: the AS signs introspection responses issued in JWT format; the client requests and verifies them.
- ID tokens: no additional requirement; FAPI 2.0 Security Profile servers already sign ID tokens.

Gotchas:
- The spec warns that values signed in a JARM response may be of limited value for non-repudiation, since they are artifacts of the AS rather than something the client signed (see its security considerations, 6.6).
- Non-repudiation in practice means keeping the signed artefacts with their verification keys; that retention practice is advice, not spec text.

Verify: store a sample signed request object and re-verify it later with the archived public key.

## Checked

Method: 2026-11-09 docs-only; fetched fapi-message-signing-2_0.html (draft -02) and read section 5.1 to 5.6 requirement lists plus 6.6 opening line; not every paragraph of section 6 was read. Removed the HTTP message signatures (RFC 9421) bullet, algorithm and key-rotation specifics, which the page does not state; the old fapi-2_0-message-signing.html and security-profile sources were dropped.

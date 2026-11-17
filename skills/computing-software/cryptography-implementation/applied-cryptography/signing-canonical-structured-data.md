---
id: computing-software.cryptography-implementation.applied-cryptography.signing-canonical-structured-data
name: signing-canonical-structured-data
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, digital-signatures, signed-payload-design, canonicalization, jcs, rfc8785, domain-separation, signing-context, cbor-cose]
level: advanced
status: docs-checked
description: "Decide exactly what bytes to sign: sign what you transmit, bind type/version/audience context, avoid JSON canonicalization traps, use COSE/JWS/DSSE."
sources: ["https://datatracker.ietf.org/doc/html/rfc8785", "https://github.com/secure-systems-lab/dsse", "https://datatracker.ietf.org/doc/html/rfc9052"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Signing canonical structured data

A signature covers bytes, not meaning. Bugs appear when signer and verifier
serialize the "same" object to different bytes, or when a signature over one
kind of message is accepted as another.

## Rule 1: sign the bytes you send, verify the bytes you received

Serialize once, sign those bytes, transmit both; the verifier checks the
signature over the received bytes **before** parsing, then parses those same
bytes. Never re-serialize a parsed object to verify it. JSON re-serialization
changes key order, whitespace, number formats and Unicode escapes.

## Rule 2: if you must canonicalize, use a standard

When signatures must survive re-serialization (stored documents edited by
other systems), use a specified canonical form: JSON Canonicalization Scheme
(RFC 8785 JCS), deterministic CBOR (RFC 8949 4.2). Ad-hoc "sort keys and dump" breaks on number formatting and
duplicate keys (JCS fixes number serialisation and forbids duplicate property names).

## Rule 3: bind context into the signed bytes

Include, inside the signed payload or as a pre-authentication prefix:
- **Type/purpose** (`"type": "payment-instruction"`) and **version**.
- **Audience/recipient** and **issuer**.
- **Freshness**: timestamp, expiry, nonce/sequence.
- **Domain separation** for the key: a fixed context string, so a signature
  made for one protocol cannot be replayed into another that uses the same key.

DSSE (used by in-toto and Sigstore) is a signing envelope format; read its
protocol document for exactly which bytes it signs.

## Use an envelope format

| Format | Use |
|---|---|
| JWS | JSON/HTTP APIs; protect alg in header, allowlist algorithms |
| COSE_Sign1 (RFC 9052) | CBOR |
| DSSE | Supply-chain attestations |
| Detached signature + manifest hash | Files, releases |

## Avoid

- Concatenating fields without lengths (`user || amount` collides: "ab"+"c" vs "a"+"bc").
- Signing a hash computed by the client of something the server later
  interprets differently.
- Partial signatures (only some fields), letting attackers add unsigned fields
  that the application then trusts.

## Verify

- [ ] Verifier checks the signature over received bytes before parsing.
- [ ] Payload includes type, version, audience and expiry.
- [ ] Field encoding is length-prefixed or a standard canonical form; tests cover re-serialization.

## Checked

- 2026-11-01. Confirmed: JCS (RFC 8785) builds on ECMAScript number serialisation, deterministic property sorting and forbids duplicate property names; COSE_Sign1 exists in RFC 9052, which aligns with the core deterministic encoding of RFC 8949 section 4.2.1; DSSE is used by in-toto and Sigstore (DSSE repository).
- Removed as unconfirmed: DSSE PAE byte layout, Unicode normalisation and XML C14N remarks, RFC 7515 number, WebAuthn and mdoc use, the Latacora source (page unreadable).

Method: documentation only; no commands were run.

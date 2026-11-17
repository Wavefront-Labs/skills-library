---
id: computing-software.cryptography-implementation.applied-cryptography.ml-dsa-context-strings-and-hashml-dsa
name: ml-dsa-context-strings-and-hashml-dsa
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, ml-dsa, hashml-dsa, context-string, prehash, external-mu, fips-204, domain-separation]
level: advanced
status: docs-checked
description: "Use ML-DSA context strings for domain separation, and decide between pure ML-DSA, external mu and HashML-DSA for large or streamed messages."
sources: ["https://csrc.nist.gov/pubs/fips/204/final", "https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ML-DSA context strings and HashML-DSA

## Context strings

FIPS 204 signs `M' = 0x00 || len(ctx) || ctx || M` in pure ML-DSA, where
`ctx` is 0-255 bytes and defaults to empty. Use it for domain separation:

- Different applications or message types sharing one key get distinct
  contexts (`b"acme-firmware-v1"`, `b"acme-audit-log-v1"`), so a signature
  from one cannot be replayed into the other.
- Verifier must use the same context; it is not transmitted in the signature.
- Some profiles fix `ctx` to empty (the LAMPS X.509 profile); follow the
  protocol, and prefer one key per purpose anyway.

## Pure, external mu, or HashML-DSA

| Mode | Signs | Use when |
|---|---|---|
| Pure ML-DSA | The whole message | Default; messages fit in memory |
| External mu | `mu = SHAKE256(tr || M')` computed by the caller, signed by the module | HSM/remote signer: send 64-byte mu instead of the message; output is a normal ML-DSA signature |
| HashML-DSA | `M' = 0x01 || len(ctx) || ctx || OID(PH) || PH(M)` | Protocol requires prehashing with a standard hash; separate OIDs |

Key points:
- HashML-DSA signatures are **not** interchangeable with pure ML-DSA; the
  0x01 domain byte and separate algorithm identifiers make them distinct.
- External mu keeps pure-ML-DSA compatibility while avoiding shipping large
  messages to an HSM; it needs the public key hash `tr` on the caller side.
- The LAMPS X.509 profile uses pure ML-DSA only; do not use HashML-DSA for
  certificates.

## Pitfalls

- Signing your own `SHA-256(M)` with pure ML-DSA is neither HashML-DSA nor
  external mu; verifiers that hash differently will fail interop. Name the
  construction in the spec.
- A context string is at most 255 bytes (FIPS 204 section 5.2).

## Verify

- [ ] Each key's mode (pure / external mu / HashML-DSA) and ctx are documented.
- [ ] A signature made with ctx A fails verification with ctx B.

## Checked
2026-11-01. Confirmed in the FIPS 204 PDF: M' = 0x00 || len(ctx) || ctx || M for pure ML-DSA, M' with 0x01, ctx, OID and PH(M) for HashML-DSA, the 255-byte context limit and empty default. Confirmed in RFC 9881: ctx left at the empty string in X.509, HashML-DSA must not be used in PKIX certificates, and the External mu computation (hash of the public key, 0x00 domain byte, ctx and message, 64-byte mu). Removed the unread NIST FAQ source and the claim that long contexts are not truncated.
Method: documentation only; no commands were run.

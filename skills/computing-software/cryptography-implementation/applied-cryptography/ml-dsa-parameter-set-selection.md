---
id: computing-software.cryptography-implementation.applied-cryptography.ml-dsa-parameter-set-selection
name: ml-dsa-parameter-set-selection
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, ml-dsa, ml-dsa-parameter-sets, fips-204, dilithium, post-quantum-signatures, signature-size, cnsa-2-0]
level: practitioner
status: docs-checked
description: "Pick ML-DSA-44, 65 or 87: security categories, public key and signature sizes, policy requirements, and how sizes affect certificates and tokens."
sources: ["https://csrc.nist.gov/pubs/fips/204/final", "https://datatracker.ietf.org/doc/rfc9881/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ML-DSA-44/65/87 selection and sizes

ML-DSA (FIPS 204, formerly Dilithium) is NIST's primary post-quantum
signature scheme.

| Parameter set | NIST category | Public key | Private key (expanded) | Signature |
|---|---|---|---|---|
| ML-DSA-44 | 2 | 1312 B | 2560 B | 2420 B |
| ML-DSA-65 | 3 | 1952 B | 4032 B | 3309 B |
| ML-DSA-87 | 5 | 2592 B | 4896 B | 4627 B |

The private key can be stored as a 32-byte seed; the X.509 profile (RFC 9881) recommends the seed-only format
because the expanded key can be derived from it. Sizes above are from that RFC's parameter table.

## How to choose

- **ML-DSA-65**: general default for new PQ signatures and most hybrid
  composites.
- **ML-DSA-87**: highest category; check your policy (for example CNSA 2.0 for national security systems, whose
  document could not be read in this review) and use it for very long-lived roots of trust.
- **ML-DSA-44**: size-sensitive uses where category 2 is acceptable
  (high-volume tokens, constrained devices).
- For firmware and roots that verify rarely and must last decades,
  consider SLH-DSA or LMS/XMSS (hash-based) instead or as well.

## Size consequences

- Every certificate carries a public key of 1312 to 2592 bytes and a signature of 2420 to 4627 bytes, so add these
  per certificate in the chain and compare with your ECDSA chain.
- Tokens carry a signature of 2420 to 4627 bytes; check HTTP header limits against the real size.
- Database columns, protobuf limits, QR codes and smart-card storage sized
  for 64-byte signatures will overflow.

## Library support

Check your library's documentation for ML-DSA support and which parameter sets and key formats it accepts; the
OpenSSL 3.2.3 used for this review has no ML-DSA algorithm.

## Verify

- [ ] Parameter set fixed per key in metadata; verifiers reject other sets.
- [ ] Storage and transport limits tested with real signature sizes.

## Checked
Date: 2026-10-31. Confirmed in RFC 9881: NIST security levels 2, 3 and 5 for ML-DSA-44, 65 and 87, public key sizes
(1312, 1952, 2592), signature sizes (2420, 3309, 4627), expanded private key sizes (2560, 4032, 4896), 32-byte seed
and the seed-only recommendation. Removed (not confirmed): Ed25519 comparison, CNSA 2.0 requirement (PDF blocked),
certificate chain and token size estimates, library and version claims. NIST FIPS 204 page is an abstract only.
Ran `openssl list -signature-algorithms` (3.2.3): no ML-DSA entries.
Method: documentation only; the only command run was that read-only OpenSSL listing.

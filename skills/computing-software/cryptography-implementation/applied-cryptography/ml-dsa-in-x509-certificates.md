---
id: computing-software.cryptography-implementation.applied-cryptography.ml-dsa-in-x509-certificates
name: ml-dsa-in-x509-certificates
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, ml-dsa-certificates, ml-dsa, x509, pq-pki, lamps, certificate-issuance, post-quantum, oid]
level: advanced
status: docs-checked
description: "Issue and validate ML-DSA certificates per RFC 9881: OIDs and encodings, key usage rules, HashML-DSA ban, private key formats and chain design during migration."
sources: ["https://www.rfc-editor.org/rfc/rfc9881"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ML-DSA in X.509 certificates

## Encoding (RFC 9881)
- AlgorithmIdentifier: OID only, parameters **absent** (id-ml-dsa-44 2.16.840.1.101.3.4.3.17, -65 .18, -87 .19).
- SubjectPublicKeyInfo: raw public key bytes in the BIT STRING.
- Signature value: raw ML-DSA signature; certificates use pure ML-DSA with an empty context string.
- Private keys (PKCS#8): CHOICE of seed (32 bytes), expanded key, or both; seed is recommended.
- HashML-DSA must not be used in certificates, CRLs or OCSP.

## Key usage
- End-entity: `digitalSignature` (and `nonRepudiation` if relevant). ML-DSA keys must not have
  `keyEncipherment` or `keyAgreement`, or any other key-establishment bit.
- CA: `keyCertSign`, `cRLSign`.

## Chain designs during migration
| Design | Notes |
|---|---|
| All-ML-DSA hierarchy | Clean; only PQ-capable relying parties can validate. |
| Classical root signing an ML-DSA intermediate | No quantum protection for the chain until the root is PQ. |
| Parallel hierarchies (classical and PQ certs per endpoint) | Serve by capability (TLS signature_algorithms). |

## Size and performance
ML-DSA keys and signatures are much larger than ECDSA ones, so chains grow; prefer short chains and measure the
handshake with your real chain. Check each client library and public CA program for current ML-DSA support before
relying on it.

## Verify
- [ ] The certificate shows the ML-DSA OID with no parameters.
- [ ] A relying party rejects an ML-DSA cert with keyEncipherment set.
- [ ] Handshake size measured with the real chain.

## Checked

2026-10-31. Confirmed in RFC 9881: OIDs 2.16.840.1.101.3.4.3.17/.18/.19, parameters absent, raw public
key in the BIT STRING, empty context string, permitted and forbidden key usage bits, seed/expandedKey/both
private key CHOICE with seed recommended, HashML-DSA prohibited. Removed: the composite-signature row and
source, the chain size figures, certificate compression and security-category remarks, and the library and
browser support list.

Method: documentation only; no commands were run.

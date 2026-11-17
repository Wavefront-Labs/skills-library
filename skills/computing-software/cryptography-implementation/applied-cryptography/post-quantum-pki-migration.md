---
id: computing-software.cryptography-implementation.applied-cryptography.post-quantum-pki-migration
name: post-quantum-pki-migration
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, pq-pki-migration, post-quantum, pki, ml-dsa, composite-signatures, related-certificates, rfc-9763, kem-certificates, root-ca]
level: sme
status: draft
description: "Plan PQ certificate migration: parallel hierarchies, composite and related certificates, KEM certificates, root distribution and relying-party capability rollout."
sources: ["https://www.rfc-editor.org/rfc/rfc9763", "https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/", "https://www.rfc-editor.org/rfc/rfc9629"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Post-quantum PKI migration

Signatures in PKI only need to resist forgery at verification time, so PKI migration is less urgent than key
exchange, but roots have long lives and device trust stores are slow to update, so it must start early.

## Strategies
| Strategy | How | Trade-off |
|---|---|---|
| Parallel hierarchies | New ML-DSA root and intermediates alongside the classical ones; endpoints hold two certs and pick by peer capability | Simple crypto, double operations |
| Composite certificates | One cert with a composite key (e.g. ML-DSA-65 + ECDSA P-256) and composite signature | Single chain; both algorithms must verify; needs composite-aware RPs |
| Related certificates (RFC 9763) | Two certificates linked by an extension proving the same subject | Lets protocols present both |
| KEM certificates (RFC 9629 KEMRecipientInfo in CMS) | ML-KEM public keys in certs for encryption (S/MIME) | Proof of possession needs a challenge, not a CSR signature |

## Order of work
1. Inventory every relying party and trust store (devices, Java cacerts, OS stores, embedded firmware).
2. Introduce the PQ root into trust stores years ahead; trust-store update latency is the critical path.
3. Pilot in closed ecosystems (internal mTLS, code signing, device identity) before WebPKI.
4. Shorten certificate lifetimes and automate issuance so switching algorithms is a configuration change.
5. Watch WebPKI direction (root program policies, Merkle Tree Certificates proposals) rather than guessing.

## Gotchas
- CSR proof-of-possession does not work for KEM keys; use the protocol's alternative (RFC 9629 / CMP).
- Certificate size growth hurts constrained protocols (IoT, DTLS); measure.
- HSM support for ML-DSA key generation and signing determines CA readiness; check firmware.

## Verify
- [ ] Inventory shows trust-store update path and lead time per relying-party class.
- [ ] Pilot PQ chain validated by every relying party in scope.

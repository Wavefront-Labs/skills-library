---
id: computing-software.cryptography-implementation.applied-cryptography.handling-pq-key-and-signature-sizes
name: handling-pq-key-and-signature-sizes
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, post-quantum-migration, pq-size-impact, ml-dsa, ml-kem, slh-dsa, certificate-chain-size, tcp-initcwnd, performance]
level: advanced
status: draft
description: "Plan for post-quantum size and speed: certificate chains over the TCP initial window, QUIC amplification limits, token and storage limits, mitigations."
sources: ["https://blog.cloudflare.com/pq-2024/", "https://www.rfc-editor.org/rfc/rfc8879", "https://datatracker.ietf.org/doc/draft-ietf-plants-merkle-tree-certs/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Handling PQ key and signature size impacts

ML-KEM is fast; its cost is bytes. ML-DSA and SLH-DSA cost bytes, and
SLH-DSA also costs signing time. Plan capacity and limits before switching.

## Sizes to budget (bytes)

| Item | Classical | PQ |
|---|---|---|
| KEM share (client/server) | X25519 32/32 | X25519MLKEM768 1216/1120 |
| Signature | Ed25519 64, ECDSA P-256 ~72 | ML-DSA-44 2420, ML-DSA-65 3309, SLH-DSA-128s 7856, SLH-DSA-128f 17088 |
| Public key | 32-65 | ML-DSA-65 1952 |

## Where it hurts

- **TLS with PQ certificates**: a chain of leaf + intermediate with ML-DSA
  keys and signatures, plus SCTs and the CertificateVerify, adds about
  10-15 KB. That exceeds the TCP initial congestion window (10 segments,
  ~14 KB) and costs an extra round trip; QUIC's 3x anti-amplification
  limit before address validation adds another.
- **Tokens**: JWT/COSE with ML-DSA approach HTTP header limits (8-16 KB in
  many proxies) when cookies are added.
- **Storage and schemas**: signature columns sized `VARBINARY(256)`,
  protobuf/size caps, DNSSEC over UDP, QR codes, smart cards, firmware
  partitions.
- **Throughput**: SLH-DSA signing is milliseconds to hundreds of ms; fine
  for firmware, wrong for per-request signing.

## Mitigations

- Shorter chains (no unnecessary intermediates); certificate compression
  (RFC 8879) helps classical parts more than PQ signatures.
- Merkle Tree Certificates and trust-anchor negotiation (IETF work) to drop
  signatures from the handshake.
- Keep classical signatures for short-lived authentication until PQ
  certificates are needed; prioritise ML-KEM first.
- Raise header limits deliberately, or move large tokens to the body.
- Pick ML-DSA-44 where category 2 suffices.

## Verify

- [ ] Load test with PQ-sized certs and tokens: handshake RTTs and header limits measured.
- [ ] Schemas and message caps sized for the largest chosen parameter set.

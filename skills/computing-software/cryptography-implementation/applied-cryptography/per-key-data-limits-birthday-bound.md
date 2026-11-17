---
id: computing-software.cryptography-implementation.applied-cryptography.per-key-data-limits-birthday-bound
name: per-key-data-limits-birthday-bound
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, birthday-bound-limits, birthday-bound, data-volume-limits, key-wearout, aes-cbc, aes-ctr, aes-gcm, key-rotation, sp-800-38a]
level: advanced
status: docs-checked
description: "Calculate how much data one key may encrypt under CBC, CTR and GCM from the block-size birthday bound, and enforce rotation before the limit."
sources: ["https://csrc.nist.gov/pubs/sp/800/38/a/final", "https://csrc.nist.gov/pubs/sp/800/38/d/final", "https://datatracker.ietf.org/doc/draft-irtf-cfrg-aead-limits/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Per-key data limits from the birthday bound

**Goal:** turn "AES is secure" into a concrete number of blocks or messages a key may process, and enforce it.

## The rule of thumb
For a block cipher with n-bit blocks used in CBC or CTR, an attacker's distinguishing advantage after q blocks is
about `q^2 / 2^(n+1)`. Pick a target advantage (TLS 1.3 uses a safety margin of about 2^-57 for AE security) and solve for q.

| Cipher | n | q for advantage 2^-33 | Data |
|---|---|---|---|
| AES (CBC/CTR) | 128 | 2^48 blocks | 4 PiB |
| 3DES / Blowfish | 64 | 2^16 blocks | 512 KiB |

AES-GCM adds per-message and random-IV invocation limits on top; read them in NIST SP 800-38D for your IV scheme.
- TLS 1.3 (RFC 8446 5.5): up to 2^24.5 full-size records (about 24 million) per connection for AES-GCM, with a safety
  margin of about 2^-57; for ChaCha20/Poly1305 the record sequence number wraps before the limit.

## Enforcing it
- Count per key version: messages encrypted and bytes encrypted. Store the counters with the key metadata.
- Rotate automatically when a counter passes a margin (for example 50% of the computed limit).
- For bulk storage, derive per-object keys (HKDF from a master key plus a random object salt) so no single AES key
  approaches the bound; this also makes random 96-bit nonces safe.
- For long-lived channels, use the protocol's rekey (TLS KeyUpdate, SSH rekey).

## Gotchas
- Limits are per key, not per process: replicas sharing a key share the budget.
- Integrity limits for GCM also depend on forgery attempts; count failed decryptions too (see the CFRG
  aead-limits draft for formulas).
- "Rotate yearly" says nothing about volume; a high-throughput service can exhaust a GCM random-IV budget in days.

## Verify
- [ ] Every key version records message and byte counters.
- [ ] Rotation triggers fire in a load test before the computed limit.
- [ ] Per-object key derivation is used for stores with billions of objects.

## Checked

2026-10-31. Confirmed: RFC 8446 section 5.5 (2^24.5 records, 2^-57 margin, ChaCha20/Poly1305 sequence-number
wrap) and the CFRG AEAD limits draft (forgery attempts count toward integrity limits; TLS integrity target 2^-57).
The table follows from q^2 / 2^(n+1) (2^48 AES blocks is 4 PiB; 2^16 64-bit blocks is 512 KiB). Removed: the
SP 800-38D figures (source not readable as text), the 2^-32 target remark and the WireGuard interval.

Method: documentation only; no commands were run.

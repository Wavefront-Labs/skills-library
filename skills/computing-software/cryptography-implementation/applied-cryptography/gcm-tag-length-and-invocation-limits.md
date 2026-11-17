---
id: computing-software.cryptography-implementation.applied-cryptography.gcm-tag-length-and-invocation-limits
name: gcm-tag-length-and-invocation-limits
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, aead, aes-gcm, gcm-tag-length, invocation-limits, nonce-reuse, sp-800-38d, rekeying]
level: advanced
status: verified
description: "Set AES-GCM tag length and per-key limits: 128-bit tags, 96-bit IVs, 2^32 random-IV invocations, TLS 1.3 record limits, and when to rotate keys."
sources: ["https://csrc.nist.gov/pubs/sp/800/38/d/final", "https://www.rfc-editor.org/rfc/rfc8446#section-5.5", "https://datatracker.ietf.org/doc/draft-irtf-cfrg-aead-limits/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GCM tag length and invocation limits

AES-GCM fails badly at its edges: short tags allow forgeries, and exceeding
per-key limits (or repeating a nonce) leaks the GHASH key `H`, after which
an attacker can forge any message. Decide the parameters once and enforce
them in code.

## Tag length

- Use the full **128-bit tag**. SP 800-38D permits 128, 120, 112, 104, 96;
  32 and 64 bits only under Appendix C guidelines (bounded packet length,
  bounded failed verifications, silent discard, error logging). Do not use them in new designs.
- Short tags are weaker than `2^-t` suggests: forgery probability grows with
  message length (Ferguson, "Authentication Weaknesses in GCM", 2005, the reference SP 800-38D Appendix B cites).
- Never let the receiver accept a tag length chosen by the sender. Fix it in
  code and validate `len(tag) == 16` before decrypting. pyca/cryptography
  `modes.GCM(iv, tag)` rejects tags under 16 bytes unless you pass
  `min_tag_length` (run: 12, 8 and 4 byte tags raise `ValueError`;
  `min_tag_length=4` accepts an 8-byte tag), and `AESGCM` always emits 16.

## IV length

Use 96-bit (12-byte) IVs. SP 800-38D caps total invocations at 2^32 for any other IV
length (deterministic construction) and for every RBG-based IV. Other lengths are run through GHASH to derive the
counter block, which breaks interop with 96-bit-only peers (pyca accepted 8, 12 and 16-byte IVs, run).

## Invocation limits per key (SP 800-38D 8.3)

| IV construction | Limit |
|---|---|
| Random (RBG-based) IVs | total invocations with the key shall not exceed 2^32 (collision probability at most 2^-32) |
| Deterministic 96-bit IVs | the 2^32 cap does not apply; the invocation field bounds it (2^s distinct inputs per fixed field and key for an s-bit field), and counters must never repeat across restarts and instances |
| Plaintext per message | at most 2^39 - 256 bits (about 64 GiB) |

Confidentiality and integrity bounds on total data are tighter than the
raw nonce limits. RFC 8446 5.5 allows up to 2^24.5 full-size AES-GCM
records on a connection (safety margin about 2^-57) and says implementations
SHOULD key-update before then; for ChaCha20/Poly1305 the sequence number wraps
first. The CFRG AEAD-limits draft (cited by RFC 8446 as [AEAD-LIMITS]) gives formulas for confidentiality
(CL) and integrity (IL) advantage if you need exact numbers.

## Enforce it

- Count encryptions per key in the key object (or per data key in envelope
  encryption: one fresh data key per object avoids the question).
- Rotate before the limit: rekey at, for example, 2^30 messages for random
  IVs to keep margin.
- In multi-instance services with random IVs, the limit is global across all
  instances sharing the key, not per process.
- If you cannot count, use AES-GCM-SIV (nonce-misuse resistant) or
  XChaCha20-Poly1305 (192-bit random nonces).

## Verify

- [ ] Tag length is a constant 16 bytes on both sides; truncated tags rejected.
- [ ] IVs are 12 bytes from a CSPRNG or a persisted, never-reset counter.
- [ ] Per-key usage count or per-object data keys keep usage below 2^32.
- [ ] Long-lived channels rekey (TLS KeyUpdate or equivalent) before 2^24.5 records.

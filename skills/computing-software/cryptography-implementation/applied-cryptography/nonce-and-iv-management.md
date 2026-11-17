---
id: computing-software.cryptography-implementation.applied-cryptography.nonce-and-iv-management
name: nonce-and-iv-management
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, nonce, iv, aes-gcm, chacha20-poly1305, xchacha20, aes-gcm-siv, aes-siv, birthday-bound, nonce-reuse, counter-mode, random-nonce, misuse-resistant-aead, deterministic-encryption]
level: advanced
status: docs-checked
description: "How to generate, size and track nonces/IVs for AES-GCM, ChaCha20-Poly1305 and AES-GCM-SIV so a key never sees a repeat: counters, random IVs, limits."
sources: ["https://csrc.nist.gov/pubs/sp/800/38/d/final", "https://www.rfc-editor.org/rfc/rfc8439", "https://www.rfc-editor.org/rfc/rfc8452"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nonce and IV management across AEAD modes

The one rule every AEAD mode shares: **a (key, nonce) pair must never be used
twice.** SP 800-38D calls IV uniqueness for GCM "almost as important as the
secrecy of the key", and RFC 8439 says nonce uniqueness is the critical
requirement for ChaCha20 as well.

## Pick the strategy by construction

- **AES-GCM, deterministic construction (SP 800-38D 8.2.1):** the IV is a
  fixed field identifying the device or context concatenated with an
  invocation field identifying the set of inputs. Distinct devices sharing a
  key must have distinct fixed fields.
- **AES-GCM, RBG-based construction (8.2.2):** the IV is a random field of at
  least 96 bits plus an optional free field (recommended empty, so the random
  field is the whole IV). The total number of invocations of the
  authenticated encryption function must not exceed 2^32 with the given key,
  across all IV lengths and instances. The same cap applies to a
  deterministic construction with IVs that are not 96 bits long.
- **ChaCha20-Poly1305:** the nonce is 96 bits and must differ for each
  invocation with the same key. RFC 8439 accepts counters and LFSRs as ways
  to generate unique nonces, and says a truncated encrypted counter is not
  acceptable with 128-bit or 256-bit block ciphers because it may repeat
  quickly.
- **AES-GCM-SIV (RFC 8452):** nonce misuse-resistant, so a repeated nonce does
  not fail catastrophically; the only security loss is that identical
  messages become visible. Use it if you cannot guarantee uniqueness (several
  uncoordinated writers sharing a key).

## Counters must survive restarts

SP 800-38D asks how the deterministic elements are recovered after a loss of
power; they could be kept in non-volatile memory. When power is restored,
neither the preceding IV nor any earlier IV may be repeated, for example by
storing the invocation value periodically so the stored value is always one
or more values ahead of the operational value.

## Multi-sender / multi-process systems

Under the deterministic construction, give every sender a distinct fixed
field. Do not let two senders share a key and pick nonces independently
without such a field: the limits above apply across all encryptions under the
key, not per sender.

## Storage and transmission

Store or send the IV with the ciphertext; it need not be secret. Watch for
truncation in serialization (for example a database column narrower than the
nonce).

## Verify

- [ ] For the chosen AEAD mode, state the nonce size and the max safe message
      count under one key, written down, not assumed.
- [ ] If nonces are random: a CSPRNG source, and the 2^32 invocation cap
      for AES-GCM is metered per key.
- [ ] If nonces are counters: the counter persists across restarts and the
      stored value runs ahead of the operational one.
- [ ] If uniqueness cannot be guaranteed: AES-GCM-SIV instead of plain GCM.
- [ ] Multi-sender systems: each sender has a distinct fixed field.

## Checked

Confirmed from SP 800-38D (PDF: IV uniqueness wording, Sec. 8.2.1 and 8.2.2 constructions, 96-bit random field minimum, 2^32 invocation limit and when it applies, power-loss guidance), RFC 8439 (96-bit nonce, uniqueness advice, counters and LFSRs, truncation warning) and RFC 8452 (repeated-nonce behaviour). Removed: the claim that SP 800-38D caps ChaCha20-Poly1305 (it covers GCM only), the 2^-32 collision probability remark, the XChaCha20 and AES-SIV sections, HKDF per-sender subkeys, the 2^28-2^30 alert thresholds and the soatok blog source (not read).

Method: docs-checked 2026-11-09 against SP 800-38D PDF, RFC 8439 and RFC 8452 text.

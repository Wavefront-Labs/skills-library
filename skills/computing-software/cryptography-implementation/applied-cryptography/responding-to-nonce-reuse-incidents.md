---
id: computing-software.cryptography-implementation.applied-cryptography.responding-to-nonce-reuse-incidents
name: responding-to-nonce-reuse-incidents
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, nonce-reuse-incident, nonce-reuse, aes-gcm, aes-ctr, chacha20-poly1305, forbidden-attack, incident-response, key-rotation, sp-800-38d]
level: advanced
status: docs-checked
description: "Triage and contain a CTR, GCM or ChaCha20-Poly1305 nonce-reuse bug: find affected keys, judge exposure, rotate keys, re-encrypt and fix the nonce source."
sources: ["https://csrc.nist.gov/pubs/sp/800/38/d/final", "https://www.rfc-editor.org/rfc/rfc8439", "https://www.rfc-editor.org/rfc/rfc8452"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Responding to a nonce-reuse incident

**Goal:** when a bug made a stream-cipher or AEAD reuse a (key, nonce) pair, establish the blast radius and recover
without guessing.

## What reuse actually breaks
| Mode | Reuse consequence |
|---|---|
| CTR / ChaCha20 (no MAC) | The keystream repeats, so the XOR of the ciphertexts equals the XOR of the plaintexts (RFC 8439). SP 800-38D notes that repeating counter blocks in counter mode may break confidentiality for the corresponding data blocks. |
| AES-GCM | SP 800-38D: if even one IV is ever repeated under a key, the implementation may be vulnerable to forgery attacks, and it calls IV uniqueness almost as important as key secrecy. Its discussion of the GCM forgery attack says repeated successes leak the hash subkey H, after which authentication assurance is completely lost. |
| ChaCha20-Poly1305 | RFC 8439: the one-time Poly1305 key and the keystream are identical between the two messages, which reveals the XOR of the plaintexts. |
| AES-GCM-SIV | RFC 8452: a repeated nonce only discloses whether the two messages were equal. |

Treat GCM reuse as an integrity compromise of the key, not just a confidentiality leak.

## Triage steps
1. **Find the bug window.** Commit that introduced the nonce source (fixed IV, counter reset on restart, random IV
   from a non-CSPRNG, nonce derived from a timestamp, shared counter across replicas) and the deploy dates.
2. **Measure actual collisions.** If ciphertexts store their nonce (they should), scan for duplicates per key:
   ```sql
   SELECT key_id, nonce, count(*) FROM blobs GROUP BY key_id, nonce HAVING count(*) > 1;
   ```
   Zero duplicates is still not "safe" if the RNG was broken; check the RNG output itself.
3. **Classify each affected key:** confidentiality exposure (which records share keystream), integrity exposure
   (for GCM assume forgeries are possible for anything that key verifies).
4. **Contain:** stop the encrypt path or hot-fix the nonce source first; then mark affected keys decrypt-only.

## Recovery
- Rotate every affected key: new key version, encrypt-only on the new key, re-encrypt stored data, then destroy the old
  key once nothing references it.
- For GCM keys used to authenticate inbound data (tokens, cookies, signed state), reject everything issued under the
  old key; forged items cannot be told apart from genuine ones.
- Fix the root cause structurally. RFC 8439 accepts counters and LFSRs as ways to generate unique nonces. SP 800-38D
  describes a deterministic construction (fixed field identifying the device plus an invocation field) and an RBG-based
  construction, and for the deterministic one says to keep the stored invocation value ahead of the operational value
  so a restart never repeats an IV. For writers that cannot coordinate, RFC 8452 specifies nonce misuse-resistant AES-GCM-SIV.
- Add a regression test that encrypts twice with the same key and asserts different nonces.

## Gotchas
- Counters stored in memory reset after restart or failover; counters in a DB row race across replicas.
- SP 800-38D also expects the system to monitor and limit unsuccessful verification attempts per key.

## Verify
- [ ] Duplicate-nonce query returns zero rows on the new key version.
- [ ] Old key is decrypt-only, then destroyed after re-encryption completes.
- [ ] Test asserts nonce uniqueness across restarts.

## Checked

Confirmed from SP 800-38D (PDF: IV-uniqueness requirement and forgery wording, deterministic and RBG-based constructions, power-loss counter advice, GCM forgery discussion, counter mode remark), RFC 8439 (nonce uniqueness advice and consequences of repetition) and RFC 8452 (repeated-nonce behaviour). The eprint 2016/475 source was not read and was dropped. Removed: the Joux "forbidden attack" attribution and that H is solved from two tagged messages, the Poly1305 forgery claim, the AES-SIV row, XChaCha20 192-bit nonces, VM snapshot replay and the nonce truncation advice, none of which was in the pages read.

Method: docs-checked 2026-11-09 against SP 800-38D PDF, RFC 8439 and RFC 8452 text.

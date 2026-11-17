---
id: computing-software.cryptography-implementation.key-management.key-overlap-windows-for-rotation
name: key-overlap-windows-for-rotation
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, key-overlap-window, key-rotation, jwks, kid, grace-period, signing-key-rollover, zero-downtime]
level: practitioner
status: draft
description: "Design accept-old, issue-new overlap windows for key rotation: publish before use, retire after max lifetime, for JWT signing keys, HMAC keys and data keys."
sources: ["https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final", "https://openid.net/specs/openid-connect-core-1_0.html#RotateSigKeys", "https://www.rfc-editor.org/rfc/rfc7517"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Key overlap windows for rotation

Zero-downtime rotation needs a period where verifiers accept both old and new keys, and an order of operations that
never leaves a producer using a key a consumer does not yet know.

## The three phases
1. **Publish:** distribute the new key to every verifier/decrypter (JWKS, config, KMS grant). Do not use it yet.
   Wait at least the longest cache TTL of any consumer.
2. **Switch:** producers start signing/encrypting with the new key. Verifiers accept both.
3. **Retire:** after the maximum lifetime of anything produced with the old key (token lifetime, cache, retention),
   remove the old key from verification. For decryption keys of stored data, retire only after re-encryption.

## Sizing the windows
| Artifact | Publish lead time | Retire after |
|---|---|---|
| JWT signing key | JWKS cache max-age (+ margin) | max token lifetime + clock skew |
| Session cookie MAC key | config rollout time | max session age |
| Webhook HMAC secret | partner confirms new secret | partner confirms switch |
| Data encryption key | n/a (key ID in ciphertext) | all data re-encrypted or expired |

## Implementation details
- Always carry a key identifier (`kid`, key version byte) in tokens and ciphertexts so verifiers do not try keys
  blindly.
- Verifiers hold a small set (current + previous + next), not an unbounded list.
- Automate the timeline; manual rotations miss the retire step and keep old keys alive forever.

## Gotchas
- Switching before publish propagates causes an outage in proportion to cache TTLs.
- Some JWT libraries cache JWKS indefinitely unless an unknown `kid` triggers a refresh; test that path.
- Overlap is not an excuse to skip revocation after compromise: then retire immediately and accept the outage.

## Verify
- [ ] Rotation drill in staging completes with zero auth failures.
- [ ] Old key is gone from verifiers after the retire date (checked automatically).

---
id: computing-software.cryptography-implementation.key-management.key-rotation-without-downtime
name: key-rotation-without-downtime
category: computing-software
field: cryptography-implementation
product: key-management
tags: [cryptography-implementation, key-management, key-rotation, key-versioning, dual-write, re-encryption, lazy-re-encryption, kid, key-id, backward-compatibility, zero-downtime, grace-period, signing-key-rollover]
level: advanced
status: docs-checked
description: "Rotate encryption/signing keys in a live system with zero downtime: key-id tagging, read-old/write-new grace periods, lazy vs batch re-encryption, and rollback safety."
sources: ["https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final", "https://cloud.google.com/kms/docs/key-rotation", "https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Key rotation without downtime

The naive approach — swap the key, redeploy — breaks every piece of data
encrypted or signed under the old key the moment the new key goes live. The
production-safe pattern separates "start using a new key for new data" from
"finish migrating old data" into two independently-scheduled phases.

## Tag every ciphertext/signature with the key id that produced it

This is the foundation everything else depends on. Prepend or attach a
**key id (`kid`)** — a short identifier, not the key itself — to every
encrypted blob, token, or signature: `kid || ciphertext` or a `kid` field in
a JSON envelope (JWTs do exactly this with the `kid` header). Without a
visible key id, you cannot know which key to use to decrypt/verify a given
piece of data once more than one key has ever been active — you're reduced
to trial-decrypting against every key you've ever had, which doesn't scale
and isn't guaranteed to even detect failure (wrong-key AEAD decrypt fails
loudly; wrong-key *signature* verify also fails loudly, but a non-AEAD
cipher might not).

## The rotation sequence

1. **Generate the new key, assign it a new `kid`.** Old key stays fully
   active for both read and write.
2. **Flip writes to the new key** (new encryptions/signatures use the new
   `kid`). Reads must now support **both** keys — this is the "dual-read"
   period and it has no fixed end date; it lasts as long as any data
   encrypted under the old key still exists and might be read.
3. **Re-encrypt old data under the new key**, by one of two strategies:
   - **Lazy re-encryption:** re-encrypt a record the next time it's read or
     written for any reason (decrypt with old key, re-encrypt with new,
     update `kid`). Zero batch job, but old-key data can linger
     indefinitely for cold records — acceptable only if you don't have a
     hard deadline to fully retire the old key.
   - **Batch re-encryption:** a background job walks all records tagged
     with the old `kid` and re-encrypts them. Needed when there's a
     compliance/security deadline to retire the old key (e.g., suspected
     compromise, crypto-period expiry per NIST SP 800-57). Rate-limit it —
     a full-table re-encrypt is a write-amplification event that can
     contend with production traffic.
4. **Retire the old key** only after confirming (via monitoring on `kid`
   usage in reads) that nothing is still being decrypted with it — pulling
   a key while live data still references it is an outage, not a rotation.
   Many KMS products support **disabling** a key (reversible) before
   **deleting** it (usually time-delayed and irreversible, e.g., AWS KMS's
   7–30 day pending-deletion window) — use the disable step as a canary: if
   nothing breaks for a soak period, deletion is safe.

## Signing keys need an additional grace window for verifiers

For signing (as opposed to encryption), the asymmetry is: verifiers need the
**new public key** available *before* you start signing with the new
private key, otherwise early-adopter signatures fail verification for
clients who haven't refreshed their key set yet. Standard pattern (same one
OAuth/OIDC JWKS endpoints use): publish the new public key alongside the old
one for a grace period, start signing with the new private key only after
verifiers have had time to pick up the new public key (poll interval +
margin), and only then retire the old public key from the published set.

## Automatic vs manual rotation

- **KMS-managed automatic rotation** (AWS KMS rotation of customer managed
  keys, Cloud KMS rotation schedules; Cloud KMS does not rotate asymmetric
  keys automatically) rotates the *key material* or creates a new key version
  while keeping the same key — the envelope-encryption pattern in
  `computing-software.cryptography-implementation.key-management.key-lifecycle-and-envelope-encryption`
  already isolates your application from this, since you're re-wrapping
  DEKs, not touching data directly.
- **Application-managed rotation** (you control the `kid` scheme yourself,
  e.g., for a signing key not stored in a KMS) needs all of the above done
  explicitly — nothing does it for you.

## Verify

- [ ] Every encrypted/signed artifact carries a `kid` that unambiguously
      identifies which key to use — no trial-decryption schemes.
- [ ] Reads support all keys still referenced by any live data; writes use
      only the current key.
- [ ] A re-encryption plan exists (lazy, batch, or both) with a defined
      completion check before old-key retirement.
- [ ] For signing keys: new public key published and given a verifier
      propagation window before the new private key starts signing.
- [ ] Old key disabled (reversible) and soaked before deletion
      (irreversible); `kid` usage monitored to confirm it's safe.

## Checked

2026-11-01. Confirmed in the AWS KMS "Rotate KMS keys" and "Deleting KMS keys" pages: rotation keeps the same KMS key, disabling is reversible, deletion needs a waiting period of 7 to 30 days and is irreversible. Confirmed in the Cloud KMS "Key rotation" page: rotation creates new key versions without re-encrypting data or disabling old versions, no automatic rotation for asymmetric keys, public key must be distributed before signing with a new asymmetric version. Removed the "annual" rotation claim. Design guidance (kid tagging, lazy vs batch) is process, not checkable.
Method: documentation only; no commands were run.

---
id: computing-software.cryptography-implementation.key-management.assessing-exposure-after-key-compromise
name: assessing-exposure-after-key-compromise
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, compromise-impact-assessment, key-compromise, incident-response, forward-secrecy, data-exposure]
level: advanced
status: draft
description: "Assess what data and systems a compromised key exposes: map key hierarchy and usage logs, determine time window, past versus future traffic, and notification scope."
sources: ["https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf", "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Assessing exposure after key compromise

## Questions to answer
1. **Which key and type?** Data-encryption, wrapping (exposes all keys it wrapped), signing (forgery, not
   disclosure), TLS (past traffic only if non-forward-secret key exchange).
2. **Window**: earliest possible compromise time to revocation/rotation time. Use access logs, repository
   history, and leak detection timestamps.
3. **Hierarchy**: every key derived from or wrapped by it. A KEK compromise plus access to wrapped DEKs exposes all
   data under those DEKs.
4. **Data reach**: query KMS/HSM audit logs (CloudTrail `Decrypt`, `GenerateDataKey`) and application logs for
   what was encrypted or signed in the window.
5. **Attacker access to ciphertext**: was the encrypted data also exposed (backups, buckets)?

## Specific cases
- TLS RSA key exchange (TLS 1.2 without ECDHE): recorded past sessions decryptable. ECDHE/TLS 1.3: past
  sessions safe, future impersonation possible until revocation.
- Signing key: identify artifacts signed in the window; anything signed after the earliest compromise time is
  suspect (code signing, tokens).
- JWT HMAC secret: forged tokens possible; revoke sessions.

## Output
Written assessment: key, window, derived keys, datasets, records count, regulatory notification triggers, and
rekey/re-encrypt actions.

## Verify
- [ ] Assessment reviewed with legal/privacy; re-encryption or re-signing completed and tracked.

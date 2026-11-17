---
id: computing-software.cryptography-implementation.key-management.key-compromise-response-plan
name: key-compromise-response-plan
category: computing-software
field: cryptography-implementation
product: key-management
tags: [cryptography-implementation, key-management, key-compromise, key-compromise-response, incident-response, revocation, sp-800-57, certificate-revocation, re-encryption, runbook]
level: advanced
status: draft
description: "Write and run a key compromise runbook per SP 800-57 Pt1 5.5: classify by key type, contain, rotate, revoke, assess what the key protected, and notify relying parties."
sources: ["https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final", "https://csrc.nist.gov/pubs/sp/800/57/pt2/r1/final", "https://cabforum.org/working-groups/server/baseline-requirements/requirements/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Key compromise response plan

SP 800-57 Pt1 5.5: the impact of a compromised key depends on its type and
what it protected; the plan must exist before the incident. Write one runbook
section per key class.

## Impact by key type

| Key | Attacker can | Response focus |
|---|---|---|
| Signing private key (code, CA, JWT) | Forge signatures from now on | Revoke/rotate, publish new trust anchor, find forged artifacts |
| TLS server private key | Impersonate server; decrypt past traffic only if RSA key exchange (no FS) | Revoke cert (24h CA/B deadline for key compromise), reissue with new key |
| Symmetric data key / KEK | Decrypt everything under it; forge AEAD ciphertexts | Rotate, re-encrypt, assess data exposure |
| Key-agreement static key | Decrypt sessions/messages to that key without FS | Rotate, assess stored ciphertexts |
| MAC/HMAC/webhook secret | Forge authenticated messages | Rotate, audit accepted messages |
| Password-hash pepper | Offline cracking becomes possible | Rotate pepper on next login, force resets if hashes also leaked |

## Runbook steps

1. **Declare and scope**: which key ids/versions, since when (earliest
   possible exposure), how detected.
2. **Contain**: disable the key in KMS/HSM (`aws kms disable-key`), revoke
   IAM access, block the leaked credential path. Disabling a decrypt key can
   cause an outage; decide who can authorise that trade-off, in advance.
3. **Replace**: generate a new key (new key id), deploy, switch encryption and
   signing to it. Keep the old key decrypt-only or verify-only if needed for
   existing data, unless the attacker can abuse that (signing keys: no).
4. **Revoke**: certificates (CA `revoke` with reason `keyCompromise`), JWKS
   (remove the kid), SSH CA KRL, PGP revocation certificate, package signing
   key revocation notices.
5. **Remediate data**: re-encrypt data under the new key; re-sign artifacts
   that must stay valid; invalidate tokens/sessions signed with the old key.
6. **Assess**: what was protected during the exposure window; legal/privacy
   notification duties.
7. **Notify relying parties**: customers who pinned or trusted the key.
8. **Post-incident**: how it leaked; fix the storage weakness.

## Preparation checklist

- Inventory maps each key to owner, data/systems it protects, and rotation
  procedure.
- Rotation has been rehearsed for each key class (see recovery drill skill).
- Revocation contacts and CA account access work out of hours.
- Pre-generated revocation certificates (PGP) stored offline.

## Verify

- [ ] Runbook has a section per key class with owner and rotation commands.
- [ ] Time-to-rotate measured in a drill for the top three critical keys.
- [ ] Old key versions can be disabled without code changes.

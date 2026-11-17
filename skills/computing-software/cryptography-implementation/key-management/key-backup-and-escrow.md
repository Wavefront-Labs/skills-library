---
id: computing-software.cryptography-implementation.key-management.key-backup-and-escrow
name: key-backup-and-escrow
category: computing-software
field: cryptography-implementation
product: key-management
tags: [cryptography-implementation, key-management, key-recovery, key-backup, key-escrow, sp-800-57, hsm-backup, kms-import, offline-backup, which-keys-to-back-up]
level: advanced
status: docs-checked
description: "Decide which keys to back up (SP 800-57 Pt1 Table 7: encryption keys OK, signing keys generally no), how to back them up securely, and how escrow differs from backup."
sources: ["https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Key backup and escrow

Losing a decryption key loses the data; backing up a signing key widens who can
forge. SP 800-57 Part 1 Rev 5 section 8.2.2 and Tables 7 and 8 tell you which
keys to back up. Not all keys need backup: if operations can continue by
re-keying, it may be preferable not to save the key, to reduce compromise risk.

## Which keys (Table 7; "OK" means permitted, not required)

| Key type | Back up? | Reason |
|---|---|---|
| Symmetric data encryption key | OK | Needed to decrypt stored data |
| Symmetric key-wrapping key (KEK) | OK | Needed to unwrap stored keys |
| Private key-transport key | OK | Needed to recover transported keys |
| Private static key-agreement key | OK | Final decision is application-specific |
| Private signature key | No (in general) | Non-repudiation would be in question; a CA's private signing key may warrant backup, stored under the owner's control |
| Public signature-verification key | OK | A certificate available elsewhere may be enough |
| Private ephemeral key-agreement key | No | Never needs recovery |
| RBG seed, shared secret, intermediate results (Table 8) | No | |
| Key metadata (IDs, purpose) (Table 8) | OK | |

The final decision depends on the application.

## How to back up

- Backups need the storage protection of section 6.2.2 and independent,
  secure media. Keep backed-up keys at least as long as the key is in
  operational use; then remove them and destroy all traces per section 8.3.4.
- Software keys: wrap under an offline KEK or split with a secret-sharing
  scheme, and store in physically separate locations. Never a plain file in
  the same backup set as the data.
- Managed HSM/KMS services have vendor-specific backup and deletion
  controls: read the vendor's documentation for restore scope and deletion
  waiting periods, and test a restore.

## Escrow versus backup

Backup protects the owner against loss. Escrow gives a third party (company
security, regulator) the ability to recover. Escrow of signing keys defeats
non-repudiation (SP 800-57 on private signature keys), so do not.

## Metadata to keep with each backup

Key id, algorithm, purpose, creation date, cryptoperiod end, which data it
protects, custodians, backup date, location. Table 8 lists key-control
information as OK to back up. Without it, a restored key is a mystery blob.

## Verify

- [ ] Inventory marks every key as back-up/no-back-up per the table above.
- [ ] Signing keys are not in backups (other than an approved CA exception under owner control).
- [ ] A restore into a clean environment has been tested.
- [ ] Key deletion is guarded by a waiting period and restricted permission.

## Checked

2026-11-01. Confirmed against SP 800-57 Pt1 Rev 5 section 8.2.2, 8.2.2.1
(Tables 7 and 8, "OK" meaning, backup retention and destruction, section 6.2.2
storage). Corrected: the description cited Table 9, which is the archive table;
backup is Table 7. Removed: Luna, nShield and AWS CloudHSM behaviour, KMS
multi-region and SCP details, "strict dual control" for CA roots, the 12-month
restore cadence, the OWASP and AWS CloudHSM sources.

Method: documentation only; no commands were run.

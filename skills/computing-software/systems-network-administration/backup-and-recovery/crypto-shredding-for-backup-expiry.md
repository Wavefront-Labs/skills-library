---
id: computing-software.systems-network-administration.backup-and-recovery.crypto-shredding-for-backup-expiry
name: crypto-shredding-for-backup-expiry
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [crypto-shredding, cryptographic-erasure, key-destruction, gdpr-erasure, backup-retention]
level: advanced
status: docs-checked
description: "Use crypto-shredding to make backup data unrecoverable by destroying keys: per-dataset keys, erasure requests vs immutable backups, and KMS key deletion."
sources:
  - https://csrc.nist.gov/pubs/sp/800/88/r2/final
  - https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/right-to-erasure/
  - https://docs.aws.amazon.com/kms/latest/developerguide/deleting-keys.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Crypto-shredding for backup expiry

**Idea:** if each dataset or period is encrypted with its own key, destroying the key renders every copy of that data (tapes, off-site, immutable object storage) unreadable at once.

## Uses
- **Expiry of immutable or offline media**: tapes in a vault or compliance-locked objects cannot be deleted early, but their key can.
- **Right to erasure** (UK GDPR): the ICO says a valid erasure request with no exemption applies to backup systems as well as live systems, with steps depending on your circumstances, retention schedule and technical mechanisms. Data may remain in backups until overwritten; the key issue is putting it "beyond use" (not used for any other purpose, held only until replaced on an established schedule), and being absolutely clear with the individual about what happens to their data in backups. Whether that is enough is context specific; per-subject keys are one way to make real erasure possible. Take legal advice.
- **Media disposal**: NIST SP 800-88 (Guidelines for Media Sanitization) lists cryptographic erase among its sanitization methods. Rev. 1 was withdrawn on 26 September 2025 and superseded by Rev. 2, so read Rev. 2 for the requirements.

## Design
- Key granularity: per backup set/month (simple, coarse), per tenant/customer (multi-tenant SaaS), per data subject (application layer, complex).
- Keys in a KMS or HSM; destruction through a scheduled deletion with a waiting period and your own dual approval; keep logs as evidence. In AWS KMS the waiting period is 7 to 30 days (default 30, up to 24 hours longer), the key is Pending deletion meanwhile and deletion can be cancelled, and deletion is irreversible once the period ends. Scheduling deletion might not immediately affect data keys already generated, so check how your service uses data keys.
- Ensure no other copy of the key exists: KMS backups, escrow envelopes, exported key files. Shredding fails if a backup of the KMS still holds the key; align KMS backup retention.

## Procedure
1. Identify the key(s) for the datasets to expire.
2. Confirm no legal hold applies and no needed data shares the key.
3. Schedule deletion, wait out the period, confirm destruction, record evidence of destruction.
4. Mark the media/backups as unrecoverable in the catalog.

## Gotchas
- Shared keys across years make selective shredding impossible; plan key rotation by period from the start.
- Plaintext copies elsewhere (exports, test restores) are not covered.

## Verify
Attempt a restore of a shredded set in a test: decryption fails; audit trail shows the key deletion event and approvals.

## Checked

2026-11-09. Confirmed against the ICO right-to-erasure guidance (backups in scope, "beyond use", be clear with individuals, context specific), the AWS KMS "Delete KMS keys" page (7 to 30 day waiting period, default 30, Pending deletion, cancel, irreversible, data-key caveat) and the NIST SP 800-88 landing pages (Rev. 1 withdrawn 2025-09-26, superseded by Rev. 2; cryptographic erase listed as a keyword). Partial read: the NIST pages are catalogue entries, not the PDF, so no NIST requirements are stated. Removed: "regulators generally accept", "erasure re-applied if a restore happens" and the claim that NIST recognises crypto erase under stated conditions.

Method: documentation only; no commands were run.

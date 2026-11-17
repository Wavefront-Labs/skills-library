---
id: computing-software.cryptography-implementation.key-management.key-destruction-evidence-and-records
name: key-destruction-evidence-and-records
category: computing-software
field: cryptography-implementation
product: key-management
tags: [cryptography-implementation, key-management, key-destruction, key-destruction-record, audit-evidence, sp-800-57, sp-800-88, zeroization, compliance]
level: practitioner
status: draft
description: "Produce destruction evidence for keys: what to record, covering every copy (backups, escrow, HSM clones), KMS and HSM log events, and retention."
sources: ["https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final", "https://csrc.nist.gov/pubs/sp/800/88/r1/final", "https://docs.aws.amazon.com/kms/latest/developerguide/ct-deletekey.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Key destruction evidence and audit records

Auditors (PCI DSS 3.6/3.7, ISO 27001, FIPS-based policies) ask you to prove
a key was destroyed and that no copy survives. The destruction itself is
easy; the evidence is the work.

## Record per destruction

- Key identifier, version, algorithm, purpose, classification.
- Reason (end of cryptoperiod, compromise, decommission, erasure request).
- Authorisation: approver(s), ticket id; dual control for high-value keys.
- Method: KMS deletion, HSM zeroisation command, physical destruction of
  smart cards/tokens, media sanitisation per SP 800-88.
- **Every copy** and its fate: primary, HSM cluster members, HSM backups,
  escrow, offline backups, key-share holders, test environments.
- Date/time, operator, witness.
- Confirmation evidence (log event ids, screenshots for offline steps,
  signed certificate of sanitisation for media).

## Machine evidence

- AWS KMS: CloudTrail `ScheduleKeyDeletion` (who, when) and the `DeleteKey`
  event KMS emits when deletion completes.
- GCP: `DestroyCryptoKeyVersion` admin activity log and the version state
  `DESTROYED`.
- HSMs: audit log entries for object deletion or zeroisation; export and
  sign them.
- Vault transit: `deletion_allowed` change and key delete in audit device logs.

## Keep

- The record (not the key) for the retention period your policy sets,
  usually as long as data protected by the key might be questioned.
- Metadata of destroyed keys stays in the inventory with state `Destroyed`.

## Pitfalls

- Destroying the KMS key but forgetting a plaintext export in an escrow safe.
- Key shares held by people who left; collect or confirm destruction.

## Verify

- [ ] Destruction template covers all copies and requires approver and witness.
- [ ] Sample of last year's destroyed keys each has a complete record with log ids.

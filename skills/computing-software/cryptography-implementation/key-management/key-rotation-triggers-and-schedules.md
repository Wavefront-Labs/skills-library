---
id: computing-software.cryptography-implementation.key-management.key-rotation-triggers-and-schedules
name: key-rotation-triggers-and-schedules
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, rotation-schedule, key-rotation, cryptoperiod, rotation-triggers, kms-rotation, pci-dss, offboarding]
level: practitioner
status: docs-checked
description: "Set rotation schedules and event triggers per key type: cryptoperiods, volume limits, staff departure, compromise suspicion, algorithm deprecation and KMS settings."
sources: ["https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Key rotation triggers and schedules

## Scheduled rotation
Take per-key-type cryptoperiods from NIST SP 800-57 Part 1 (the PDF and page were not readable for this review, so no
figures are given here) and your own policy. Shorten for high volume, broad exposure, or weak protection. Rotate TLS
server keys at each certificate renewal.

## Event triggers (rotate now, not on schedule)
- Suspected or confirmed compromise (revoke, do not overlap).
- A person with access to plaintext key material leaves or changes role (for keys they could export: secrets, PEM
  files, shared passwords; not for non-exportable KMS/HSM keys they only used).
- Usage limits approaching (message/byte counters).
- Algorithm or key size deprecated.
- Infrastructure change: key moved between environments, copied to a less trusted system, or exposed in logs.

## Cloud KMS settings
- AWS KMS: `aws kms enable-key-rotation --key-id <id> --rotation-period-in-days 365` (90-2560 days); on-demand
  `aws kms rotate-key-on-demand`. Automatic and on-demand rotation exist only for customer managed keys; for
  asymmetric and HMAC keys and keys in custom key stores, rotate manually by creating a new key and moving the alias.
- GCP: `gcloud kms keys update KEY --rotation-period 90d --next-rotation-time ...`.

## Gotchas
- KMS key rotation does not rotate data keys or re-encrypt data, and does not mitigate a compromised data key.
- Rotating a key without the ability to re-encrypt stored data only limits future exposure.
- Track rotation as evidence (AWS: CloudTrail, `GetKeyRotationStatus`, `ListKeyRotations`); calendar reminders are not evidence.

## Checked

2026-10-31. Confirmed in the AWS KMS rotation page (customer managed keys only, manual rotation for asymmetric, HMAC and custom key store keys, no re-encryption, GetKeyRotationStatus and ListKeyRotations) and the AWS KMS API model (rotation period 90-2560 days). Commands passed check_commands. Removed: the SP 800-57 table, 47-day certificate claim, SP 800-131A and IR 8547, PCI requirement number, imported-material claim and Azure lifetimeActions (not confirmable from readable pages).

Method: documentation only; no commands were run.

## Verify
- [ ] Each inventory row has schedule and triggers.
- [ ] Offboarding checklist includes key and secret rotation steps.

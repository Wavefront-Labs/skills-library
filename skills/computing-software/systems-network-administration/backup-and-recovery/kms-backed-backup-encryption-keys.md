---
id: computing-software.systems-network-administration.backup-and-recovery.kms-backed-backup-encryption-keys
name: kms-backed-backup-encryption-keys
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [kms-backup-keys, kms, kmip, key-management, envelope-encryption, aws-kms]
level: advanced
status: docs-checked
description: "Use a KMS for backup encryption keys: KMIP, cloud KMS with envelope encryption, key access policy, scheduled key deletion and availability in DR."
sources:
  - https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html
  - https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html
  - https://docs.aws.amazon.com/kms/latest/developerguide/deleting-keys.html
  - https://docs.oasis-open.org/kmip/kmip-spec/v2.1/kmip-spec-v2.1.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# KMS-backed backup encryption keys

## Why
Passwords typed into backup jobs get lost, reused or stored in the same system an attacker owns. A KMS centralises keys, can log key use and enforces who may decrypt.

## Patterns
- **Envelope encryption**: data is encrypted with data keys; data keys are encrypted (wrapped) by a KMS key, often called a wrapping or key-encryption key. AWS KMS notes that wrapping keys are used far less often than data keys. Losing access to the wrapping key makes the wrapped data keys, and so the backups, unreadable. That is both the protection and the risk.
- **KMIP**: the Key Management Interoperability Protocol is an OASIS standard (the cited spec is v2.1) for talking to key management servers. Whether a backup product can use a KMIP server, and how, is product-specific; read that product's documentation before relying on it.
- **Cloud KMS**: for cloud-native backups, use the provider's KMS with customer managed keys, for example AWS KMS.

## Policy
- Separation of duties: backup admins can run jobs but not delete or disable keys; KMS admins cannot read backups.
- Key deletion is destructive and irreversible. AWS KMS requires a waiting period of 7 to 30 days (default 30; the actual wait can be up to 24 hours longer), during which the key is Pending deletion and deletion can be cancelled. Add your own dual approval, and consider a CloudWatch alarm for use of a key during the wait.
- Rotation: AWS KMS rotation keeps old key material so existing ciphertext still decrypts, but it does not re-encrypt data or rotate the data keys already generated.

## DR availability
The KMS must be reachable at the recovery site, including in a cyber vault scenario where production is compromised: plan replication or recovery of the KMS across sites, back up the KMS itself, and keep a break-glass recovery procedure offline.

## Verify
Restore test at the DR site with the primary KMS unreachable succeeds via the replica or recovery path; the KMS audit log shows the decrypt calls.

## Checked

2026-11-09. Confirmed against AWS KMS "Rotate KMS keys" (wrapping keys, rotation does not re-encrypt data or rotate data keys, old material kept for decrypt), "Delete KMS keys" (7 to 30 day waiting period, default 30, up to 24 hours longer, Pending deletion, cancel, CloudWatch alarm) and the KMIP v2.1 spec (OASIS). Read only the opening sections of the large KMIP spec and the AWS KMS "concepts" page headings; no KMIP product claims are made. Removed: named KMIP vendors, Veeam v12 KMS integration steps and port 5696, Azure Key Vault and Google Cloud KMS claims, "AWS Backup vaults" and "Azure Backup CMK" claims (not on cited pages).

Method: documentation only; no commands were run.

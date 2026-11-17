---
id: computing-software.cybersecurity-defensive.cloud-security.aws-backup-vault-lock
name: aws-backup-vault-lock
category: computing-software
field: cybersecurity-defensive
product: cloud-security
tags: [backup-vault-lock, aws-backup, worm-backups, logically-air-gapped-vault, ransomware-recovery, cross-account-backup, cloud-data-protection]
level: practitioner
status: docs-checked
description: "Protect AWS backups from deletion with Backup Vault Lock: governance vs compliance mode, grace time, logically air-gapped vaults, restore testing."
sources: ["https://docs.aws.amazon.com/aws-backup/latest/devguide/vault-lock.html", "https://docs.aws.amazon.com/aws-backup/latest/devguide/logicallyairgappedvault.html", "https://docs.aws.amazon.com/aws-backup/latest/devguide/restore-testing.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS Backup Vault Lock

Attackers with admin access delete backups before encrypting/destroying data. Vault Lock makes recovery
points WORM-like: AWS Backup denies deletes and lifecycle changes in a locked vault, even for the root user.

## Modes
| Mode | Behaviour |
|---|---|
| Governance | Users with sufficient IAM permissions can manage the lock or delete the vault - good for testing |
| Compliance | Has a cooling-off "grace time" (at least 3 days / 72 hours); until it ends you can still remove or change the lock; after it, the vault and its lock are immutable and cannot be changed or deleted by any user or by AWS |

Create via the `PutBackupVaultLockConfiguration` API. Include `ChangeableForDays` only for compliance
mode; omit it for governance mode. `MinRetentionDays` and `MaxRetentionDays` are optional.
```
aws backup put-backup-vault-lock-configuration --backup-vault-name <VAULT_NAME> \
  --min-retention-days 7 --max-retention-days 30 --changeable-for-days 3
```
Each vault can have one vault lock.

## Architecture
- **Logically air-gapped vault**: encrypted with an AWS owned key by default (or optionally a customer
  managed KMS key), always locked in compliance mode, and its backups can be shared through AWS RAM or
  MPA with another account and restored there.

## Restore testing
AWS Backup **restore testing** restores selected recovery points on a schedule; optional validation
confirms the result, and AWS Backup then deletes the test resources.

## Gotchas
- Compliance mode is irreversible once grace time ends: backups cannot be deleted until their lifecycle
  completes, so avoid recovery points with an "Always" retention - they are retained forever.
- Retention periods set at backup creation are independent of the vault lock min/max settings.

## Verify
- [ ] Attempt to delete a recovery point in the locked vault is denied.
- [ ] A restore test job succeeded recently.

## Checked
2026-11-01. Confirmed on the AWS Backup Developer Guide pages for Vault Lock, logically air-gapped vaults
and restore testing: modes, 3-day minimum grace time, ChangeableForDays semantics, root-user denial, one lock per
vault, air-gapped vault key and RAM/MPA sharing, restore testing validation and cleanup. The CLI command passes the
model check. Removed (not stated on those pages): the named IAM action in governance mode, SCP actions, cross-account
copy and KMS sharing detail, plan-write failure behaviour, the source/backup-plan deletion gotcha, Lambda validation
hooks wording.
Method: documentation only; no commands were run.

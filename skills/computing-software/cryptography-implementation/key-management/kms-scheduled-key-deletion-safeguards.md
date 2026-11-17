---
id: computing-software.cryptography-implementation.key-management.kms-scheduled-key-deletion-safeguards
name: kms-scheduled-key-deletion-safeguards
category: computing-software
field: cryptography-implementation
product: key-management
tags: [cryptography-implementation, key-management, key-destruction, scheduled-key-deletion, aws-kms, gcp-kms, azure-key-vault, soft-delete, purge-protection]
level: practitioner
status: docs-checked
description: "Delete KMS keys without destroying data by accident: disable first, waiting periods, alarms on use during pending deletion, IAM guards and purge protection."
sources: ["https://docs.aws.amazon.com/kms/latest/developerguide/deleting-keys.html", "https://cloud.google.com/kms/docs/destroy-restore", "https://learn.microsoft.com/en-us/azure/key-vault/general/soft-delete-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KMS scheduled key deletion safeguards

Deleting a KMS key makes every ciphertext under it permanently
unrecoverable. Cloud KMSs add a waiting period; use it deliberately.

## Procedure

1. **Find dependants**: CloudTrail/Cloud Audit Logs for Decrypt/Encrypt/
   GenerateDataKey with this key over at least the longest data retention
   cycle (monthly jobs, yearly reports). Check grants, aliases, EBS/RDS/S3
   default encryption settings.
2. **Disable first** (`aws kms disable-key`) for weeks; anything that breaks
   tells you it was still needed. A disabled key can be re-enabled, and a scheduled deletion cancelled, but a deleted key cannot be recovered.
3. **Schedule deletion** with the maximum waiting period (AWS: 7-30 days).
4. **Alarm** on any attempted use during the window.
5. Let it complete; record the destruction.

## Platform specifics

| Platform | Mechanism |
|---|---|
| AWS KMS | `schedule-key-deletion --pending-window-in-days 7..30` (default 30; the real wait can run up to 24 hours longer); `cancel-key-deletion`. A key in Pending deletion cannot be used in cryptographic operations; AWS suggests a CloudWatch alarm for attempted use. A multi-Region primary can be deleted only after its replicas, and its waiting period starts when the last replica is deleted. Public keys of an asymmetric key already shared outside KMS keep encrypting, undetected by such alarms. |
| GCP Cloud KMS | Destroying a version schedules it (default scheduled-for-destruction duration 30 days; a custom duration can be set at key creation, and an organization policy can set a minimum); `gcloud kms keys versions restore` cancels. |
| Azure Key Vault | Soft delete (7-90 days, default 90) plus **purge protection** prevents purging before retention ends, until the retention period passes. Enable purge protection on production vaults. |

## IAM guards

- Deny scheduling or purging key deletion (AWS key-deletion actions, Cloud KMS version destroy, Key Vault purge) to all but a break-glass role; require two-person approval.
- Key policies should not grant deletion to application roles.
- Imported AWS key material can be removed with `DeleteImportedKeyMaterial` (reversible by reimporting); restrict it equally.

## Checked

2026-10-31. Confirmed against the AWS KMS deleting-keys page (7-30 day wait, default 30, up to 24 hours longer, Pending deletion, multi-Region and imported-material rules), the Cloud KMS destroy-restore page (30 day default, custom duration at creation) and the Key Vault soft-delete page (7-90 days, default 90, purge protection). Removed: GCP 24 h to 120 days range, the exception name, specific IAM action names, "even by admins".
Method: documentation only; no commands were run.

## Verify

- [ ] Alarm fires in a test when a pending-deletion key is used.
- [ ] Only break-glass principals can schedule deletion (policy simulator).
- [ ] Azure vaults have purge protection on.

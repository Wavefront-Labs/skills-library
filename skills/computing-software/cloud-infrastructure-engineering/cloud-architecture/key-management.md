---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.key-management
name: key-management
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, data-protection, key-management, kms, customer-managed-keys, byok, hyok, external-key-manager, envelope-encryption, key-rotation, key-policies, hsm]
level: advanced
status: draft
description: "Design encryption key management: provider-managed vs customer-managed vs BYOK/HYOK/external keys, key hierarchy per data domain, rotation, access separation and deletion safety."
sources: ["https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html", "https://learn.microsoft.com/azure/security/fundamentals/key-management", "https://cloud.google.com/kms/docs/ekm", "https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Key management and BYOK / HYOK

## Options (increasing control and operational burden)
1. **Provider-managed keys** (default encryption at rest): zero effort, no separate access control.
2. **Customer-managed keys (CMK) in KMS** (AWS KMS, Azure Key Vault/Managed HSM, Cloud KMS):
   you control key policy, rotation, disable/delete; access to data requires both data and key permissions.
3. **BYOK**: you generate key material in your HSM and import it — proves provenance; you must
   keep a copy and manage expiry.
4. **HYOK / external key manager**: keys stay outside the provider (AWS KMS External Key Store,
   Google Cloud EKM, Azure Managed HSM / double key encryption) — provider can't decrypt without
   your system; your key service's availability becomes the data's availability.

## Design
- Envelope encryption: data keys encrypt data; KMS keys encrypt data keys.
- **Key per data domain/classification and environment** (not one key for everything, not one per object).
- **Separation of duties**: key administrators can't use keys for decryption; workload roles can
  use but not administer. Least-privilege key policies + grants.
- **Rotation**: automatic rotation of KMS keys (AWS yearly by default when enabled, configurable
  period; Azure Key Vault rotation policies; Cloud KMS rotation schedule). Old versions remain for decryption.
- **Deletion safety**: scheduled deletion windows (AWS 7-30 days), alarms on `ScheduleKeyDeletion`
  and disable events — deleting a key destroys all data it protects, including backups.
- Multi-region keys / replicated keys for DR copies.
- Log all key usage (CloudTrail, Key Vault diagnostic logs, Cloud Audit Logs data access).

## Verify
- [ ] Key inventory: owner, domain, rotation status, policies reviewed.
- [ ] Alerts on key disable/schedule-deletion.
- [ ] DR region can decrypt restored backups.

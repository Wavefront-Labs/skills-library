---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.isolated-recovery-environment
name: isolated-recovery-environment
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, disaster-recovery, isolated-recovery-environment, cyber-recovery, immutable-backups, ransomware-recovery, clean-room]
level: practitioner
status: draft
description: "Build an isolated recovery environment for cyber recovery: separate account and identity, immutable vaulted backups, clean-room restore, malware scanning and drills."
sources: ["https://www.ncsc.gov.uk/collection/principles-for-ransomware-resistant-cloud-backups", "https://docs.aws.amazon.com/aws-backup/latest/devguide/logicallyairgappedvault.html", "https://learn.microsoft.com/azure/backup/backup-azure-immutable-vault-concept", "https://cloud.google.com/backup-disaster-recovery/docs/concepts/backup-vault"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Isolated recovery environment for cyber recovery

## Steps
1. **Separate trust domain**: dedicated account/subscription/project, ideally under a separate
   organisation or tenant, with its own identities and MFA; no federation trust from the
   production IdP that an attacker could already own.
2. **Immutable vaulted copies**: AWS Backup logically air-gapped vault or vault lock in
   compliance mode, Azure Backup immutable vault (locked), Google Backup vault with enforced
   retention; S3 Object Lock compliance mode for custom copies. Retention longer than typical
   attacker dwell time.
3. **Restricted deletion**: retention changes require multi-party approval (Azure
   Multi-User Authorization, Resource Guard; AWS restore-testing roles separate from admin).
4. **Clean-room restore**: network-isolated VPC/VNet with no route to production; restore
   there, scan with updated EDR/AV, check for persistence (accounts, scheduled tasks), rebuild
   identity before reconnecting.
5. **Minimum viable company**: define which systems restore first (identity, DNS, core apps)
   and their order.
6. **Drill** at least yearly: full restore into the IRE, time it, and verify integrity.

## Gotchas
- Backups encrypted with keys in the compromised account are unrecoverable if keys are deleted.
- Restoring straight into production reinfects; always restore and scan in isolation first.

## Verify
- [ ] Vault lock or immutability verified (deletion attempt fails).
- [ ] Clean-room restore drill timed and documented.

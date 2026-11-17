---
id: computing-software.systems-network-administration.backup-and-recovery.azure-backup-vaults-and-soft-delete
name: azure-backup-vaults-and-soft-delete
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [azure-backup, recovery-services-vault, soft-delete, immutable-vault, multi-user-authorization, cross-region-restore, cloud-backup]
level: advanced
status: docs-checked
description: "Protect Azure workloads with Azure Backup: vault types, standard vs enhanced VM policies, soft delete, immutable vaults, multi-user authorization, cross-region restore."
sources:
  - https://learn.microsoft.com/en-us/azure/backup/backup-overview
  - https://learn.microsoft.com/en-us/azure/backup/secure-by-default
  - https://learn.microsoft.com/en-us/azure/backup/backup-azure-vms-enhanced-policy
  - https://learn.microsoft.com/en-us/azure/backup/backup-azure-backup-faq
  - https://learn.microsoft.com/en-us/azure/backup/backup-azure-immutable-vault-concept
  - https://learn.microsoft.com/en-us/azure/backup/multi-user-authorization-concept
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure Backup vaults and soft delete

**Goal:** backups of Azure VMs, databases, files and on-premises machines that survive accidental deletion and a compromised admin.

## Vault types
- **Recovery Services vault**: Azure VMs, SQL/SAP HANA in VMs, Azure Files, MARS agent (files/folders on Windows), MABS/DPM.
- **Backup vault**: newer workloads (Azure Disks, Blobs, Azure Database for PostgreSQL servers, Kubernetes services in preview, per the Azure Backup FAQ).
Set storage redundancy (LRS/ZRS/GRS) before configuring the first backup; the option is disabled afterwards. **Cross Region Restore** is a separate vault setting supported only for Recovery Services vaults that use GRS.

## VM policies
- **Standard**: does not protect newer offerings such as Ultra Disk and Premium SSD v2.
- **Enhanced**: multiple backups per day (as often as every 4 hours), supports Trusted Launch VMs, Premium SSD v2 and Ultra Disks, and 1 to 30 days of instant-restore snapshot retention (the maximum shrinks as snapshot frequency rises). Trusted Launch VMs on the Standard policy are possible only through the Azure CLI (2.73.0+), PowerShell (Az 14.0.0+) or REST API (2025-01-01+).
```bash
az backup protection enable-for-vm --resource-group rg-prod --vault-name rsv-prod --vm app01 --policy-name EnhancedPolicy-4h
az backup job list --resource-group rg-prod --vault-name rsv-prod -o table
```

## Soft delete
Microsoft now enforces soft delete by default ("secure by default"): deleted backup items, recovery points and vaults stay recoverable for 14 days by default, configurable from 14 to 180 days. No charge applies for the first 14 days, and you pay for any period beyond. In regions where this is enforced you cannot disable soft delete or change its state in the portal; for Backup vaults outside Australia East, West Central US and East Asia the documentation says you can still disable it. The Azure CLI exposes the state and duration for Recovery Services vaults:
```bash
az backup vault backup-properties set --name rsv-prod --resource-group rg-prod --soft-delete-feature-state AlwaysOn --soft-delete-duration 30
```

## Immutable vault
Blocks operations that could lose recovery points, and applies to Recovery Services vaults and Backup vaults. Enabling is reversible until you **lock** it; locking is irreversible and puts backups on WORM storage. By default recovery points are immutable for as long as the backup policy retains them; alternatively set a specific duration, and policy retention cannot then be reduced below it.

## Multi-user authorization (MUA)
Protect critical operations (such as disabling soft delete) with a **Resource Guard**, owned by a different user and ideally placed in a different subscription or tenant. The backup admin must not hold Contributor, Backup MUA Admin or Backup MUA Operator on the guard; the security admin temporarily grants Backup MUA Operator to approve an operation.

## At scale
Azure Policy definitions can auto-configure backup on VMs with or without a given tag, to an existing or new Recovery Services vault. Backup center is the legacy at-scale experience; Microsoft is transitioning it to Resiliency.

## Gotchas
- Change vault storage redundancy before the first backup; afterwards the option is disabled (the docs list workarounds).
- Deleting a VM does not delete its backups; stop protection explicitly and watch costs.

## Verify
The backup reporting view (Resiliency or Backup center) shows all production VMs protected with successful jobs, soft delete enabled, and MUA enforced for the vault.

## Checked

Checked 2026-10-27 against the current Azure Backup articles in MicrosoftDocs/azure-docs (secure-by-default dated 14 Aug 2026, enhanced soft delete configure/manage, enhanced VM policy, immutable vault, multi-user authorization, create Recovery Services vault, Backup vault overview, FAQ, Backup center overview and auto-enable policies) and the Azure CLI backup module source (Azure/azure-cli). Confirmed: soft delete is enforced by default with 14 to 180 days retention and charges only beyond 14 days, vault-type datasource lists, Enhanced policy frequency and Trusted Launch support, immutable vault lock semantics, Resource Guard roles and placement, redundancy fixed before the first backup, Cross Region Restore requiring GRS, and the CLI options `--soft-delete-feature-state` (`Enable`, `Disable`, `AlwaysOn`) and `--soft-delete-duration`.

Method: documentation only; no commands were run.

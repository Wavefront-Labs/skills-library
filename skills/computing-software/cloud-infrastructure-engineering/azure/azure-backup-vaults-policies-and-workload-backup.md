---
id: computing-software.cloud-infrastructure-engineering.azure.azure-backup-vaults-policies-and-workload-backup
name: azure-backup-vaults-policies-and-workload-backup
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-backup, recovery-services-vault, backup-vault, backup-policy, vm-backup, enhanced-policy, files-backup, blob-backup, sql-backup, sap-hana-backup, aks-backup, disk-backup, postgresql-backup, backup-center, business-continuity-center, soft-delete, immutable-vault, multi-user-authorization, resource-guard, cross-region-restore, instant-restore, file-level-recovery, backup-reports, backup-policy-at-scale, restore-testing, vault-setup, vault-redundancy]
level: practitioner
status: docs-checked
description: "Protect workloads with Azure Backup: vault choice, VM Enhanced policy, vault hardening (soft delete, immutability, MUA), cross-region restore and restore drills."
sources: ["https://learn.microsoft.com/en-us/azure/backup/backup-azure-recovery-services-vault-overview", "https://learn.microsoft.com/en-us/azure/backup/backup-vault-overview", "https://learn.microsoft.com/en-us/azure/backup/backup-azure-vms-enhanced-policy", "https://learn.microsoft.com/en-us/azure/backup/backup-azure-vms-introduction", "https://learn.microsoft.com/en-us/azure/backup/secure-by-default", "https://learn.microsoft.com/en-us/azure/backup/backup-azure-immutable-vault-concept", "https://learn.microsoft.com/en-us/azure/backup/multi-user-authorization-concept", "https://learn.microsoft.com/en-us/cli/azure/backup/vault"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Azure Backup — vaults, policies and restores you have actually rehearsed

**Goal:** every stateful resource has a backup policy applied automatically, the vault
can't be emptied by a compromised admin, and restores are tested on a schedule.

## 1. Which vault
- **Recovery Services vault** (RSV): Azure VM backup (the vault must be in the same region as
  the VM) and the other classic workloads described on the RSV overview page.
- **Backup vault**: the newer workloads, for example Azure Disks, PostgreSQL, vaulted blobs
  and AKS (Backup vaults overview). Backup vaults use system- or user-assigned managed
  identities for access to the source resources, and offer Azure RBAC; you choose the
  storage redundancy when creating the vault.
```bash
az backup vault create -g rg-bk -n rsv-prod-uks -l uksouth
az backup vault backup-properties set -g rg-bk -n rsv-prod-uks --backup-storage-redundancy GeoRedundant --cross-region-restore-flag Enabled   # set BEFORE first backup
az backup vault update ... --immutability-state Unlocked   # then Locked once proven; Locked cannot be reversed
```

## 2. VM backup
```bash
az backup policy create -g rg-bk -v rsv-prod-uks -n pol-vm-daily --backup-management-type AzureIaasVM --policy policy.json   # Enhanced policy JSON
az backup protection enable-for-vm -g rg-bk -v rsv-prod-uks --vm <vm-id> --policy-name pol-vm-daily
az backup protection backup-now -g rg-bk -v rsv-prod-uks -c <container> -i <item> --retain-until 01-01-2027
```
- **Enhanced policy**: zone-resilient (ZRS) Instant Restore snapshots, hourly schedules
  (every 4, 6, 8, 12 or 24 hours), snapshot (instant restore) retention 1 to 30 days with a
  default of 7 (it cannot exceed vault retention, and the maximum shrinks as snapshots per
  day rise), support for Trusted Launch VMs, Premium SSD v2 and Ultra Disks. Defaults for
  retention are 180 days daily, 12 weeks weekly, 60 months monthly, 10 years yearly.
  After a VM is protected with Enhanced you cannot switch it back to Standard; Standard
  protects Trusted Launch VMs only through newer Azure CLI, PowerShell or REST versions
  (see the Enhanced policy page for the exact versions).
- The backup extension on the VM is `VMSnapshot` (Windows) or `VMSnapshotLinux` (Linux).
- Disks up to 32 TB each are covered by VM backup; see the VM backup introduction for the size table.

## 3. Harden the vault (ransomware)
- **Soft delete**: deleted backup data stays recoverable; the retention can be 14 to 180
  days with 14 as the default, and can be made always-on so it cannot be disabled.
- **Immutable vault**: blocks operations that lose recovery points. Enabling is reversible
  (**Unlocked**); **Locked** is irreversible and adds WORM storage. Run Unlocked until you
  are satisfied with the effect, then lock.
- **Multi-user authorization** uses a **Resource Guard**: critical operations on the vault
  need authorization on the guard, so a compromised vault admin alone cannot proceed.
  See the multi-user authorization page for which operations and roles apply.
- Cross-region restore is configured with `--cross-region-restore-flag` (Disabled or
  Enabled) next to `--backup-storage-redundancy`; PostgreSQL backups in Backup vaults can use it too, billed at RA-GRS rates.

## 4. Operate at scale
- Use Azure Policy for tag-driven backup so new VMs are covered without tickets, and audit
  for unprotected resources.
- Send vault diagnostics to a Log Analytics workspace for reports; alert on failed jobs.
- Quarterly **restore drill**: restore a VM to an isolated VNet, boot, app check; restore a
  database to a point in time; test cross-region restore on one VM; record RTO.

## Gotchas
- Choose storage redundancy and cross-region restore before the first backup.
- Deleting a VM does not stop its backup; stop protection explicitly (`az backup protection disable`)
  and decide whether to keep or delete the data.
- A Locked immutable vault cannot be unlocked, so rehearse in Unlocked first.

## Verify
- [ ] No production VM, share or database is unprotected.
- [ ] Recent jobs succeed or are triaged; failures alert on-call.
- [ ] `az backup vault show` confirms soft-delete state and immutability state as intended.
- [ ] A drill record under 90 days old exists.

## Checked
2026-10-28. Confirmed against the RSV and Backup vault overviews, Enhanced policy, VM backup
introduction, secure-by-default (soft delete 14 to 180 days, default 14), immutable vault,
multi-user authorization and `az backup vault` CLI pages: Enhanced policy figures,
`VMSnapshot`/`VMSnapshotLinux`, immutability states, `--cross-region-restore-flag` (the old
`--cross-region-restore-enabled` flag does not exist), same-region rule, 32 TB disk size.
Removed as unconfirmed: vault-to-workload table detail, built-in role list, Files, blob,
disk, SQL, SAP HANA, AKS and MySQL workload details and limits, the 200-snapshot figure, the
Business Continuity Center and diagnostic table names, `AzureBackupRG` and `vmbackup.conf`
details, and the claim that Enhanced is required for Trusted Launch (Standard also works via
newer clients). Commands were checked for existence with the command checker.
Method: documentation only; no commands were run.

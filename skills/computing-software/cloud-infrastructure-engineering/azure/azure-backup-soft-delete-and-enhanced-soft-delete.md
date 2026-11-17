---
id: computing-software.cloud-infrastructure-engineering.azure.azure-backup-soft-delete-and-enhanced-soft-delete
name: azure-backup-soft-delete-and-enhanced-soft-delete
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-backup, backup-soft-delete, enhanced-soft-delete, immutable-vault, multi-user-authorization]
level: advanced
status: docs-checked
description: "Configure Azure Backup soft delete and enhanced soft delete (always-on, retention 14-180 days), immutable vaults and MUA, and undelete backup items safely."
sources: ["https://learn.microsoft.com/azure/backup/backup-azure-enhanced-soft-delete-about", "https://learn.microsoft.com/azure/backup/secure-by-default", "https://learn.microsoft.com/azure/backup/backup-azure-immutable-vault-concept", "https://learn.microsoft.com/azure/backup/multi-user-authorization-concept"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backup soft delete and enhanced soft delete

**Goal:** make sure an attacker or mistake cannot permanently destroy backups.

## Levels
| Feature | What it does | Reversible? |
|---|---|---|
| Soft delete (secure by default) | Deleted backup data kept 14 days by default, no cost for those 14 days | Cannot be disabled in regions where secure-by-default is in preview or GA |
| **Configurable retention** | Soft-delete retention of **14-180 days**; days beyond 14 are billed at regular backup rates | Change at any time; the period active at deletion governs |
| **Immutable vault** | Blocks operations that could lose recovery points | Enabled can be disabled; **locked** is irreversible |
| **Multi-user authorization (MUA)** | Critical operations need permission on a Resource Guard owned by someone else (can sit in another subscription or tenant) | Remove MUA protection is a mandatory-protected operation |

Recovery Services vaults and Backup vaults both support soft delete, immutability and MUA (check the region and workload tables on each page).

## Configure
```bash
az backup vault backup-properties set -g rg -n vault1 --soft-delete-feature-state AlwaysON --soft-delete-duration 30
az backup vault update -g rg -n vault1 --immutability-state Unlocked   # test, then Locked
```
Lock immutability only after confirming the impact: locking is irreversible.

MUA: the security admin owns a **Resource Guard** (a different user; optionally another subscription or tenant) and grants the backup admin Reader on it so MUA can be enabled. For a critical operation the backup admin requests the `Backup MUA Operator` role, for example through PIM.

## Undelete
1. Vault → Backup items → item shows "Soft deleted".
2. *Undelete* (`az backup protection undelete -g rg -v vault1 -c <container> -i <item> --workload-type VM --backup-management-type AzureIaasVM`).
3. Resume protection with a policy; data reappears.
Soft-delete retention beyond 14 days is billed at regular backup rates.

## Gotchas
- Deleting a Recovery Services vault or Backup vault that holds soft-deleted items moves the vault into a soft-deleted state (portal), recoverable within the retention period.
- A backup item already in a soft-deleted state cannot be reconfigured to the same vault; protect it in a different vault, or undelete and resume (Recovery Services vaults).

## Verify
- [ ] `az backup vault backup-properties show -g rg -n vault1 --query "[0].properties.{sd:softDeleteFeatureState, days:softDeleteRetentionPeriodInDays}"` returns AlwaysON.
- [ ] Drill: delete a test VM backup, undelete it, restore a file.

## Checked
2026-11-01. Confirmed against Microsoft Learn secure-by-default (enhanced soft delete), immutable vault and multiuser authorization pages: 14-180 day retention, 14 days free, billing beyond, cannot disable in secure-by-default regions, locked immutability irreversible, Resource Guard roles and placement, PIM mention. The az commands match the CLI reference (check_commands). Removed: portal path, Backup center alert claim, and the vault-deletion claim that contradicted the docs.
Method: documentation only; no commands were run.
